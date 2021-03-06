import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max

file = 'J15_ZPL'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220729_EZ01\\"

save_name = "J15_ZPL" # no extension since added later
save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220729_EZ01\\'+save_name

plot_title = "J15 ZPL Scan"

save_bool = 1
rotate = 0
confocal_show = 1
colorbar_bool = 1
colorbar_rotate = 1

color_min = 200
color_max = 40000

# peak finding parameters
min_distance = 5 #enforces minimum pixel distance between two identified peaks
threshold_factor = 1.5 #multiplied with the mean of the confocal to set the threshold

##############################################################################################
# load data
confocal = np.loadtxt(path+file+'.kns')
meta = np.loadtxt(path+file+".kns1")

# coordinate transformation parameters
x_min = meta[0]
y_min = meta[2]
x_step = meta[1]
y_step = meta[3]
x_max = x_min+x_step*len(confocal)
y_max = y_min+y_step*len(confocal[0])

if rotate == 1:
    x0 = y_min
    x1 = y_max
    y0 = x_min
    y1 = x_max
else:
    x0 = x_min
    x1 = x_max
    y0 = y_min
    y1 = y_max

# rotate PL figure if desired
if rotate == 1:
    confocal = np.rot90(confocal)

# show raw PL confocal scan
if confocal_show == 1:
    plt.figure(figsize = (10,10))
    plt.imshow(confocal, origin='lower', extent=[x0, x1, y0, y1])
    plt.title(plot_title)
    if colorbar_bool == 1:
        if colorbar_rotate == 1:
            cbar = plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
            cbar.formatter.set_powerlimits((0, 0))
            cbar.ax.yaxis.set_offset_position('left')
        else:
            cbar = plt.colorbar(fraction=0.046, pad=0.04)
            cbar.formatter.set_powerlimits((0, 0))
            cbar.ax.yaxis.set_offset_position('left')
        plt.clim(color_min, color_max)
    if save_bool == 1:
        plt.savefig(save_path+'_confocal.png', bbox_inches='tight')
    plt.show()

# #applying the detection and plotting results
detected_peaks = peak_local_max(confocal, min_distance=min_distance, threshold_abs=threshold_factor*np.mean(confocal))
peak_y, peak_x = detected_peaks.T
coord_x = [x_min+j*x_step for j in peak_x]
coord_y = [y_min+j*y_step for j in peak_y]

plt.figure(figsize=(10,10))
plt.imshow(confocal, origin='lower', extent=[x0, x1, y0, y1])
plt.title(plot_title+" Peak Finding")
if colorbar_bool == 1:
    if colorbar_rotate == 1:
        cbar = plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
        cbar.formatter.set_powerlimits((0, 0))
        cbar.ax.yaxis.set_offset_position('left')
    else:
        cbar = plt.colorbar(fraction=0.046, pad=0.04)
        cbar.formatter.set_powerlimits((0, 0))
        cbar.ax.yaxis.set_offset_position('left')
    plt.clim(color_min, color_max)
plt.scatter(coord_x, coord_y, marker='.', c='r')
if save_bool == 1:
    plt.savefig(save_path+'_peak_find.png', bbox_inches='tight')
plt.show()

# produce data file with all coordinates, need to convert from pixel location --> need a way to automatically grab this info
if save_bool == 1:
    f = open(save_path+"_meta.txt", "w")
    f.write(file+'\n')
    f.write("Minimum distance:{}\n".format(min_distance))
    f.write("Threshold factor:{}\n".format(threshold_factor))
    f.close()
    f = open(save_path+"_peak_find.txt", "w")
    for i, j in zip(coord_x, coord_y):
        f.write("{:.2f},{:.2f}\n".format(i, j))

print(len(peak_x))
