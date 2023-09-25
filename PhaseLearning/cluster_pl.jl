
using Yao, Zygote, YaoPlots, CuYao, Yao.EasyBuild, Yao.AD
using LinearAlgebra, Statistics, Random, StatsBase, ArgParse, Distributions
using Printf, BenchmarkTools, MAT, Plots, NPZ
using Flux: batch, Flux
include("updated_gates.jl")

# Location at which training vector and testing matrix are stored as .npy files
ROOT = "/n/home02/kwolinski/pl_julia"


function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table s begin
        "lr"
            help = "learning rate"
            required = true
            arg_type = Float64
    
        "depth"
            help = "block-depth of circuit"
            required = true
            arg_type = Int

         "mesh"
            help = "testing mesh size"
            required = true
            arg_type = Int

        "num_q"
            help = "number of qubits"
            required = true
            arg_type = Int

        "nits"
            help = "number of iterations for training"
            required = true
            arg_type = Int

        "phase"
            help = "phase location of training state"
            required = true
            arg_type = String

        "circ"
            help = "DA, D, or rots"
            required = true
            arg_type = String

        "taskid"
            help = "job array index"
            required = true
            arg_type = Int
    end

    return parse_args(s)
end

args = parse_commandline()

# Fix the quantum constants
nsites = num_qubit = args["num_q"]
depth = args["depth"]
mesh = args["mesh"]
phase = args["phase"]
circ = args["circ"]
task = args["taskid"]


# Fix the classical constants
batch_size = 1 # my data is 1 shot and 1 data point
#lr = 0.1
lr = args["lr"]       # learning rate
niters = args["nits"];     # number of iterations (go up to 60)
optim = Flux.AdaGrad(); # Adam optimizer

# Importing testing and training vector
if phase == "zafm"
    x_train = transpose(npzread(string("/n/home02/kwolinski/pl_julia/train_q", num_qubit, "_m", mesh, ".npy")))
elseif phase == "qz"
    x_train = transpose(npzread(string("/n/home02/kwolinski/pl_julia/qz_train_q", num_qubit, "_m", mesh, ".npy")))
elseif phase == "vbs"
    x_train = transpose(npzread(string("/n/home02/kwolinski/pl_julia/vbs_train_q", num_qubit, "_m", mesh, ".npy")))
elseif phase == "xy"
    x_train = transpose(npzread(string("/n/home02/kwolinski/pl_julia/xy_train_q", num_qubit, "_m", mesh, ".npy")))
end


x_test = npzread(string("/n/home02/kwolinski/pl_julia/test_q", num_qubit, "_m", mesh, ".npy"))

NUM_MEAS = num_qubit # Number of qubits to measure; initially doing 16, will change to 2*sqrt(n)
NUM_OPS = 2^NUM_MEAS

# Defining measurement indices
if num_qubit == 6
    idxs = (1, 2, 3, 4, 5, 6) 
elseif num_qubit == 8
    idxs = (1, 2, 3, 4, 5, 6, 7, 8) 
elseif num_qubit == 10
    idxs = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) 
elseif num_qubit == 12
    idxs = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
elseif num_qubit == 14
    idxs = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
elseif num_qubit == 16
    idxs = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
end

# Defining projectors
op0s = [put(num_qubit, k=>0.5*(I2+Z)) for k in idxs] # Projectors onto |0>
op1s = [put(num_qubit, k=>0.5*(I2-Z)) for k in idxs] # Projectors onto |1>
ops = []

for i = 0:2^(NUM_MEAS)-1
    s = bitstring(i)
    s = s[length(s)-NUM_MEAS+1:end]
    s = [parse(Int, ss) for ss in split(s, "")]
    op_here = []
    for (idx, bit) in enumerate(s)
        push!(op_here, bit == 0 ? op0s[idx] : op1s[idx])
    end
    push!(ops, chain(op_here...))
end
println(string("Number of ops = ", NUM_OPS))


# Encode the classical information into quantum registers
x_train_yao = zero_state(num_qubit)
x_train_yao.state = x_train;

cpu_x_train_yao = copy(x_train_yao) |> cpu; #telling yao we are running on cpu
focus!(cpu_x_train_yao, idxs)
#print(nactive(cpu_x_train_yao))

# finding avg rydberg density_matrix
dens = 0
for i=1:num_qubit
    term = expect(op1s[i],cpu_x_train_yao)
    global dens = dens + term
end
dens = dens/num_qubit
print("\nAverage Rydberg Density:", dens)


# Set up the ansatz
h = ryd_h(nsites, 0.98, 0.8) # prepare the Rydberg Hamiltonian 
if circ == "DA"
    composite(nbit::Int64) = chain(params_layer(nbit), NoParams(time_evolve(h, 0.25))) #DA
elseif circ == "D"
    composite(nbit::Int64) = chain(params_layer(nbit), ent_cx(nbit)) #just D
elseif circ == "rots"
    composite(nbit::Int64) = params_layer(nbit) #rotations only
end

circuit = chain(composite(nsites) for d in 1:depth)
dispatch!(circuit, :random)
params = parameters(circuit)
println(string("\nNumber of parameters = ", size(params)))

# TRAINING
loss_train_history = Float64[] # vector to save training loss

for k in 0:niters
    # calculate the loss
    train_loss = full_loss_evaluation2(circuit, op0s, cpu_x_train_yao, num_qubit)
    push!(loss_train_history, train_loss)

    if k % 5 == 0 # can print more frequently
        @printf("\nStep=%d, loss=%.15f\n", k, train_loss)
    end
    
    #=
    # at each training epoch, randomly choose a batch of samples from the training set
    batch_index = randperm(num_train)[1:batch_size]
    =#
    x_batch = x_train #[:,batch_index] #x_train is 1 vector; does this need to change?

    # prepare these samples into quantum states
    x_batch_1 = copy(x_batch)
    x_batch_yao = zero_state(num_qubit) #, nbatch=batch_size)
    x_batch_yao.state = x_batch_1
    cpu_x_batch_yao = copy(x_batch_yao) |> cpu
    batch_here = [zero_state(num_qubit) for i in 1:batch_size]

    for i in 1:batch_size
        batch_here[i].state = x_batch_1  #[:,i:i]
    end
    #may take out
    batch_here = zero_state(num_qubit)
    batch_here.state = x_batch_1
    focus!(batch_here,idxs)

    # Get the distribution of the measurement qubit in the computational hbasis
    q_ = zeros(batch_size, 2^num_qubit)  # get rid of for loops over batch size or set batch_size = 1
    res = copy(cpu_x_train_yao) |> circuit
    for i = 1:batch_size
        rdm = density_matrix(viewbatch(res, i), idxs)
        q_[i,:] = Yao.probs(rdm)
    end
    
    # calculate the gradients w.r.t. the loss function
    arr = Array{Float64}(zeros(num_qubit, nparameters(circuit)))
    for i = 1:num_qubit
        arr[i,:] = expect'(op1s[i], copy(cpu_x_train_yao)=> circuit)[2]
    end

    # TODO: change this; don't need to sum over batch
    grads = collect(mean([-sum([arr[i,:] for i in 1:num_qubit])]))
    #grads = collect(mean([-sum([Arr[i,j,:] for j in 1:NUM_OPS]) for i = 1:batch_size])) WAS USING THIS
    #grads = collect(mean([-sum([(2*q_)[i,j] * Arr[i,j,:] for j in 1:NUM_OPS]) for i = 1:batch_size]))
    
    # update the parameters
    updates = Flux.Optimise.update!(optim, params, grads);
    dispatch!(circuit, updates)
end

# Save the circuit parameters
params = parameters(circuit)
println("Writing parameters...")
npzwrite(string("params_d", depth, "_q", num_qubit, "_p", phase, "_circ", circ, "_its", niters, "_task", task, ".npy"), params)
npzwrite(string("trainloss_d", depth, "_q", num_qubit, "_p", phase, "_circ", circ, "_its", niters, "_task", task, ".npy"), loss_train_history)
# Plotting training loss versus time
using Plots 
its= LinRange(0,niters,niters+1) #iterations
p = Plots.plot(its,loss_train_history)
title!("Training loss versus iteration\n d: $(depth)_q: $(num_qubit)_p: $(phase)_circ: $(circ)_its: $(niters)_task: $(task)")
xlabel!("Iteration")
ylabel!("Training loss")

savefig(string("Trainloss_d ",depth, "_q", num_qubit, "_p", phase, "_circ", circ, "_its", niters, "_task", task, ".pdf"))
Plots.display(p)

# Evaluating loss at each point in testing mesh
test_vec = Array{Float64}(undef, 0) # random row that will be deleted from matrix
for i in 1:mesh
    for j in 1:mesh
        test_state = x_test[i,j,:]
        x_test_yao = zero_state(num_qubit)

        test_state = reshape(test_state, length(test_state), 1)
        x_test_yao.state = test_state;
        cpu_x_test_yao = copy(x_test_yao) |> cpu; #telling yao we are running on cpu
        focus!(cpu_x_test_yao, idxs)
        test_loss = full_loss_evaluation2(circuit, op0s, cpu_x_test_yao, num_qubit)
        test_loss = Real(test_loss)
        
        push!(test_vec, test_loss)
    end
end

row = reshape(test_vec, mesh, mesh)

npzwrite(string("Testlosses_d", depth, "_q", num_qubit, "_p", phase, "_circ", circ, "_its", niters, "_task", task, ".npy"), row)

println("\nDone Testing")

# Plotting the test loss, i.e. Learned PD
J_ratios = LinRange(0.01,2.5,mesh)
alphas = LinRange(0.01,1,mesh);

p1 = contour(J_ratios, alphas, row, levels=25, color=:turbo, fill=true)
title!("Learned PD \n d: $(depth)_q: $(num_qubit)_p: $(phase)_circ: $(circ)_its: $(niters)_task: $(task)")
xlabel!("J_ratios")
ylabel!("alphas")

savefig(string("LPD_d ",depth, "_q", num_qubit, "_p", phase, "_circ", circ, "_its", niters, "_task", task, ".pdf"))
Plots.display(p1)

println("Done.")
