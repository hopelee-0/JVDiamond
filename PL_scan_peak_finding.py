import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max

file = '20220413_R1D4_532nm_ZPLCollect_SM_3.kns'
path = 'C:\\Users\\hopel\\Documents\\Data\\20220411\\'+file

save_name = "20220414_R1D4_PLConfocal_ID_3" # no extension since added later
save_path = 'C:\\Users\\hopel\\Documents\\\Data\\20220411\\'+save_name

save_bool = 1
rotate = 0
confocal_show = 1
colorbar_bool = 0

# peak finding parameters
min_distance = 5 #enforces minimum pixel distance between two identified peaks
threshold_factor = 3 #multiplied with the mean of the confocal to set the threshold

# coordinate transformation parameters
x_min = -4.
y_min = -2.75
x_step = 0.005
y_step = 0.005

# load data
confocal = np.loadtxt(path)

# rotate PL figure if desired
if rotate == 1:
    confocal = np.rot90(confocal)

# show raw PL confocal scan
if confocal_show == 1:
    plot = plt.figure(figsize=(10,10))
    plt.imshow(confocal)
    ax=plt.gca()
    ax.invert_yaxis()
    if colorbar_bool == 1:
        if rotate == 1:
            cbar = plt.colorbar(orientation='horizontal')
            cbar.formatter.set_powerlimits((0, 0))
        else:
            cbar = plt.colorbar()
            cbar.formatter.set_powerlimits((0, 0))
    plt.show()

# #applying the detection and plotting results
detected_peaks = peak_local_max(confocal, min_distance=min_distance, threshold_abs=threshold_factor*np.mean(confocal))
peak_x, peak_y = detected_peaks.T

plt.figure(figsize=(10,10))
plt.imshow(confocal)
ax=plt.gca()
ax.invert_yaxis()
if rotate == 1:
    if colorbar_bool == 1:
        cbar = plt.colorbar(orientation='horizontal')
        cbar.formatter.set_powerlimits((0, 0))
else:
    if colorbar_bool == 1:
        cbar = plt.colorbar()
        cbar.formatter.set_powerlimits((0, 0))
plt.scatter(peak_y, peak_x, marker='.', c='r')
if save_bool == 1:
    plt.savefig(save_path+'.png')
plt.show()

# produce data file with all coordinates, need to convert from pixel location --> need a way to automatically grab this info
if save_bool == 1:
    f = open(save_path+"_meta.txt", "w")
    f.write(file+'\n')
    f.write("Minimum distance:{}\n".format(min_distance))
    f.write("Threshold factor:{}\n".format(threshold_factor))
    f.close()
    f = open(save_path+".txt", "w")
    for i, j in zip(peak_x, peak_y):
        x_coord = x_min+j*x_step
        y_coord = y_min+i*y_step
        f.write("{:.2f},{:.2f}\n".format(x_coord, y_coord))

print(len(peak_x))
