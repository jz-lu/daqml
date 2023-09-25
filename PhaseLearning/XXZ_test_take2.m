% making parameter mesh
nx = 20;
ny = 20;
J_ratios = linspace(0.01,2.5,nx);
alphas = linspace(0.01,1,ny);
Lx = 6; % System size (number of qubits)


gss = zeros([nx, ny, 2^Lx]); % Matrix of zeros where testing mesh will be saved
ops.p =16; % large number of basis vectors for eigensolver

% Filling gss with nx x ny ground states of the XXZ Hamiltonian
for i = 1:nx
    for j = 1:ny
        alpha = alphas(j); J = J_ratios(i); % setting parameters
        h = Ham_XXZ_J3J6(Lx, alpha, J, 1); % generating Hamiltonian with said parameters
        [v, d] = eigs(h, 1, 'smallestreal', ops); % solving eigensystem
        gss(i, j, :) = v(:,1); % placing this eigenvector as (i,j)th element of gss
        disp([i, j])
    end
end

title = sprintf('XXZtest%d_by_%d_nq%dtake3.mat',nx,ny,Lx);

fpath = 'C:/Users/Kristina/Desktop/QML/Qubit variation/test_meshes';
save(title, "gss", '-v7')