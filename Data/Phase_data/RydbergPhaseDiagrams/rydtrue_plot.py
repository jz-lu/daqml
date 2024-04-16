# Code for plotting true phase diagram (entanglement entropy plot) of 13 qubit Rydberg chain
# Imports
import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import pylatexenc
import qiskit 
print(qiskit.__version__)
from __class_net import QNet
from __constants import *
from qiskit.quantum_info import Statevector, partial_trace, entropy
from __constants import PARAM_PER_R
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
%matplotlib inline

nsites = 13
depth = 1
ROOT = './'

# Calculate the entanglement entropy
phase_grid = np.apply_along_axis(lambda x: x / LA.norm(x), -1, np.load(f'{ROOT}/test.npy'))
losses_phase = np.zeros(phase_grid.shape[:-1])
ee = np.zeros_like(losses_phase)

for i in range(phase_grid.shape[0]):
    for j in range(phase_grid.shape[1]):
        state = Statevector(phase_grid[i, j])
        dm = partial_trace(state, list(np.arange(nsites // 2)))
        ee[i, j] = entropy(dm)

title = "ryd_true.npy"
np.save(title, ee)

FONT_SIZE = 20
fig, ax = plt.subplots(figsize=(8,6))
plt.rc('font', size=16)
plt.xlabel(r"$\Delta/\Omega$", fontsize=FONT_SIZE)
plt.ylabel(r"$R_b/a$", fontsize=FONT_SIZE)
plt.xticks(fontsize=FONT_SIZE-2)
plt.yticks(fontsize=FONT_SIZE-2)
# plt.plot(train_point[0], train_point[1], marker='^', markerfacecolor='lime', markersize=10)
plt.text(4.3, 3.55, r'$S$', fontsize=FONT_SIZE)
plt.contourf(x, y, ee.T, levels=501, cmap='binary')
plt.title("True phase diagram", fontsize=FONT_SIZE)

plt.text(3.5, 1.5, r"$\mathbb{Z}_2$", c='white', fontsize=FONT_SIZE+6)
plt.text(3.5, 2.5, r"$\mathbb{Z}_3$", c='white', fontsize=FONT_SIZE+6)
plt.text(3.5, 3.2, r"$\mathbb{Z}_4$", c='white', fontsize=FONT_SIZE+6)

plt.tight_layout()
cbar = plt.colorbar()
cbar.set_ticks([0, 0.25, 0.5, 0.75])
plt.savefig(f"Chain_{nsites}_{depth}_True.jpg")

