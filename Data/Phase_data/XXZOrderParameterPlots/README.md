# XXZ chain order parameter plotting (True Phase Diagram)

This directory contains the MATLAB files used to calculate the 8-qubit XXZ chain's 4 g.s. order parameters, the raw data for the plots, and Python code to generate the plots.

#### Order Parameter Calculation
<ul>
  <li> <code> get_OVBS.m </code>, <code> get_qzAFM.m </code>, <code> get_zAFM.m </code>, <code> get_XAFM.m </code>  </li> all use the Hamiltonian defined in <code> Ham_XXZ_J3J6.m </code> (see PhaseLearning folder) to calculate the VBS, qzAFM, zAFM, and XAFM order parameters, respectively.
  <li> <code> PlotOVBS.m </code>, <code> PlotqzAFM.m </code>, <code> PlotzAFM.m </code>, <code> PlotXAFM.m </code> </li> plot a contour plot of each respective order parameter over an <code>nx</code> x <code> ny</code> mesh of the Hamiltonian parameters.  An additional contour line is plotted separating the <code>f</code>-percentile highest contour values from the others.
  
</ul>

#### Raw Data
<ul>
  <li>  <code> vbs_op.mat </code>, <code> qzafm_op.mat </code>, <code> zafm_op.mat </code>, <code> xafm_op.mat </code>  </li> are the raw data files for each order parameter plot for an 8-qubit Hamiltonian on a 20x20 parameter mesh.
  
</ul>

#### Plotting code
  <ul>
    <li><code> op_plotting.py </code> imports the raw data, defines the contour lines for each plot, and plots a 2x2 set of labeled contour plots.</li>
  </ul>

  


