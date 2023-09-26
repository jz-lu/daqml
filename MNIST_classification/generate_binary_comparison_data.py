# this file generates data for all digit combinations. 
# this file can be run and the data can be used for the single comparisons as well

import numpy as np
import os
import numpy.linalg as LA
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector
import matplotlib
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from itertools import combinations

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'

def mkdir_p(dir):
    '''make a directory (dir) if it doesn't exist'''
    if not os.path.exists(dir):
        os.mkdir(dir)

def PCA_to_state(L, vals):
    if huge:
        vals = vals / LA.norm(vals)
        return Statevector(vals)
    # np.random.shuffle(vals) # scramble principal components
    thetas = vals[:L] - np.min(vals[:L])
    phis = vals[L:] - np.min(vals[L:])
    thetas = thetas / np.max(thetas) * np.pi
    phis = phis / np.max(phis) * np.pi
    states = [Statevector([np.cos(theta/2), np.exp(1j * phi) * np.sin(theta/2)]) for theta, phi in zip(thetas, phis)]
    final_state = states[0]
    for state in states[1:]:
        final_state = final_state.tensor(state)
    return final_state
    
ROOT = "../../MNIST_collection"
mkdir_p(ROOT)


"""Learning parameters"""
TRAIN_SZ = 1000
TEST_SZ = 200
huge = False

"""Import the MNIST dataset"""
mnist = fetch_openml('mnist_784')

index_number= np.random.permutation(70000)
x1, y1 = mnist.data.loc[index_number], mnist.target.loc[index_number]
x1.reset_index(drop=True,inplace=True)
y1.reset_index(drop=True,inplace=True)
y1 = np.array(list(map(int, y1.to_numpy())))

combos = list(combinations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2))
for combination in combos:
    idxs = (y1 == 1) + (y1 == 9)
    x1 = x1[idxs]; y1 = y1[idxs]
    y1_temp = [[0,0] for _ in range(len(y1))]
    for i in range(len(y1)):
        y1_temp[i] = [1.0, 0.0] if y1[i] == 1 else [0.0, 1.0]
    y1 = np.array(y1_temp)

    x_train , x_test = x1[:TRAIN_SZ], x1[TRAIN_SZ:TRAIN_SZ+TEST_SZ]
    y_train , y_test = y1[:TRAIN_SZ], y1[TRAIN_SZ:TRAIN_SZ+TEST_SZ]

    L = 8
    pca = PCA(n_components=2**L if huge else 2*L)
    reduced_train = pca.fit_transform(x_train)
    reduced_test = pca.transform(x_test)
    print(reduced_train.shape)

    mypca = PCA(n_components=20)
    mypca.fit(x_train)
    # plt.plot(mypca.explained_variance_ratio_ * 100)
    train_states = np.array([PCA_to_state(L, vals) for vals in reduced_train])
    test_states = np.array([PCA_to_state(L, vals) for vals in reduced_test])
    # print(train_states.shape)

    file_ext = f"{combination[0]}_{combination[1]}_MNIST_data"
    full_ext = os.path.join(ROOT, file_ext)
    mkdir_p(full_ext)

    hh = "huge_" if huge else ""
    np.save(f"{full_ext}/{hh}x_{combination[0]}_{combination[1]}_train.npy", train_states)
    np.save(f"{full_ext}/{hh}y_{combination[0]}_{combination[1]}train.npy", y_train)
    np.save(f"{full_ext}/{hh}x_{combination[0]}_{combination[1]}test.npy", test_states)
    np.save(f"{full_ext}/{hh}y_{combination[0]}_{combination[1]}test.npy", y_test)
    print("Done")