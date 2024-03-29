import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import peak_local_max

file = "20230711_EZ04_wvg_001"
path = "/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/EZ04 Disks/20230711/"

save_name = file # no extension since added later
save_path = "/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/EZ04 Disks/20230711/"+save_name

plot_title = ''

save_bool = 1
rotate = 0
confocal_show = 1
colorbar_bool = 1
colorbar_rotate = 1

manual_color = 0
color_min = 100
color_max = 150000

# peak finding parameters
peak_find_bool = 0
min_distance = 5 #enforces minimum pixel distance between two identified peaks
threshold_factor = 1.5 #multiplied with the mean of the confocal to set the threshold

# for cutting out features that we aren't interested in
peak_find_filter_bool = 1
peak_find_filter_x = [-3, 2.5]
peak_find_filter_y = [-1, 1]

##############################################################################################
# load data
confocal = np.loadtxt(path+file+'.kns')
meta = np.loadtxt(path+file+".kns1")

# coordinate transformation parameters
x_min = meta[0]
y_min = meta[2]
x_step = meta[1]
y_step = meta[3]
x_max = x_min+x_step*len(confocal[0])
y_max = y_min+y_step*len(confocal)

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
    plt.yticks([])
    plt.xticks([])
    plt.title(plot_title)
    if colorbar_bool == 1:
        if colorbar_rotate == 1:
            cbar = plt.colorbar(location ='bottom', aspect = 70, pad=0.01)
            cbar.formatter.set_powerlimits((0, 0))
            # cbar.ax.yaxis.set_offset_position('right')
            cbar.set_ticklabels(['0', '1.5e5'])
        else:
            cbar = plt.colorbar(fraction=0.046, pad=0.04, shrink=0.5)
            cbar.formatter.set_powerlimits((0, 0))
            cbar.ax.yaxis.set_offset_position('left')
        if manual_color == 1:
            plt.clim(color_min, color_max)
    if save_bool == 1:
        plt.savefig(save_path+'_confocal.png', bbox_inches='tight', transparent=True)
    plt.show()

# #applying the detection and plotting results
if peak_find_bool == 1:
    detected_peaks = peak_local_max(confocal, min_distance=min_distance, threshold_abs=threshold_factor*np.mean(confocal))
    peak_y, peak_x = detected_peaks.T
    coord_x = [x_min+j*x_step for j in peak_x]
    coord_y = [y_min+j*y_step for j in peak_y]

    plt.figure(figsize=(10,10))
    plt.imshow(confocal, origin='lower', extent=[x0, x1, y0, y1])
    plt.title(plot_title+" Peak Finding")
    # ax=plt.gca()
    # ax.invert_yaxis()
    if colorbar_bool == 1:
        if colorbar_rotate == 1:
            cbar = plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04, shrink=0.5)
            cbar.formatter.set_powerlimits((0, 0))
            cbar.ax.yaxis.set_offset_position('left')
        else:
            cbar = plt.colorbar(fraction=0.046, pad=0.04, shrink=0.5)
            cbar.formatter.set_powerlimits((0, 0))
            cbar.ax.yaxis.set_offset_position('left')
        plt.clim(color_min, color_max)
    plt.scatter(coord_x, coord_y, marker='.', c='r')
    if save_bool == 1:
        plt.savefig(save_path+'_peak_find.png', bbox_inches='tight')
    plt.show()

    if peak_find_filter_bool == 1:

        filtered = [[i,j] for i,j in zip(coord_x, coord_y) if (peak_find_filter_x[0]<=i<=peak_find_filter_x[1]) and (peak_find_filter_y[0]<=j<=peak_find_filter_y[1])]

        coord_x = [i[0] for i in filtered]
        coord_y = [i[1] for i in filtered]

        # check filtering
        plt.figure(figsize=(10,10))
        plt.imshow(confocal, origin='lower', extent=[x0, x1, y0, y1])
        plt.title(plot_title+" Peak Finding")
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
        f = open(save_path+".txt", "w")
        for i, j in zip(coord_x, coord_y):
            f.write("{:.2f},{:.2f}\n".format(i, j))
    print(len(coord_x))
