% Choose parameters
Lx = 8; % System size (number of qubits)
% Defining a training point in the zAFM phase
J3 = 1.8447; % J3 parameter for testing vector
J6 = 1; % J6 parameter for testing vector
Alpha = 0.1663; % Alpha parameter for testing vector
mesh = 20; % For bookkeeping purposes, record what testing mesh size this training vector falls in


N = Lx;
ops.p = 50; % large number of basis vectors for eigensolver

h = Ham_XXZ_J3J6(Lx, Alpha, J3, J6); % Defining Hamiltonian
[v, d] = eigs(h, 6, 'smallestreal', ops); % Calculating eigenvectors and values

gs = v(:,1); % Saving first eigenvector as ground state "gs"

title = sprintf('zAFMtrain_m%d_q%d_J%.4f_a%.4f.mat',mesh,Lx,J3,Alpha);

save(title, "gs", '-v7')



