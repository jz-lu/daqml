%Jratios = linspace(0,2.5,10);
%alphas = linspace(0,1,10);

close all
%plotting for specific q6 m20 mesh
nx = 20;
ny = 20;
Lx = 8;
Jratios = linspace(0.01,2.5,nx);
alphas = linspace(0.01,1,ny);
[X,Y] = meshgrid(Jratios,alphas);

op = zeros(length(Jratios),length(alphas));

for i = 1:length(Jratios)
    for j = 1:length(alphas)
        op(i,j) = getXAFM(Jratios(i),1,alphas(j),Lx);
    end
end


figure
%contourf(X,Y,op',20)

imagesc(Jratios,alphas,op',[0 3])
axis xy 
hold on

f = 0.5; %percentile in the range of op vals I am selecting for contour line
op_sorted = sort(op(:)); % sort in increasing order
num_elems = numel(op_sorted);
index = round(f * num_elems); % index corr to f percentile element of sorted array
contour_value = op_sorted(index);
disp(contour_value)

M = contour(Jratios, alphas, op',[contour_value contour_value], 'color', [1 1 1], 'linewidth', 2, 'linestyle', '-');
npoint = M(2,1); % number of points in contour line
xafm_contour_xvals = M(1,2: (npoint + 1)); % saving x values
xafm_contour_yvals = M(2,2: (npoint + 1)); % saving y values

folder = 'C:\Users\Kristina\Desktop\QML';
filename = [folder '\' 'xafm_contour.mat'];
save(filename, 'xafm_contour_xvals', 'xafm_contour_yvals');

op_filename = [folder '\' 'xafm_op.mat'];
op_prime = op';
save(op_filename, 'op_prime');

colorbar
title(sprintf('xafm order parameter %d-qubit mesh', Lx))
xlabel('J3/J6') 
ylabel('alpha') 