function op = getOVBS(J3,J6,Alpha,Lx)
    
    sx=[0,1;1,0]; % Pauli X matrix
    sy=[0, -1i; 1i, 0]; % Pauli Y matrix
    sz=[1,0;0,-1]; % Pauli Z matrix

    % Defining Hamiltonian with these parameters
    h = Ham_XXZ_J3J6(Lx, Alpha, J3, J6); %Lx = 16 always
    opts.p = 60;
    [v, d] = eigs(h, 2, 'smallestreal', opts);
    ground_state = v(:,1); % ground state of this Hamiltonian
    
    % calculating VBS order parameter 
    order_param = 0;
    %%central_term = kronSpin(Lx, 2, sx, 3, sx) - kronSpin(Lx, 1, sx, 2, sx);
    % NEW version with all terms
    central_term = (kronSpin(Lx, 2, sx, 3, sx) + kronSpin(Lx, 2, sy, 3, sy) + kronSpin(Lx, 2, sz, 3, sz) - kronSpin(Lx, 1, sx, 2, sx) - kronSpin(Lx, 1, sy, 2, sy)- kronSpin(Lx, 1, sz, 2, sz));
        
    for i = 1:Lx
        if i == 1
            middle_term = (kronSpin(Lx, i, sx, i+1, sx)+kronSpin(Lx, i, sy, i+1, sy)+kronSpin(Lx, i, sz, i+1, sz)-kronSpin(Lx, i, sx, Lx, sx)-kronSpin(Lx, i, sy, Lx, sy)-kronSpin(Lx, i, sz, Lx, sz));
            %middle_term = (kronSpin(Lx, i, sx, i+1, sx)-kronSpin(Lx, i, sx, Lx, sx));
            correlator = ground_state.' * central_term * middle_term *ground_state;
            order_param = order_param + exp(1i*pi*i)*correlator;
        elseif i == Lx
            middle_term=(kronSpin(Lx, 1, sx, Lx, sx)+kronSpin(Lx, 1, sy, Lx, sy)+kronSpin(Lx, 1, sz, Lx, sz)-kronSpin(Lx, i-1, sx, i, sx)-kronSpin(Lx, i-1, sy, i, sy)-kronSpin(Lx, i-1, sz, i, sz));
            %middle_term=(kronSpin(Lx, 1, sx, Lx, sx)-kronSpin(Lx, i-1, sx, i, sx));
            correlator = ground_state.' * central_term * middle_term *ground_state;
            order_param = order_param + exp(1i*pi*i)*correlator; 
        end
        % If not near the beginning or end of the chain, no need for special cases
        if i > 1 && i < Lx
            middle_term = (kronSpin(Lx, i, sx, i+1, sx)+kronSpin(Lx, i, sy, i+1, sy)+kronSpin(Lx, i, sz, i+1, sz)-kronSpin(Lx, i-1, sx, i, sx)-kronSpin(Lx, i-1, sy, i, sy)-kronSpin(Lx, i-1, sz, i, sz));
            %middle_term = (kronSpin(Lx, i, sx, i+1, sx)-kronSpin(Lx, i-1, sx, i, sx));
            correlator = ground_state.' * central_term * middle_term *ground_state;
            order_param = order_param + exp(1i*pi*i)*correlator;
        end
    
    end
    
    op = abs(order_param);
    %op = imag(order_param);
end