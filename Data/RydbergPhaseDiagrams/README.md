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
    <li><code> 3x3_Rydberg_plot.py </code> plots the 3 raw data files above side-by-side.</li>
    <li><code> rydtrue_plot.py </code> generates the entangelment entropy plot and plots this figure solo.</li>
  </ul>

  

