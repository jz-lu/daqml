using Yao, Bloqade
using SparseArrays, LinearAlgebra

# Digital entanglement
ent_cx(nbit::Int64) = (nbit%2 == 0) ? 
    chain(chain(nbit,control(i,i+1=>X) for i in 1:2:nbit-1),
          chain(nbit,control(i,i+1=>X) for i in 2:2:nbit-2)) : 
    chain(chain(nbit,control(i,i+1=>X) for i in 1:2:nbit-2),
          chain(nbit,control(i,i+1=>X) for i in 2:2:nbit-1))

ent_cz(nbit::Int64) = (nbit%2 == 0) ? 
    chain(chain(nbit,control(i,i+1=>Z) for i in 1:2:nbit-1),
          chain(nbit,control(i,i+1=>Z) for i in 2:2:nbit-2)) : 
    chain(chain(nbit,control(i,i+1=>Z) for i in 1:2:nbit-2),
          chain(nbit,control(i,i+1=>Z) for i in 2:2:nbit-1))

# Digital rotations
rx_layer(nbit::Int64) = chain(put(nbit, i => Rx(0)) for i in 1:nbit)
rz_layer(nbit::Int64) = chain(put(nbit, i => Rz(0)) for i in 1:nbit)
params_layer(nbit::Int64) = chain(rx_layer(nbit),rz_layer(nbit),rx_layer(nbit))
p_chain(op, nbit::Int64, total::Int64) = chain(put(total, i => op) for i in 1:nbit)

# Analog Hamiltonian
function ryd_h(nsites::Int64, Rb_over_a::Float64, Δ_over_Ω::Float64)
    Ω = 2π * 4
    C6 = 2π * 862690 # MHz * μm^6
    Rb = (C6 / Ω)^(1/6)
    Δ = Δ_over_Ω * Ω
    a = Rb / Rb_over_a

    atoms = generate_sites(ChainLattice(), nsites, scale = a)
    h = rydberg_h(atoms; Δ=Δ, Ω=Ω) # create the Rydberg Hamiltonian
    return matblock(h)
end


# Full loss function
# measure from 1 to nqubits (calc every probability)
function full_loss_evaluation(circuit::ChainBlock, reg::AbstractArrayReg, batch_size::Int64, idxs::Vector{Int64}, nbit::Int64)
    
    res = focus!(copy(reg),idxs) |> circuit
    #=
    q_ = zeros(batch_size, 2^nbit);
    for i = 1:batch_size
        rdm = density_matrix(viewbatch(res, i), idxs)
        q_[i,:] = Yao.probs(rdm)
    end
    =#
    q_ = zeros(2^nbit)
    rdm = density_matrix(res, idxs)
    q_ = Yao.probs(rdm)
    
    # create loss function to make as close as possible to 0000 - can take difference and then norm
    loss = q_ 
    loss # just return loss
end

# measure from 1 to nqubits (calc every probability)
function full_loss_evaluation2(circuit::ChainBlock, ops::Vector{PutBlock{2, 1, Scale{Float64, 2, Add{2}}}}, reg::AbstractArrayReg, nbit::Int64)
    #res = focus!(copy(reg),idxs) |> circuit
    res = copy(reg) |> circuit
    dens = 0
    for i=1:nbit
        term = expect(ops[i],res)
        dens = dens + term
    end
    dens = dens/nbit
    
    # create loss function to make as close as possible to 0000 - can take difference and then norm
    loss = dens
    loss # just return loss
end

# sanity check calculating average rydberg density
# measure from 1 to nqubits (calc every probability)
function full_loss_evaluation3(ops::Array{PutBlock{2, 1, Scale{Float64, 2, Add{2}}}, 1}, reg::AbstractArrayReg, nbit::Int64)
    dens = 0
    for i=1:nbit
        term = expect(ops[i],reg)
        dens = dens + term
    end
    dens = dens/nbit
    loss = dens
    loss # just return loss
end


function test_loss_evaluation(state, circuit::ChainBlock, reg::AbstractArrayReg, batch_size::Int64, idxs::Vector{Int64}=[1,2,3], nbit::Int64=3)
    res = copy(reg) |> circuit
    q_ = zeros(batch_size, 2^nbit);
    for i = 1:batch_size
        rdm = density_matrix(viewbatch(res, i), idxs)
        q_[i,:] = Yao.probs(rdm)
    end
    
    # find way to evolve state in testing mesh, then measure, and return loss

    loss = 2 
    loss # just return loss
end


## --- FUNCTIONS I DON'T USE --------------------------------------------------------------------------------------------------

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
