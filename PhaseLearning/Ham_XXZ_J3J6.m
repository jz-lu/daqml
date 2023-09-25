function Ham=Ham_XXZ_J3J6(Lx, Alpha, J3, J6)
% Lx = x-length of chain
% Alpha = ratio between NN and NNN distances, cubed
% J3, J6 = strengths of spin-exchange interactions and Ising interactions for NN pairs
% a = distance between lattice sites

sx=[0,1;1,0]; % Pauli X matrix
sy=[0,-1i; 1i, 0]; % Pauli Y matrix
sz=[1,0;0,-1]; % Pauli Z matrix


N = Lx;
NoMax = N^2*(2^N); % maximum number of nonzero elements. Actual number may be much smaller
Ham=spalloc(2^N,2^N,NoMax); % preallocate a sparse matrix

% J3 term
for k=1:Lx - 1
    
    idx = k;
    % adding NN terms
    Ham = Ham + J3 * (kronSpin(N, idx, sx, idx + 1, sx) + kronSpin(N, idx, sy, idx +1, sy));

end  
% Adding the remaining sx(1)sx(N) term b.c. PBC's
Ham = Ham + J3 * (kronSpin(N, 1, sx, Lx, sx) + kronSpin(N, 1, sy, Lx, sy));

for k=1:Lx - 2
    
    idx = k;
    % adding NNN terms
    Ham = Ham + J3 * Alpha * (kronSpin(N, idx, sx, idx+2, sx) + kronSpin(N, idx, sy, idx+2, sy));

end  
% Adding the remaining 2 terms: sx(1)sx(N-1) and s(2)s(N)
Ham = Ham + J3 * Alpha * (kronSpin(N, 1, sx, Lx-1, sx) + kronSpin(N, 1, sy, Lx-1, sy));
Ham = Ham + J3 * Alpha * (kronSpin(N, 2, sx, Lx, sx) + kronSpin(N, 2, sy, Lx, sy));


% J6 term  
for k=1:Lx - 1
    
idx = k;
% adding NN terms
Ham = Ham + J6 * kronSpin(N, idx, sz, idx + 1, sz);

end  
% Adding the remaining sx(1)sx(N) term b.c. PBC's
Ham = Ham + J6 * kronSpin(N, 1, sz, Lx, sz);

for k=1:Lx - 2
    
    idx = k;
    % adding NNN terms
    Ham = Ham + J6 * Alpha^2* kronSpin(N, idx, sz, idx+2, sz);

end  
% Adding the remaining 2 terms: sx(1)sx(N-1) and s(2)s(N)
Ham = Ham + J6 * Alpha^2* kronSpin(N, 1, sz, Lx-1, sz);
Ham = Ham + J6 * Alpha^2* kronSpin(N, 2, sz, Lx, sz);
    
end 
    





