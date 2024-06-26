# XXZ chain depth 2 Digital vs Digital-Analog comparison

This directory contains the raw data files for the averaged learned phase diagrams for noisy DA and noisy digital at depth 2 presented in the paper, and Python code to generate the plots.


#### Raw Data
<ul>
  <li>  <code> zafm_8_DA_noisyaveraged.npy </code> and <code> zafm_8_DA_noisyaveraged.npy </code>  </li> are 20x20 arrays of the final test loss for the 8-qubit, depth 2 DA and Digital noisy circuits, trained in the zAFM phase region.  Each file is generated by averaging over 20 runs.  The 20 raw "test losses" files are provided in the <code>DA_Testlosses</code> and <code>D_Testlosses</code> for the DA and Digital noisy circuits, respectively.  These are sample output files achieved from running <code>pl_noisy_D.jl</code> and <code>pl_noisy_DA.jl</code> (see PhaseLearning folder).
  
</ul>

#### Plotting code
  <ul>
    <li><code> depth2_plotting.py </code> generates the averaged plots mentioned above by averaging the results of 20 independent learning runs.  The results of these runs are specifically the test losses generated by running <code> pl_noisy_D.jl </code> and <code>pl_noisy_DA.jl</code>(see PhaseLearning folder), which are named as follows: <code>Testlosses{circ}_d{d}_q{nq}_p{phase}_its70_task{i+1}.npy </code>.<br />
After creating and saving these averaged data files, the code plots them as a 2x1 set of contour plots, with training point labeled.  This code will also overlay the contour lines defined for the XXZ order parameter plots (see XXZOrderParameterPlots folder).
       </li>
    
  </ul>

 **NOTE:** The final 4 lines of this code overlays the contours from the XXZ order parameter plots to visually distinguish the phase boundaries.  The variables <code>xafm_op</code> and <code>xafm_contour_value </code>, etc. are defined in <code>op_plotting.py </code> (see XXZOrderParameterPlots github folder) and will not be defined if the variables from this file have not been included.  In this case, or if the contours are not desired, just comment out the last 4 lines.
