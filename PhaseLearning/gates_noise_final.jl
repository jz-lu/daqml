using Yao, Bloqade, YaoBlocks
using SparseArrays, LinearAlgebra
using Random, Distributions

# setting up random generator for 1 percent noise
d = Normal(0, 0.1)

# noise for cnot, found by sampling average fidelity
cnot_noise = Normal(0, 0.065)

println("entering gates")

# Digital entanglement
ent_cx(nbit::Int64) = (nbit%2 == 0) ? 
    chain(chain(nbit,control(i,i+1=>X) for i in 1:2:nbit-1),
          chain(nbit,control(i,i+1=>X) for i in 2:2:nbit-2)) : 
    chain(chain(nbit,control(i,i+1=>X) for i in 1:2:nbit-2),
          chain(nbit,control(i,i+1=>X) for i in 2:2:nbit-1))

# somehow needed to broadcast the matrix I defined into a proper Julia "Matrix"
# could have used a simliar definition using the array method but I think having the matrix there helps
function vecvec_to_matrix(vecvec)
    dim1 = length(vecvec)
    dim2 = length(vecvec[1])
    my_array = zeros(ComplexF64, dim1, dim2)
    for i in 1:dim1
        for j in 1:dim2
            my_array[i,j] = vecvec[i][j]
        end
    end
    return my_array
end

function noisy_cnot_approx_gate(theta::Float64)
    exp_term = exp(-4im * theta)
    big_endian = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0.5 * (1 + exp_term), 0.5 - 0.5 * exp_term],
        [0, 0, 0.5 * (1 - exp_term), 0.5 + 0.5 * exp_term],
    ]
    # rotation_on_target = [
    #     [0.5 * (1 + exp_term), 0.5 - 0.5 * exp_term],
    #     [0.5 * (1 - exp_term), 0.5 + 0.5 * exp_term],
    # ]
    be = vecvec_to_matrix(big_endian)
    return matblock(be, tag=string("crot", theta))
end

# digital cnot gate with noise (add noise to angle of rotation)
function ent_cx_noisy(nbit::Int64)
    return (nbit%2 == 0) ? 
    chain(chain(nbit,put((i, i+1)=>noisy_cnot_approx_gate(pi/4 + rand(cnot_noise, 1)[1])) for i in 1:2:nbit-1),
        chain(nbit,put((i, i+1)=>noisy_cnot_approx_gate(pi/4 + rand(cnot_noise, 1)[1])) for i in 2:2:nbit-2)) : 
    chain(chain(nbit,put((i, i+1)=>noisy_cnot_approx_gate(pi/4 +rand(cnot_noise, 1)[1])) for i in 1:2:nbit-2),
        chain(nbit,put((i, i+1)=>noisy_cnot_approx_gate(pi/4 + rand(cnot_noise, 1)[1])) for i in 2:2:nbit-1))
end

println("ent_cx done")

ent_cz(nbit::Int64) = (nbit%2 == 0) ? 
    chain(chain(nbit,control(i,i+1=>Z) for i in 1:2:nbit-1),
          chain(nbit,control(i,i+1=>Z) for i in 2:2:nbit-2)) : 
    chain(chain(nbit,control(i,i+1=>Z) for i in 1:2:nbit-2),
          chain(nbit,control(i,i+1=>Z) for i in 2:2:nbit-1))

println("ent_cz done")

# Digital rotations
rx_layer(nbit::Int64) = chain(put(nbit, i => Rx(0)) for i in 1:nbit)
rz_layer(nbit::Int64) = chain(put(nbit, i => Rz(0)) for i in 1:nbit)
params_layer(nbit::Int64) = chain(rx_layer(nbit),rz_layer(nbit),rx_layer(nbit))
p_chain(op, nbit::Int64, total::Int64) = chain(put(total, i => op) for i in 1:nbit)

println("digital rotations done")


# Analog Hamiltonian, with option of adding noise
function ryd_h(nsites::Int64, Rb_over_a::Float64, Δ_over_Ω::Float64, noise::Bool=false)
    Ω = 2π * 4 # MHz, radians per microsecond is this times 2pi, bloqade may be radians per second
    C6 = 2π * 862690 # MHz * μm^6
    Rb = (C6 / Ω)^(1/6)
    Δ = Δ_over_Ω * Ω # has units of omega MHz, 
    a = Rb / Rb_over_a

    if noise
        perturbations = rand(d, 2)
        Ω = Ω * (1 + perturbations[1]/10) # multiplicative error
        # Δ = Δ * (1 + perturbations[2]) # detuning is additive error only
        Δ = Δ + perturbations[2] # since we are drawing from 0.01 std dev, we can multiply by 10 to get 0.1 std dev
    end


    local atoms
    if !noise  
        atoms = generate_sites(ChainLattice(), nsites, scale = a)  
    else
        # generate noise: For atoms additve error to position ~ std dev 100 nanometers = .1 micron
        # lattices are default in microns

        # PREVIOUS MODEL (NOT IN CODE): 1% noise in x and y, x: (1 + perturbation) * a , y : a * pertubation
        x_coords = LinRange(1, nsites * a, nsites)
        x_noise = rand(d, nsites)
        x_coords = x_coords .+ x_noise # noise is std dev 0.1, so it is already in correct units

        y_noise = rand(d, nsites) # perturbation of 0.1 micron noise
        y_coords = y_noise

        atoms = AtomList(collect(zip(x_coords, y_coords))) # creates the atom coordinates (x, y) with noise
    end

    h = rydberg_h(atoms; Δ=Δ, Ω=Ω) # create the Rydberg Hamiltonian
    return matblock(h)
end

# Loss function
function acc_loss_evaluation(circuit::ChainBlock, reg::AbstractArrayReg, y_batch::Matrix{Float64}, batch_size::Int64, pos_::Int64)
      # pos_ is the measurement qubit index
      res = copy(reg) |> circuit
      q_ = zeros(batch_size, 2);
      for i = 1:batch_size
          rdm = density_matrix(viewbatch(res, i), (pos_,))
          q_[i,:] = Yao.probs(rdm)
      end
      
      pred = [x[2] for x in argmax(q_, dims=2)[:]]
      y_max = [x[2] for x in argmax(y_batch, dims=2)[:]]
      acc = sum(pred .== y_max) / batch_size
      loss = crossentropy(y_batch, q_) / batch_size
      acc, loss
  end


# Full loss function
function full_acc_loss_evaluation(circuit::ChainBlock, reg::AbstractArrayReg, y_batch::Matrix{Float64}, batch_size::Int64, idxs::Vector{Int64}=[1,2,3], nbit::Int64=3)
    res = copy(reg) |> circuit
    q_ = zeros(batch_size, 2^nbit);
    for i = 1:batch_size
        rdm = density_matrix(viewbatch(res, i), idxs)
        q_[i,:] = Yao.probs(rdm)
    end
    
    pred = [x[2] for x in argmax(q_, dims=2)[:]]
    y_max = [x[2] for x in argmax(y_batch, dims=2)[:]]
    acc = sum(pred .== y_max) / batch_size
    loss = crossentropy(y_batch, q_) / batch_size
    acc, loss
end

# Full loss function
function unary_acc_loss_evaluation(circuit::ChainBlock, reg::AbstractArrayReg, y_batch::Matrix{Float64}, batch_size::Int64, nbit::Int64=8)
    # poc_ is the measurement qubit index
    res = copy(reg) |> circuit
    q_ = zeros(batch_size, nbit);
    for i = 1:batch_size
        for j = 1:nbit
            rdm = density_matrix(viewbatch(res, i), j)
            q_[i,j] = Yao.probs(rdm)[1]
        end
        q_[i,:] /= sum(q_[i,:]) # normalize
    end
    
    pred = [x[2] for x in argmax(q_, dims=2)[:]]
    y_max = [x[2] for x in argmax(y_batch, dims=2)[:]]
    acc = sum(pred .== y_max) / batch_size
    loss = crossentropy(y_batch, q_) / batch_size
    acc, loss
end
