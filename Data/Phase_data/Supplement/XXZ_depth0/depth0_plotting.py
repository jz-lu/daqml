import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib
import scipy.io as sio
import matplotlib.ticker as tick
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
%matplotlib inline

ROOT = ".\" # location where depth 0 files are stored

mesh = 20
J_ratios = np.linspace(0.01,2.5,mesh)
alphas = np.linspace(0.01,1,mesh)
phase = "xy"
if phase == "zAFM":
    train_point = (0.01, 0.2184)

if phase == "xy":
    train_point = (1.8447, 0.1663)

nq = 8
d = 1
circ = "rots" # rots = rotations only circuit
n = 20

# saving array of loss arrays
loss_arrays = []
for i in range(n):
    losses = np.load(f"{ROOT}\\Testlosses_d{d}_q{nq}_pzafm_circ{circ}_its50_task{i+1}.npy")
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
for i in range(n):
    trainloss = np.load(f"{ROOT}\\trainloss_d{d}_q{nq}_pzafm_circ{circ}_its50_task{i+1}.npy")
    finalloss = trainloss[-1]
    final_training_losses.append(finalloss)
print(final_training_losses)
avg_final_loss = np.average(final_training_losses)
print("Average final loss: ", avg_final_loss)
shortloss = '%.*f' % (3, avg_final_loss)

xy_train_point = (1.8447, 0.1663)

# PLOTTING -----------------------------------------------------------
# formatting rots plot 

xy_rots = np.load("xy_8_rots_averaged.npy")

# plotting side by side

FONT_SIZE = 22
label_size = FONT_SIZE-2

zafm_train_point = (0.01, 0.2184)

plt.rcParams["figure.figsize"] = [8, 6]
plt.rcParams["figure.autolayout"] = True


fig, ax1 = plt.subplots(1)

# plotting
ax1.contourf(J_ratios, alphas, xy_rots, levels = 501, cmap='Spectral')
ax1.plot(xy_train_point[0], xy_train_point[1], marker='^', markerfacecolor='lime', markersize=18, clip_on=False)
#ax1.set_title('Noisy DA')

ax1.set_xlabel(r"$J_3/J_6$", fontsize=FONT_SIZE)
ax1.set_ylabel(r"$\alpha$", fontsize=FONT_SIZE)



# setting axis ticks and label size
ax1.set_xticks([1,2])

ax1.set_yticks([0.2, 0.6, 1])

ax1.tick_params(axis='x', labelsize=label_size)
ax1.tick_params(axis='y', labelsize=label_size)


# making colorbars
clb1 = fig.colorbar(ax1.contourf(J_ratios, alphas, xy_rots, levels=501, cmap='Spectral', vmin=0.45, vmax=0.55), ax=ax1)


# titling colorbars
clb1.ax.set_title(r'$\mathcal{L}$', fontsize=FONT_SIZE)

# formatting decimal places on colorbars
clb1.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))

# formatting number of ticks and tick label size of colorbars
clb1.ax.locator_params(nbins=4)
clb1.ax.tick_params(labelsize=label_size)
