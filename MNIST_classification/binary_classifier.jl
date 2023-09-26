using Yao, Zygote, YaoPlots, CuYao, Yao.EasyBuild, Yao.AD
using LinearAlgebra, Statistics, Random, StatsBase, ArgParse, Distributions
using Printf, BenchmarkTools, MAT, NPZ
using Flux: batch, Flux
using TickTock
include("gates.jl")

# location of the MNIST encoded data
ROOT = "../../MNIST_8/"


function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table s begin
        "--lr"
            help = "learning rate"
            arg_type = Float64
            default = 0.1
        "mode"
            help = "selects to train on digital or digital analog"
            arg_type = String
            required = true
            default = "DA"    
        "--evo_time"
            help = "evolution time paramter"
            arg_type = Float64
            default = 0.87
        "depth"
            help = "block-depth of circuit"
            required = true
            arg_type = Int
        "noise"
            help = "train and test on noisy circuits if true"
            required = true
            arg_type = Bool
        "output"
            help = "the directory to write the outputs of this program"
            required = true
            arg_type = String
            default="./"
    end

    return parse_args(s)
end

args = parse_commandline()

# Fix the quantum constants
nsites = num_qubit = 8
depth = args["depth"]
time = args["evo_time"]
output_location = args["output"]
NUM_MEAS = 1 # Number of qubits to measure
pos_ = 1 # index of qubit that will be measured
println(string("Measuring qubit ", pos_))
op0 = put(num_qubit, pos_=>0.5*(I2+Z)) # Projector onto |0>
op1 = put(num_qubit, pos_=>0.5*(I2-Z)) # Projector onto |1>


function get_new_noise_circuit()
    noise = args["noise"]
    function get_composite()
        h = ryd_h(nsites, 0.87, 0.8, noise) # prepare the Rydberg Hamiltonian
        return composite(nbit::Int64) = chain(params_layer(nbit), NoParams(time_evolve(h, time)))
    end
    function get_composite_digital()
        cx = noise ? ent_cx_noisy : ent_cx
        return composite(nbit::Int64) = chain(params_layer(nbit), cx(nbit))
    end
    generator = args["mode"] == "DA" ? get_composite : get_composite_digital

    noisy_circuit = chain(generator()(nsites) for d in 1:depth)
    return noisy_circuit
end

# Fix the classical constants
batch_size = 100
lr = args["lr"]       # learning rate
niters = 70;     # number of iterations
optim = Flux.AdaGrad(); # optimizer

# Import the prepared dataset of (nsites - 1) normalized principle components
x_train = transpose(npzread(ROOT * "x_train.npy"))
x_test = transpose(npzread(ROOT * "x_test.npy"))
y_train = npzread(ROOT * "y_train.npy")
y_test = npzread(ROOT * "y_test.npy")

num_train = 1000
num_test = 200
x_train = x_train[:,1:num_train]
y_train = y_train[1:num_train,:]
x_test = x_test[:,1:num_test]
y_test = y_test[1:num_test,:]
println(size(x_train))

print("Train size: ")
println(num_train)
print("Test size: ")
println(num_test)

# Encode the classical information into quantum registers
x_train_yao = zero_state(num_qubit, nbatch=num_train)
x_train_yao.state = x_train;
cpu_x_train_yao = copy(x_train_yao) |> cpu;

x_test_yao = zero_state(num_qubit, nbatch=num_test)
x_test_yao.state = x_test;
cpu_x_test_yao = copy(x_test_yao) |> cpu;

global circuit = get_new_noise_circuit()

dispatch!(circuit, :random)
params = parameters(circuit)
println(string("Number of parameters = ", size(params)))

global current_params = params

# TRAINING
loss_train_history = Float64[]
acc_train_history = Float64[]
loss_test_history = Float64[]
acc_test_history = Float64[]

for k in 0:niters
    global circuit
    global h
    global current_params

    # calculate the accuracy and loss
    train_acc, train_loss = acc_loss_evaluation(circuit, cpu_x_train_yao, y_train, num_train, pos_)

    test_circuit = get_new_noise_circuit()
    dispatch!(test_circuit, current_params)

    test_acc, test_loss = acc_loss_evaluation(test_circuit, cpu_x_test_yao, y_test, num_test, pos_) 
    push!(loss_train_history, train_loss)
    push!(loss_test_history, test_loss)
    push!(acc_train_history, train_acc)
    push!(acc_test_history, test_acc)
    if k % 5 == 0
        @printf("\nStep=%d, loss=%.3f, acc=%.3f, test_loss=%.3f, test_acc=%.3f\n", k, train_loss, train_acc,test_loss, test_acc)
    end
    
    # define n_batch noisy circuits for 
    batch_noise = [get_new_noise_circuit() for i in 1:batch_size]

    # at each training epoch, randomly choose a batch of samples from the training set
    batch_index = randperm(num_train)[1:batch_size]
    x_batch = x_train[:,batch_index]
    y_batch = y_train[batch_index,:]

    # prepare these samples into quantum states
    x_batch_1 = copy(x_batch)
    x_batch_yao = zero_state(num_qubit, nbatch=batch_size)
    x_batch_yao.state = x_batch_1
    cpu_x_batch_yao = copy(x_batch_yao) |> cpu
    batch_here = [zero_state(num_qubit) for i in 1:batch_size]

    for i in 1:batch_size
        batch_here[i].state = x_batch_1[:,i:i]
    end
    
    # Get the distribution of the measurement qubit in the computational hbasis
    q_ = zeros(batch_size, 2)
    for i = 1:batch_size
        # reset the circuit each time with new noise
        dispatch!(batch_noise[i], current_params)

        res = copy(cpu_x_train_yao) |> batch_noise[i]
        rdm = density_matrix(viewbatch(res, i), (pos_,))
        q_[i,:] = Yao.probs(rdm)
    end
    
    # calculate the gradients w.r.t. the cross-entropy loss
    Arr = Array{Float64}(zeros(batch_size, nparameters(circuit)))
    for i = 1:batch_size
        dispatch!(batch_noise[i], current_params)
        Arr[i,:] = expect'(op0, copy(batch_here[i])=>batch_noise[i])[2]
    end
    C = [Arr, -Arr] # hack for double efficiency, since op0 = 1 - op1 ==> op1' = -op0'
    grads = collect(mean([-sum([y_batch[i,j]*((1 ./ q_)[i,j]) * batch(C)[i,:,j] for j in 1:2]) for i = 1:batch_size]))
    
    circuit = get_new_noise_circuit()

    # update the parameters
    updates = Flux.Optimise.update!(optim, params, grads);
    dispatch!(circuit, updates)

    current_params = updates

    # write while in progress
    npzwrite(string(output_location ,"_train_acc_", time, "_", depth, "_", ".npy"), acc_train_history)
    npzwrite(string(output_location ,"_test_acc_", time, "_", depth, "_", ".npy"), acc_test_history)

end

# Save the circuit parameters
params = parameters(circuit)
println("Writing parameters...")
npzwrite(string(output_location ,"_parameters_", time, "_", depth, "_", ".npy"), params)

# save train and test accuracy after each round of training
npzwrite(string(output_location ,"_train_acc_", time, "_", depth, ".npy"), acc_train_history)
npzwrite(string(output_location ,"_test_acc_", time, "_", depth, ".npy"), acc_test_history)

# save train and test loss after each round of training
npzwrite(string(output_location ,"_train_loss_", time, "_", depth, "_", ".npy"), loss_train_history)
npzwrite(string(output_location ,"_test_loss_", time, "_", depth, "_", ".npy"), loss_test_history)
