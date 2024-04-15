# 13 qubit Rydberg chain phase diagram plotting

This directory contains the raw data for the 13 qubit Rydberg chain plots, as well as code to generate the plots.

#### Raw Data
<ul>
  <li> <code> ryd_true.npy </code>  </li> encodes an entanglement entropy plot ("true phase diagram") over a range of parameters for the Rydberg chain.
  <li> <code> Z2_13_averaged.npy  </code> </li> encodes a learned phase diagram generated on a depth 5 DA circuit.
  <li> <code> ryd_rots.npy  </code> </li> encodes a learned phase diagram, trained at a different point from the above, generated on a depth 0 circuit.
</ul>

#### Plotting code
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

  

