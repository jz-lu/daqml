import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib
import scipy.io as sio
import matplotlib.ticker as tick
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
%matplotlib inline

# side by side plotting with True phase diagram

mesh = 45
D_over_o = np.linspace(0,4,mesh)
Rb_over_a = np.linspace(1,3.5,mesh)

FONT_SIZE = 22
label_size = FONT_SIZE-2

z2_avg_DA = np.load("Z2_13_averaged.npy")
ryd_true = np.load("ryd_true.npy")
ryd_rots = np.load("ryd_rots.npy")

z2_train_point = (2.5, 1.3538)
DO2_train_point = (0.6, 1.3)

plt.rcParams["figure.figsize"] = [15, 5]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['figure.dpi'] = 300

fig, (ax1, ax2, ax3) = plt.subplots(1,3)

# plotting
ax2.contourf(D_over_o, Rb_over_a, z2_avg_DA, levels = 501, cmap='Spectral')
ax2.plot(z2_train_point[0], z2_train_point[1], marker='^', markerfacecolor='lime', markersize=18, clip_on=False)
#ax1.set_title('Noisy DA')

ax1.contourf(D_over_o, Rb_over_a, ryd_true.T, levels=501, cmap='YlOrRd')
#ax2.pcolormesh(J_ratios, alphas, zafm_avg_D, cmap='Spectral')
#ax2.plot(z2_train_point[0], z2_train_point[1], marker='^', markerfacecolor='lime', markersize=10, clip_on=False)
#ax2.set_title('Noisy Digital')

ax3.contourf(D_over_o, Rb_over_a, ryd_rots, levels=501, cmap='Spectral')
ax3.plot(DO2_train_point[0], DO2_train_point[1], marker='^', markerfacecolor='lime', markersize=18, clip_on=False)

# axis labels

#ax1.set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)
#ax2.set_xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
#ax2.set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)


for ax in (ax1, ax2, ax3):
    ax.set_xlabel(r"$\Delta/\Omega$", fontsize=FONT_SIZE)
    ax.set_ylabel(r"$R_b/a$", fontsize=FONT_SIZE)

for ax in (ax1, ax2, ax3):
    ax.label_outer()


# setting axis ticks and label size
ax1.set_xticks([1,3])
ax2.set_xticks([1, 3])
ax3.set_xticks([1, 3])
ax1.set_yticks([1, 2, 3])
ax2.set_yticks([1, 2, 3])
ax3.set_yticks([1, 2, 3])
ax1.tick_params(axis='x', labelsize=label_size)
ax1.tick_params(axis='y', labelsize=label_size)
ax2.tick_params(axis='x', labelsize=label_size)
ax2.tick_params(axis='y', labelsize=label_size)
ax3.tick_params(axis='x', labelsize=label_size)
ax3.tick_params(axis='y', labelsize=label_size)

# making colorbars
clb2 = fig.colorbar(ax2.contourf(D_over_o, Rb_over_a, z2_avg_DA, levels=501, cmap='Spectral'), ax=ax2)
clb1 = fig.colorbar(ax1.contourf(D_over_o, Rb_over_a, ryd_true.T, levels=501, cmap='YlOrRd'), ax=ax1)
clb3 = fig.colorbar(ax3.contourf(D_over_o, Rb_over_a, ryd_rots, levels=501, cmap='Spectral'), ax=ax3)

# titling colorbars
clb1.ax.set_title(r'$\mathcal{S}$', fontsize=FONT_SIZE)
clb2.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)
clb3.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)

# formatting decimal places on colorbars
clb1.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))
clb2.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))
clb3.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))


# formatting number of ticks and tick label size of colorbars
clb2.ax.locator_params(nbins=4)
clb3.ax.locator_params(nbins=4)
clb1.set_ticks([0, 0.25, 0.5, 0.75])
clb1.ax.tick_params(labelsize=label_size) 
clb2.ax.tick_params(labelsize=label_size)
clb3.ax.tick_params(labelsize=label_size)

# labeling phases
ax1.text(2.75, 1.5, r"$\mathbb{Z}_2$", c='black', fontsize=FONT_SIZE+6)
ax1.text(2.75, 2.5, r"$\mathbb{Z}_3$", c='black', fontsize=FONT_SIZE+6)
ax1.text(2.75, 3.2, r"$\mathbb{Z}_4$", c='black', fontsize=FONT_SIZE+6)
