import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib
import scipy.io as sio
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
%matplotlib inline

ROOT = ".\"

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

nq = 8 #10
d = 2
circ = "DA"
n = 20

# saving array of loss arrays 
loss_arrays = []
for i in range(n):
    losses = np.load(f"{ROOT}\\Testlosses_d{d}_q{nq}_p{phase}_circ{circ}_its50_task{i+1}.npy")
    loss_arrays.append(losses)

#averaged_losses = np.sum(loss_arrays, axis = (0,1))/20
total = np.zeros((20,20))
for i in range(n):
    total = np.add(total, loss_arrays[i])
averaged_losses = total / n

#print(averaged_losses)
#print(np.size(averaged_losses))
title = f"{phase}_{nq}_averaged.npy"
np.save(title, averaged_losses)

final_training_losses = []
for i in range(n):
    trainloss = np.load(f"{ROOT}\\trainloss_d{d}_q{nq}_p{phase}_circ{circ}_its50_task{i+1}.npy")
    finalloss = trainloss[-1]
    final_training_losses.append(finalloss)
print(final_training_losses)
avg_final_loss = np.average(final_training_losses)
print("Average final loss: ", avg_final_loss)
shortloss = '%.*f' % (3, avg_final_loss)

# Setting plotting parameters
FONT_SIZE=20
label_size = FONT_SIZE - 2
FONT_SIZE = 22

qz_avg = np.load("qz_8_averaged.npy")
zafm_avg = np.load("zAFM_8_averaged.npy")
vbs_avg = np.load("vbs_8_averaged.npy")
xy_avg = np.load("xy_8_averaged.npy")

zafm_train_point = (0.01, 0.2184)
qz_train_point = (0.01, 0.9479)
vbs_train_point = (1.5826, 0.6353)
xy_train_point = (1.8447, 0.1663)


plt.rcParams["figure.figsize"] = [10, 8]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.dpi"] = 300

fig, axs = plt.subplots(2, 2)

#plotting

plt.rc('font', size=16)
im1 = axs[1, 0].contourf(J_ratios, alphas, xy_avg, levels=501, cmap='Spectral')
axs[1,0].plot(xy_train_point[0], xy_train_point[1], marker='^', markerfacecolor='lime', markersize=18)
#axs[0, 0].set_title('XY-QLRO')


axs[0, 1].contourf(J_ratios, alphas, qz_avg, levels=501, cmap='Spectral')
axs[0,1].plot(qz_train_point[0], qz_train_point[1], marker='^', markerfacecolor='lime', markersize=18, clip_on=False)
#axs[0, 1].set_title('qzAFM')

axs[0, 0].contourf(J_ratios, alphas, zafm_avg, levels=501, cmap='Spectral')
axs[0,0].plot(zafm_train_point[0], zafm_train_point[1], marker='^', markerfacecolor='lime', markersize=18, clip_on = False)
#axs[1, 0].set_title('zAFM')

axs[1, 1].contourf(J_ratios, alphas, vbs_avg, levels=501, cmap='Spectral')
axs[1,1].plot(vbs_train_point[0], vbs_train_point[1], marker='^', markerfacecolor='lime', markersize=18)
#axs[1, 1].set_title('VBS')

# labeing axes
'''
axs[1,0].set_xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
axs[1,1].set_xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
axs[0,0].set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)
axs[1,0].set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)
'''

for ax in axs.flat:
    ax.set_xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
    ax.set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)

for ax in axs.flat:
    ax.label_outer()

import matplotlib.ticker as tick

# setting axis ticks and label size
for ax in axs.flat:
    ax.set_xticks([0.01,1,2])
    ax.set_xticklabels(["0","1","2"])
    ax.set_yticks([0.2, 0.6, 1])
    ax.tick_params(axis='x', labelsize=label_size)
    ax.tick_params(axis='y', labelsize=label_size)

# making colorbars
clb1 = fig.colorbar(axs[1, 0].contourf(J_ratios, alphas, xy_avg, levels=501, cmap='Spectral'), ax=axs[1,0])
clb2 = fig.colorbar(axs[0, 1].contourf(J_ratios, alphas, qz_avg, levels=501, cmap='Spectral'), ax=axs[0,1])
clb3 = fig.colorbar(axs[0, 0].contourf(J_ratios, alphas, zafm_avg, levels=501, cmap='Spectral'), ax=axs[0,0])
clb4 = fig.colorbar(axs[1, 1].contourf(J_ratios, alphas, vbs_avg, levels=501, cmap='Spectral'), ax=axs[1,1])

clb1.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)
clb2.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)
clb3.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)
clb4.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)


clb1.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))
clb2.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))
clb3.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))
clb4.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))

# formatting number of ticks and tick label size of colorbars
clb1.ax.locator_params(nbins=4)
clb2.ax.locator_params(nbins=4)
clb3.ax.locator_params(nbins=4)
clb4.ax.locator_params(nbins=4)
clb1.ax.tick_params(labelsize=label_size) 
clb2.ax.tick_params(labelsize=label_size)
clb3.ax.tick_params(labelsize=label_size) 
clb4.ax.tick_params(labelsize=label_size)

# NOTE: The variables "xafm_op" and "xafm_contour_value," etc. are defined in "op_plotting.py" (XXZOrderParameterPlots github folder)
# This code just overlays the contours from the XXZ order parameter plots to visually distinguish the phase boundaries
# This code may be commented out if these contours are not desired
for ax in axs.flat:
    CS1 = ax.contour(J_ratios, alphas, xafm_op['op_prime'], [xafm_contour_value], colors="blue", linestyles='dashed')
    CS2 = ax.contour(J_ratios, alphas, qzafm_op['op_prime'], [qzafm_contour_value], colors="green", linestyles='dashed')
    CS3 = ax.contour(J_ratios, alphas, zafm_op['op_prime'], [zafm_contour_value], colors="purple", linestyles='dashed')
    CS4 = ax.contour(J_ratios, alphas, vbs_op['op_prime'], [vbs_contour_value], colors="black", linestyles='dashed')

