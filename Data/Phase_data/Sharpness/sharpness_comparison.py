import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
%matplotlib inline

ROOT = ".\" # file root at which Rb/a = 0.87
mesh = 20
J_ratios = np.linspace(0.01,2.5,mesh)
alphas = np.linspace(0.01,1,mesh)
phase = "zAFM"
if phase == "zAFM":
    train_point = (0.01, 0.2184)

# Function for calculating the sharpness of an averaged learned phase diagram
n = 100
num_trials = 5
trial_size = int(n/num_trials) #in my case 20 results per trial

def get_sharpness(nq, d, circ):

    # saving array of loss arrays
    loss_arrays = []

    for j in range(num_trials):
        for i in range(trial_size):
            losses = np.load(f"{ROOT}\\Testlosses{circ}_d{d}_q{nq}_pzafm_its70_task{(j*trial_size)+i+1}.npy")
            loss_arrays.append(losses)
        
    avg_losses_array = []    
    for j in range(num_trials):
        total = np.zeros((20,20))
        for i in range(trial_size):
            total = np.add(total, loss_arrays[i+(j*trial_size)])
        averaged_losses = total / trial_size
        avg_losses_array.append(averaged_losses)
    
    trial_stds = []
    for i in range(num_trials):
        horiz_grad = np.gradient(np.array(avg_losses_array[i], dtype=float))[0]
        vert_grad = np.gradient(np.array(avg_losses_array[i], dtype=float))[1]

        grad_mag = np.square(horiz_grad) + np.square(vert_grad)

        stdev = np.std(grad_mag)
        trial_stds.append(stdev)

    trial_mean = np.mean(trial_stds)
    trial_stdev = np.std(trial_stds)

    return trial_mean, trial_stdev
    
# returns mean and std of the sharpnesses for num_trials trials

# example of using this function:
print(get_sharpness(8,3,'DA'))

# 8 qubits (saving data in arrays for DA and digital)
depth_arr_8 = [2,3,4,5,6,7,8,9,10,11,12,13,14]
sharpness_8_D = []
sharpness_8_DA = []
for i in range(len(depth_arr_8)):
    sharpness_8_D.append(get_sharpness(8, depth_arr_8[i],'D')[0])
    sharpness_8_DA.append(get_sharpness(8, depth_arr_8[i],'DA')[0])

errors_8_D = []
errors_8_DA = []
for i in range(len(depth_arr_8)):
    errors_8_D.append(get_sharpness(8, depth_arr_8[i],'D')[1])
    errors_8_DA.append(get_sharpness(8, depth_arr_8[i],'DA')[1])

# Repeating above with different Hamiltonian parameters
ROOT2 = ".\" # file root at which Rb/a = 0.98
sharpness_8_DA_2 = []
for i in range(len(depth_arr_8)):
    sharpness_8_DA_2.append(get_sharpness(8, depth_arr_8[i],'DA')[0])

errors_8_DA_2 = []
for i in range(len(depth_arr_8)):
    errors_8_DA_2.append(get_sharpness(8, depth_arr_8[i],'DA')[1])

# PLOTTING ---------------------------------------------------------
# plotting side by side

FONT_SIZE = 28
label_size = FONT_SIZE - 2


plt.rcParams["figure.figsize"] = [10, 6]
plt.rcParams["figure.autolayout"] = True

fig, ax1 = plt.subplots(1)

ax1.errorbar(depth_arr_8, [x * 1000 for x in sharpness_8_DA], yerr=[x * 1000 for x in errors_8_DA], marker='o', label='DA, ' + r"$\mathrm{R}_\mathrm{b}$" + "/a = 0.87", color='red')
ax1.errorbar(depth_arr_8, [x * 1000 for x in sharpness_8_D], yerr=[x * 1000 for x in errors_8_D], marker='o', label='Digital', color='blue')
ax1.errorbar(depth_arr_8, [x * 1000 for x in sharpness_8_DA_2], yerr=[x * 1000 for x in errors_8_DA_2], marker='o', label='DA, ' + r"$\mathrm{R}_\mathrm{b}$" + "/a = 0.98", color='gray')


ax1.tick_params(axis='x', labelsize=label_size)
ax1.tick_params(axis='y', labelsize=label_size)


ax1.legend(fontsize=label_size)

ax1.set_xlabel("Number of layers " + r'($\ell$)', fontsize=FONT_SIZE)
ax1.set_ylabel(r'$\sigma_{\mathrm{learn}}$'+ '  ' + r'$(10^{-3})$', fontsize=FONT_SIZE)
