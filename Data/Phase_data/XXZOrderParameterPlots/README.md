# XXZ chain order parameter plotting (True Phase Diagram)

This directory contains the MATLAB files used to calculate the 8-qubit XXZ chain's 4 g.s. order parameters, the raw data for the plots, and Python code to generate the plots.

# TODO (unfinished)

#### Order Parameter Calculation
<ul>
  <li> <code> get_OVBS.m </code>, <code> get_qzAFM.m </code>, <code> get_zAFM.m </code>, <code> get_XAFM.m </code>  </li> all use the Hamiltonian defined in <code> Ham_XXZ_J3J6.m </code> (see PhaseLearning folder) to calculate the VBS, qzAFM, zAFM, and XAFM order parameters, respectively.
  <li> <code> PlotOVBS.m </code>, <code> PlotqzAFM.m </code>, <code> PlotzAFM.m </code>, <code> PlotXAFM.m </code> </li> plots a contour plot of each respective order parameter over an <code>nx</code> x <code> ny</code> mesh of the Hamiltonian parameters.  An additional contour line is plotted separating the <code>f</code>-percentile highest contour values from the others.
  
</ul>

#### Raw Data
<ul>
  <li> <code> ryd_true.npy </code>  </li> encodes an entanglement entropy plot ("true phase diagram") over a range of parameters for the Rydberg chain.
  <li> <code> Z2_13_averaged.npy  </code> </li> encodes a learned phase diagram generated on a depth 5 DA circuit.
  <li> <code> ryd_rots.npy  </code> </li> encodes a learned phase diagram, trained at a different point from the above, generated on a depth 0 circuit.
</ul>

#### Plotting code
  <ul>
    <li><code> lr </code> specifies the learning rate.</li>
    <li><code> depth </code> specifies the block depth of the QML circuit.</li>
  </ul>

  


