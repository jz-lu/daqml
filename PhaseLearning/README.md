# XXZLearning

The code files in this folder are split into files associated with generating training states (ground states of the XXZ Hamiltonian) and testing meshes (meshes of ground
states) that will be used in the learning, and files which perform the machine learning itself and generate a learned phase diagram.

#### Training/Testing Files 
<ul>
  <li> <code> Ham_XXZ_J3J6.m </code>  </li> contains a function to generate the XXZ Hamiltonian with a specified number of qubits and parameters J3/J6 and alpha.
  <li> <code> XXZtrain.m  </code> </li> generates and saves a training state, which is a ground state of the XXZ Hamiltonian (with specified qubit number/parameters).
  <li> <code> XXZ_test_take2.m  </code> </li> generates and saves a testing mesh, which is an array of XXZ Hamiltonian ground states at different parameters, which
  are linearly spaced horizontally and vertically.
</ul>

#### Quantum Machine Learning Files
<ul>
  <li> <code> pl_noisy_DA.jl </code> performs noisy DA phase learning, and takes seven command line arguments:
  <ul>
    <li><code> lr </code> specifies the learning rate.</li>
    <li><code> depth </code> specifies the block depth of the QML circuit.</li>
    <li><code> mesh </code> specifies the length of the parameter mesh used for testing (assumed to be square).</li>
    <li><code> num_q </code> specifies the system size (qubit number).</li>
    <li><code> nits </code> specifies the number of training iterations to be performed.</li>
    <li><code> phase </code> specifies the phase of the training state used.</li>
    <li><code> taskid </code> specifies the number of times this learning has been performed. If one desires to perform the learning just once, rather than looking at many results for say, averaging, this parameter should be set to 1.</li>
  </ul>
    This script imports a user-specified training state and testing mesh.  Before training begins, we define a function <code>get_new_noise_circuit()</code> which generates a circuit with depth and size specified by the command line arguments, and randomly sampled noise on the digital and analog gates.  Then the training loop begins, where the training loss (average Rydberg density) of the training state on a random noisy circuit is calculated. Gradient descent is performed on the circuit output using the Flux optimizer.  A new noisy circuit is then generated, and its parameters are updated accordingly. This loop continues <code>nits</code> times.
    After training is completed, the circuit with its final updated parameters is used to find the loss (average Rydberg density) at each point in the testing mesh.  This <code>mesh</code>x<code>mesh</code> array of losses is then saved in an <code>.npy</code> array titled <code>Testlosses</code> with additional labels specifed by the command line arguments.
   </li>
  
  <li> <code> pl_noisy_D.jl  </code> </li> performs noisy digital phase learning, and takes the identical 7 command line arguments as <code>pl_noisy_DA.jl</code>.  Workflow is exactly the same as in the above, except the circuit sampled by <code>get_new_noise_circuit</code> is a noisy digital circuit.  The saved array of testing meshes is the noisy digital learned phase diagram.
  <li> <code> cluster_pl.jl </code> </li> performs noiseless phase learning (DA, digital, and just rotations).  This script takes the same 7 command line arguments as specified earlier, as well as one additional argument <code>circ</code>, which indicates the type of circuit to use: <code>DA</code> will generate a DA circuit, <code>D</code> will generate a digital circuit, and <circ>rots</circ> will generate a circuit with only rotation gates (this option should have <code>depth</code> specified as 1).  Learning and saves are identical as in the above scripts.
  
  <li> <code> updated_gates.jl  </code> </li> contains the function definitions for generating digital entanglement (<code>ent_cx()</code> and <code>ent_cz()</code>), the noiseless analog Hamiltonian (<code>ryd_h()</code>), as well as the loss function evaluation (<code>full_loss_evaluation_2()</code>).
   <li> <code> gates_noise_final.jl  </code> </li> contains the function definitions for noisy digital entanglement gates, as well as the analog Hamiltonian with the option of adding noise.
</ul>

#### Example: How to generate a learned phase diagram via a noisy DA circuit trained in the zAFM phase
1. Decide on the desired size of your learned phase diagram (say, 20x20).  Using <code>XXZ_test_take2.m</code>, generate a 20x20 testing mesh for your desired system size.
2. From the 20x20 parameter mesh, pick out a state in the zAFM phase.  Input these J3/J6 and alpha values into <code>XXZtrain.m</code> to generate your desired training state.
3. In <code>pl_noisy_DA.jl</code>, make sure the training vector and testing mesh import lines are set correctly.
4. Run the code in a Julia terminal as follows: <code> julia pl_noisy_DA.jl 0.1 2 20 8 40 zafm 20 </code> for learning rate of 0.1, depth 2, parameter mesh size 20, qubit number of 8, 40 training iterations, a training point in the zAFM phase, and 20 total repitions.
5. If desired, take the 20 resulting noisy learned phase diagrams and average them to obtain an "averaged" learned phase diagram.
