# Numerical Convergence

This directory contains the raw data files for the numerical convergence plots in the paper's supplement, and Python code to generate the plots.


#### Raw Data
<ul>
  <li>  <code> XXZ_depth2 </code>  </li> contains 4 data files each labeled <code>zAFM_8_{circ}_{noiseless/noisy}_traininglosses.npy</code>.  These files encode the averaged (over 20 independent runs) training losses at each iteration, with a total of 70 iterations for the noisy regime, and 50 iterations for the noiseless regime.  The sub-directories <code>XXZ_noiseless</code> and <code>XXZ_noisy</code> contain the 20 raw training files each for DA and D that were averaged over (averaging performed in <code>convergence_plotting.py</code>, see next section). The training was performed on 8-qubit circuits trained in the zAFM phase.
  <li> The raw data for the 3vs8 comparison conversion plot is provided in the <code>3v8</code> folder.  For details on how this data was generated, see the <code>MNIST_data</code> folder.</li>
  
</ul>

#### Plotting code
  <ul>
    <li><code> convergence_plotting.py </code> averages the raw training loss data, and plots the 3v8 convergence data alongside the XXZ_depth2 convergence data, in the 4 regimes for circuit type and noise on/off.
       </li>
    
  </ul>




