import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib
import scipy.io as sio
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
%matplotlib inline


# ROOT at which noisy convergence files are stored
ROOT = ".\"
# no noise
#ROOT = "C:\\Users\\Kristina\\Desktop\\QML\\rydphaselearning\\Ham\\Cluster_results\\Jobarrays\\jobarrays"

mesh = 20
J_ratios = np.linspace(0.01,2.5,mesh)
alphas = np.linspace(0.01,1,mesh)
phase = "zAFM"
if phase == "zAFM":
    train_point = (0.01, 0.2184)

if phase == "qz":
    train_point = (0.01, 0.9479)

if phase == "vbs":
    train_point = (1.5826, 0.6353)

if phase == "xy":
    train_point = (1.8447, 0.1663)

nq = 8 
d = 2
circ = "DA" # NOTE: Change this parameter to 'D' to get the digital data
n = 20

# saving array of loss arrays
loss_arrays = []
for i in range(n):
    losses = np.load(f"{ROOT}\\Testlosses{circ}_d{d}_q{nq}_p{phase}_its70_task{i+1}.npy")
    #losses = np.load(f"{ROOT}\\Testlosses_d{d}_q{nq}_p{phase}_circ{circ}_its50_task{i+1}.npy")
    loss_arrays.append(losses)

#averaged_losses = np.sum(loss_arrays, axis = (0,1))/20
total = np.zeros((20,20))
for i in range(n):
    total = np.add(total, loss_arrays[i])
averaged_losses = total / n

#print(averaged_losses)
#print(np.size(averaged_losses))
title = f"{phase}_{nq}_{circ}_averaged.npy"
np.save(title, averaged_losses)

final_training_losses = []
training_losses = []
for i in range(n):
    trainloss = np.load(f"{ROOT}\\trainloss{circ}_d{d}_q{nq}_p{phase}_its70_task{i+1}.npy")
    #trainloss = np.load(f"{ROOT}\\trainloss_d{d}_q{nq}_p{phase}_circ{circ}_its50_task{i+1}.npy")
    finalloss = trainloss[-1]
    final_training_losses.append(finalloss)
    training_losses.append(trainloss)
#print(final_training_losses)
avg_final_loss = np.average(final_training_losses)

total2 = np.zeros((1,71))
#total2 = np.zeros((1,51))
for i in range(n):
    total2 = np.add(total2, training_losses[i])
avg_training_losses = total2 / n

print(np.size(avg_training_losses))
print("Average final loss: ", avg_final_loss)
shortloss = '%.*f' % (3, avg_final_loss)

title2 = f"{phase}_{nq}_{circ}_noisy_traininglosses.npy"
np.save(title2, avg_training_losses)

# NOTE: re-run the above code block a total of 4 times for both DA and Digital, noisy and noiseless data
# Then, move on to next part of plotting the 4 different convergence data (or just use the averaged filed provided in the Github)

# Plot for just phase data
# convergence plots
DA_training_noisy = np.load("zAFM_8_DA_noisy_traininglosses.npy")
D_training_noisy = np.load("zAFM_8_D_noisy_traininglosses.npy")

DA_training_noiseless = np.load("zAFM_8_DA_noiseless_traininglosses.npy")
D_training_noiseless = np.load("zAFM_8_D_noiseless_traininglosses.npy")



FONT_SIZE = 28
label_size = FONT_SIZE - 2


plt.rcParams["figure.figsize"] = [10, 6]
plt.rcParams["figure.autolayout"] = True

fig, ax1 = plt.subplots(1)

ax1.scatter(np.linspace(1,71,71), DA_training_noisy, label='DA', color='red')
ax1.scatter(np.linspace(1,71,71), D_training_noisy, label='Digital', color='blue')

ax1.tick_params(axis='x', labelsize=label_size)
ax1.tick_params(axis='y', labelsize=label_size)

#plt.title("Sharpness vs Depth \n Farther Atom Spacing")
ax1.legend(fontsize=label_size)


ax1.set_xlabel("Iteration", fontsize=FONT_SIZE)
ax1.set_ylabel("Training loss", fontsize=FONT_SIZE)

# Plotting phase and 3 vs 8 comparison data

3v8_ROOT = '.\'
D_3v8_noiseless = np.load(f"{3v8_ROOT}\\digital_loss_3v8_noiseless.npz")
D_3v8_noisy = np.load(f"{3v8_ROOT}\\digital_loss_3v8_noisy.npz")

DA_3v8_noisy = np.load(f"{3v8_ROOT}\\da_training_loss_3v8_0.87_depth_12_noisy.npz")
DA_3v8_noiseless = np.load(f"{3v8_ROOT}\\da_training_loss_3v8_depth_12_087_noiseless.npz")

FONT_SIZE = 28
label_size = FONT_SIZE - 2
plt.rcParams["figure.figsize"] = [9, 9]
plt.rcParams["figure.autolayout"] = True

fig, (ax1, ax2) = plt.subplots(2,1)

ax1.plot(np.linspace(1,71,71), D_3v8_noiseless['arr_0'], label='Digital', color='red')
ax1.plot(np.linspace(1,71,71), D_3v8_noisy['arr_0'], color='red', linestyle='dashed')
ax1.plot(np.linspace(1,71,71), DA_3v8_noiseless['arr_0'], label='DA', color='blue')
ax1.plot(np.linspace(1,71,71), DA_3v8_noisy['arr_0'], color='blue', linestyle='dashed')

ax2.plot(np.linspace(1,51,51), D_training_noiseless[0], color='red', label='Digital')
ax2.plot(np.linspace(1,71,71), D_training_noisy[0], color='red',linestyle='dashed')
ax2.plot(np.linspace(1,51,51), DA_training_noiseless[0], label='DA', color='blue')
ax2.plot(np.linspace(1,71,71), DA_training_noisy[0], color='blue',linestyle='dashed')


ax1.tick_params(axis='x', labelsize=label_size)
ax1.tick_params(axis='y', labelsize=label_size)
ax2.tick_params(axis='x', labelsize=label_size)
ax2.tick_params(axis='y', labelsize=label_size)

#plt.title("Sharpness vs Depth \n Farther Atom Spacing")
ax1.legend(fontsize=label_size-2)
ax2.legend(fontsize=label_size-2)


ax2.set_xlabel("Iteration", fontsize=FONT_SIZE)
ax1.set_ylabel("Training loss", fontsize=FONT_SIZE)
ax2.set_ylabel("Training loss", fontsize=FONT_SIZE)

for ax in (ax1, ax2):
    ax.label_outer()

fig.tight_layout(pad=10.0)
