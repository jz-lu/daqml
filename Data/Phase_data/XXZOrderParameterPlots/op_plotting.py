import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib
import scipy.io as sio
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
%matplotlib inline

# Uploading raw data files
True_root = ".\"

xafm_op = sio.loadmat(f"{True_root}\\xafm_op.mat")
qzafm_op = sio.loadmat(f"{True_root}\\qzafm_op.mat")
zafm_op = sio.loadmat(f"{True_root}\\zafm_op.mat")
vbs_op = sio.loadmat(f"{True_root}\\vbs_op.mat")


# getting phase contour lines

xafm_fill = 0.5
xafm_op_reshaped = xafm_op['op_prime'].reshape(1,400)
# converting reshaped array to list for sorting
xafm_op_list = xafm_op_reshaped[0].tolist()

xafm_op_list.sort()
#print(xafm_op_list)
num_xafm = len(xafm_op_list)
xafm_index = round(xafm_fill * num_xafm) # index corr to xafm_fill percentile element of sorted array
xafm_contour_value = xafm_op_list[xafm_index];

#ZAFM
zafm_fill = 0.91
zafm_op_reshaped = zafm_op['op_prime'].reshape(1,400)
# converting reshaped array to list for sorting
zafm_op_list = zafm_op_reshaped[0].tolist()

zafm_op_list.sort()
#print(xafm_op_list)
num_zafm = len(zafm_op_list)
zafm_index = round(zafm_fill * num_zafm) # index corr to zafm_fill percentile element of sorted array
zafm_contour_value = zafm_op_list[zafm_index];

#vbs
vbs_fill = 0.82
vbs_op_reshaped = vbs_op['op_prime'].reshape(1,400)
# converting reshaped array to list for sorting
vbs_op_list = vbs_op_reshaped[0].tolist()

vbs_op_list.sort()
#print(xafm_op_list)
num_vbs = len(vbs_op_list)
vbs_index = round(vbs_fill * num_vbs) # index corr to zafm_fill percentile element of sorted array
vbs_contour_value = vbs_op_list[vbs_index];

#qZAFM
qzafm_fill = 0.97
qzafm_op_reshaped = qzafm_op['op_prime'].reshape(1,400)
# converting reshaped array to list for sorting
qzafm_op_list = qzafm_op_reshaped[0].tolist()

qzafm_op_list.sort()
#print(xafm_op_list)
num_qzafm = len(qzafm_op_list)
qzafm_index = round(qzafm_fill * num_qzafm) # index corr to zafm_fill percentile element of sorted array
qzafm_contour_value = qzafm_op_list[qzafm_index];

FONT_SIZE = 22
label_size = FONT_SIZE - 2


#PLOTTING

#-------


plt.rcParams["figure.figsize"] = [10, 8]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.dpi"] = 300

fig, axs = plt.subplots(2, 2)

#fig.suptitle("test")

plt.rc('font', size=16)
im1 = axs[1, 0].contourf(J_ratios, alphas, xafm_op['op_prime'], levels=501, cmap='Spectral')
#axs[0, 0].set_title('xAFM')

axs[0, 1].contourf(J_ratios, alphas, qzafm_op['op_prime'], levels=501, cmap='Spectral')
#axs[0, 1].set_title('qzAFM')

axs[0, 0].contourf(J_ratios, alphas, zafm_op['op_prime'], levels=501, cmap='Spectral')
#axs[1, 0].set_title('zAFM')

axs[1, 1].contourf(J_ratios, alphas, vbs_op['op_prime'], levels=501, cmap='Spectral')
#axs[1, 1].set_title('VBS')

#print(xafm_op['op_prime'])
#plt.text(-2,2, r'$\mathcal{O}_{xAFM}$', fontsize=FONT_SIZE)
#plt.contourf(J_ratios, alphas, xafm_op['op_prime'], levels=501, cmap='Spectral')

for ax in axs.flat:
    ax.set_xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
    ax.set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)

for ax in axs.flat:
    ax.label_outer()

#axs[0,0].xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
#axs[0,0].ylabel(r"$\alpha$", fontsize=FONT_SIZE)

import matplotlib.ticker as tick
# setting axis ticks and label size
for ax in axs.flat:
    ax.set_xticks([0.01,1,2])
    ax.set_xticklabels(["0","1","2"])
    ax.set_yticks([0.2, 0.6, 1])
    ax.tick_params(axis='x', labelsize=label_size)
    ax.tick_params(axis='y', labelsize=label_size)

clb1 = fig.colorbar(axs[1, 0].contourf(J_ratios, alphas, xafm_op['op_prime'], levels=501, cmap='YlOrRd'), ax=axs[1,0])
clb2 = fig.colorbar(axs[0, 1].contourf(J_ratios, alphas, qzafm_op['op_prime'], levels=501, cmap='YlOrRd'), ax=axs[0,1])
clb3 = fig.colorbar(axs[0, 0].contourf(J_ratios, alphas, zafm_op['op_prime'], levels=501, cmap='YlOrRd'), ax=axs[0,0])
clb4 = fig.colorbar(axs[1, 1].contourf(J_ratios, alphas, vbs_op['op_prime'], levels=501, cmap='YlOrRd'), ax=axs[1,1])

clb1.ax.set_title(r'$\mathcal{O}_{xAFM}$', fontsize=FONT_SIZE)
clb2.ax.set_title(r'$\mathcal{O}_{qzAFM}$', fontsize=FONT_SIZE)
clb3.ax.set_title(r'$\mathcal{O}_{zAFM}$', fontsize=FONT_SIZE)
clb4.ax.set_title(r'$\mathcal{O}_{VBS}$', fontsize=FONT_SIZE)

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

CS1 = axs[1,0].contour(J_ratios, alphas, xafm_op['op_prime'], [xafm_contour_value], colors="blue", linestyles='dashed')
CS2 = axs[0,1].contour(J_ratios, alphas, qzafm_op['op_prime'], [qzafm_contour_value], colors="green", linestyles='dashed')
CS3 = axs[0,0].contour(J_ratios, alphas, zafm_op['op_prime'], [zafm_contour_value], colors="purple", linestyles='dashed')
CS4 = axs[1,1].contour(J_ratios, alphas, vbs_op['op_prime'], [vbs_contour_value], colors="black", linestyles='dashed')


# labeling phases
axs[1,0].text(1.3, 0.2, r"$\mathrm{xAFM}$", c='white', fontsize=FONT_SIZE+2)
axs[0,1].text(1, 0.7, "qzAFM", c='black', fontsize=FONT_SIZE+2)
axs[0,0].text(1, 0.2, "zAFM", c='black', fontsize=FONT_SIZE+2)
axs[1,1].text(1.3, 0.64, "VBS", c='white', fontsize=FONT_SIZE+2)
