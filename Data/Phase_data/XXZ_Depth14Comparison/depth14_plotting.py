import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib
import scipy.io as sio
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
%matplotlib inline

ROOT = ".\" # location at which noisy, depth 14 loss arrays are stored (both digital and DA)

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
d = 14
circ = "D" #also need to change this to DA
n = 20

# saving array of loss arrays
loss_arrays = []
for i in range(n):
    losses = np.load(f"{ROOT}\\Testlosses{circ}_d{d}_q{nq}_p{phase}_its70_task{i+1}.npy")
    loss_arrays.append(losses)

#averaged_losses = np.sum(loss_arrays, axis = (0,1))/20
total = np.zeros((20,20))
for i in range(n):
    total = np.add(total, loss_arrays[i])
averaged_losses = total / n

#print(averaged_losses)
#print(np.size(averaged_losses))
title = f"{phase}_{nq}_{circ}_{d}_averaged.npy"
np.save(title, averaged_losses)

final_training_losses = []
for i in range(n):
    trainloss = np.load(f"{ROOT}\\trainloss{circ}_d{d}_q{nq}_p{phase}_its70_task{i+1}.npy")
    finalloss = trainloss[-1]
    final_training_losses.append(finalloss)
print(final_training_losses)
avg_final_loss = np.average(final_training_losses)
print("Average final loss: ", avg_final_loss)
shortloss = '%.*f' % (3, avg_final_loss)

# PLOTTING ------------------------------------------------------------------------------------------------------
# plotting side by side

FONT_SIZE = 22
label_size = FONT_SIZE-2

zafm_avg_DA = np.load("zAFM_8_DA_14_averaged.npy")
zafm_avg_D = np.load("zAFM_8_D_14_averaged.npy")

zafm_train_point = (0.01, 0.2184)

plt.rcParams["figure.figsize"] = [6, 8]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.dpi"] = 300

fig, (ax1, ax2) = plt.subplots(2)

# plotting
ax1.contourf(J_ratios, alphas, zafm_avg_DA, levels = 501, cmap='Spectral')
ax1.plot(zafm_train_point[0], zafm_train_point[1], marker='^', markerfacecolor='lime', markersize=18, clip_on=False)
#ax1.set_title('Noisy DA')

ax2.contourf(J_ratios, alphas, zafm_avg_D, levels=501, cmap='Spectral')
#ax2.pcolormesh(J_ratios, alphas, zafm_avg_D, cmap='Spectral')
ax2.plot(zafm_train_point[0], zafm_train_point[1], marker='^', markerfacecolor='lime', markersize=18, clip_on=False)
#ax2.set_title('Noisy Digital')

# axis labels

#ax1.set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)
#ax2.set_xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
#ax2.set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)


for ax in (ax1, ax2):
    ax.set_xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
    ax.set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)

for ax in (ax1, ax2):
    ax.label_outer()


# setting axis ticks and label size
ax1.set_xticks([0.01,1,2])
ax1.set_xticklabels(["0","1","2"])
ax2.set_xticks([0.01,1, 2])
ax2.set_xticklabels(["0","1","2"])
ax1.set_yticks([0.2, 0.6, 1])
ax2.set_yticks([0.2, 0.6, 1])
ax1.tick_params(axis='x', labelsize=label_size)
ax1.tick_params(axis='y', labelsize=label_size)
ax2.tick_params(axis='x', labelsize=label_size)
ax2.tick_params(axis='y', labelsize=label_size)

# making colorbars
clb1 = fig.colorbar(ax1.contourf(J_ratios, alphas, zafm_avg_DA, levels=501, cmap='Spectral'), ax=ax1)
clb2 = fig.colorbar(ax2.contourf(J_ratios, alphas, zafm_avg_D, levels=501, cmap='Spectral'), ax=ax2)

# titling colorbars
clb1.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)
clb2.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)

# formatting decimal places on colorbars
clb1.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))
clb2.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))

# formatting number of ticks and tick label size of colorbars
clb1.ax.locator_params(nbins=4)
clb2.ax.locator_params(nbins=4)
clb1.ax.tick_params(labelsize=label_size) 
clb2.ax.tick_params(labelsize=label_size)

# NOTE: The variables "xafm_op" and "xafm_contour_value," etc. are defined in "op_plotting.py" (XXZOrderParameterPlots github folder)
# This code just overlays the contours from the XXZ order parameter plots to visually distinguish the phase boundaries
# This code may be commented out if these contours are not desired:

# plotting true PD contours
for ax in (ax1, ax2):
    CS1 = ax.contour(J_ratios, alphas, xafm_op['op_prime'], [xafm_contour_value], colors="blue", linestyles='dashed')
    CS2 = ax.contour(J_ratios, alphas, qzafm_op['op_prime'], [qzafm_contour_value], colors="green", linestyles='dashed')
    CS3 = ax.contour(J_ratios, alphas, zafm_op['op_prime'], [zafm_contour_value], colors="purple", linestyles='dashed')
    CS4 = ax.contour(J_ratios, alphas, vbs_op['op_prime'], [vbs_contour_value], colors="red", linestyles='dashed')

