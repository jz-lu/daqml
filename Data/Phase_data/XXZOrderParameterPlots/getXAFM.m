function op = getXAFM(J3,J6,Alpha,Lx)
    
    sx=[0,1;1,0]; % Pauli X matrix

    % Defining Hamiltonian with these parameters
    h = Ham_XXZ_J3J6(Lx, Alpha, J3, J6); %Lx = 16 always
    opts.p = 60;
    [v, d] = eigs(h, 2, 'smallestreal', opts);
    ground_state = v(:,1); % ground state of this Hamiltonian
    
    % calculating zAFM order parameter 
    order_param = 0;
    for i = 1:Lx
        if i == 1
            correlator = ground_state.' * kronSpin(Lx, 1, sx, 2, sx) * ground_state;
            order_param = order_param + exp(1i*pi*i)*correlator; %i = r-value
        elseif i == 2
            correlator = ground_state.' * kronSpin(Lx, 2, sx) * ground_state;
            order_param = order_param + exp(1i*pi*i)*correlator;
        elseif i > 2
            correlator = ground_state.' * kronSpin(Lx, 2, sx, i, sx) * ground_state;
            order_param = order_param + exp(1i*pi*i)*correlator;
        end
    end
    
    op = abs(order_param);
    %op = imag(order_param);
end