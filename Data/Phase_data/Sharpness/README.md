# DA vs Digital Learned PD sharpness comparisons

This directory contains the raw data files for the sharpness comparison plot presented in the paper, and Python code to calculate the sharpnesses and generate the plot.


#### Raw Data
<ul>
  <li>  <code> Testlosses_D </code>, <code> Testlosses_DA_Rbovera=0.98 </code>, and <code> Testlosses_DA_Rbovera=0.87 </code>  </li> are folders containing 1,300 final "test loss" arrays (i.e. Learned phase diagrams) for digital, DA with Rb/a = 0.98, and DA with Rb/a = 0.87 circuits respectively.  There are 100 arrays generated at each circuit depth (from 2 to 14), totalling in 1,300 per folder.
  
</ul>

#### Plotting code
  <ul>
    <li><code> sharpness_comparison.py </code> defines the function <code>get_sharpness(nq, d, circ)</code>.  This function splits the final test losses (for each given depth) in <code>num_trials</code> groups of <code>trial_size</code> arrays (in this case 5 and 20, respectively, for the total of 100 diagrams per depth). This program then calculates the "sharpness" for the averaged PD of <code>trial_size</code diagrams, which is defined as the standard deviation of the gradient of the diagram.  This number is calculated for all 13 depths for all 3 circuit types, and then plotted with error bars.
       </li>
    
  </ul>




