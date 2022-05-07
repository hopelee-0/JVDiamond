import numpy as np
import matplotlib.pyplot as plt

# PLE plotting script adapted from Shariar's Matlab script

# Import data from PLE files to temp
file = 'PLE_test_data.txt'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\'+file
PLE_x, PLE_y = np.loadtxt(path, unpack=True, skiprows=0)
lamb = 619.3914
c = 299792458

# plt.scatter(PLE_x_mhz, PLE_y, marker='.')
# plt.show()

diff_PLE_x = [PLE_x[i+1]-PLE_x[i] for i in range(len(PLE_x)-1)]
# print(diff_PLE_x)
zc_b = np.where(np.diff(np.sign(diff_PLE_x)))[0] # gives index of point right before crossing
zc_a = [i+1 for i in zc_b] # gives index after crossing

for previous, current in zip(zc_a, zc_a[1:]):
    print(previous, current)

cut_idx = [[0, zc_a[0]]]+[[i,j] for i,j in zip(zc_a, zc_a[1:])]

cut_x = [PLE_x[0:zc_a[0]]] + [PLE_x[i:j] for i,j in zip(zc_a, zc_a[1:])]
cut_y = [PLE_y[0:zc_a[0]]] + [PLE_y[i:j] for i,j in zip(zc_a, zc_a[1:])] # first section and iteratively add all other sections

for i,j,k in zip(cut_idx, cut_x, cut_y):
    print(i,j,k)
    if abs(i[0]-i[1]) <= 10:
        cut_x.remove(j)
        cut_y.remove(k)

count = 1
for i, j in zip(cut_x, cut_y): # plot check
    plt.plot(i,j, label=count)
    count += 1
plt.legend()
plt.show()

# Create stacked offset plots

y_height = max(cut_y[0])-min(cut_y[0])
cut_y_stacked = []
for i,j in zip(cut_y, range(len(cut_y))):
    i = [k+j*y_height/2 for k in i]
    cut_y_stacked.append(i)

count = 1
for i, j in zip(cut_x, cut_y_stacked): # plot check
    plt.plot(i,j, label=count)
    count += 1
plt.legend()
plt.show()




# # Calculte the PLE Spectra for multiple scans
# n = length(PLE_x)
#
# # Find edges of the scans
# x = movmean(diff(PLE_x),10)
# zcd = dsp.ZeroCrossingDetector;     # Create zero crossing detector --> will need to find out for python!
# zcdOut = zcd(movmean(diff(PLE_x),10))   # Number of zero crossings
# % figure
# % plot(x)
# % figure
# % plot(PLE_x)
#
# % For single scans
# if zcdOut ==0
#     hold on
#     plot(PLE_x_mhz,PLE_y)
# else
#
# # upward zero-crossings to nearest time step
# upcross = find(x(1:end-1) <= 0 & x(2:end) > 0);
# # interpolate
# upcross = round(upcross - x(upcross) ./ (x(upcross+1)-x(upcross)));
# # downward zero-crossings
# downcross = find(x(1:end-1) >= 0 & x(2:end) < 0);
# downcross = round(downcross - x(downcross) ./ (x(downcross+1)-x(downcross)));
# cross = sort([downcross;upcross]);
# # plotting all the scans
#  figure
#  plot(PLE_x_mhz(1:cross(1)),PLE_y(1:cross(1)))
# for (k=1:zcdOut-1)
#  hold on
#  plot(PLE_x_mhz(cross(k):cross(k+1)),double(k)*3000 +PLE_y(cross(k):cross(k+1)))
# end
#  hold on
#  plot(PLE_x_mhz(cross(zcdOut):end),double(zcdOut)*3000+PLE_y(cross(zcdOut):end))
#
# # plotting a heatmap of the data
# figure
# xMat = repmat(PLE_x_mhz(1:cross(1)),1,2);
# zMat = repmat(PLE_y(1:cross(1)),1,2);
# yMat = 0.5*scan_length*[zeros(length(xMat),1),ones(length(xMat),1)];
# h = surf(xMat,yMat,zMat); view(0,90)
# set(h, 'edgecolor','none')
# for (k=1:zcdOut-1)
# hold on
# xMat = repmat(PLE_x_mhz(cross(k):cross(k+1)),1,2);
# zMat = repmat(PLE_y(cross(k):cross(k+1)),1,2);
# yMat = 0.5*scan_length*[double(k)*ones(length(xMat),1),double(k+1)*ones(length(xMat),1)];
# h = surf(xMat,yMat,zMat); view(0,90)
# set(h, 'edgecolor','none')
# end
# xMat = repmat(PLE_x_mhz(cross(zcdOut):end),1,2);
# zMat = repmat(PLE_y(cross(zcdOut):end),1,2);
# yMat = 0.5*scan_length*[double(zcdOut)*ones(length(xMat),1),double(zcdOut+1)*ones(length(xMat),1)];
# h = surf(xMat,yMat,zMat); view(0,90)
# set(h, 'edgecolor','none')
# colormap magma
# view(0,90)
# caxis([0,15000])
# set(gca,'FontName','Helvetica')
# set(gca,'FontSize',16)
# xlim ([-2000,2000])
# %ylim ([-32,0])
# xlabel ('Detuning (MHz)','fontsize',16 )
# ylabel ('Time (s)','fontsize',16)
#
# %%%% Plotting the average linewidth in MHz
# N = 2412;   % Index of the desired peak (obtain from plotting the PLE_y alone)
# % figure
# % plot(PLE_x_mhz,PLE_y)
#
# %%% Binning data for histogram purposes
# num_bins = 100;
# x_bins = linspace(min(PLE_x_mhz),max(PLE_x_mhz), num_bins)';
# PLE_y_binned = zeros(num_bins,1);
# occ_bins = zeros(num_bins,1); %% occupancy of each bin
# for k = 1:num_bins-1
#     for f = 1: n
#         if x_bins (k)<= PLE_x_mhz(f) && PLE_x_mhz(f)< x_bins(k+1)
#         PLE_y_binned (k) = PLE_y_binned (k)+ PLE_y(f);
#         occ_bins (k) = occ_bins (k)+1;
#         end
#     end
# end
# figure
# PLE_y_binned = PLE_y_binned./occ_bins;
# plot(x_bins,PLE_y_binned)
# xlabel ('Detunning (MHz)','fontsize',16 )
# ylabel ('Binned Counts (arb. units)','fontsize',16)
