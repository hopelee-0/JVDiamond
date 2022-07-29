import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

# Import PL confocal data
file = '20220725_H15_001'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220725_EZ01\\"

save_name = "20220725_H15_001.png"
save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220725_EZ01\\'+save_name

plot_title = "H15 PL Scan"

save_bool = 1
trimmed_bool = 0
colorbar_rotate = 1
rotate = 0

color_min = 200
color_max = 70000

confocal = np.loadtxt(path+file+".kns")
meta = np.loadtxt(path+file+".kns1")

if rotate == 1:
    confocal = np.rot90(confocal)

if trimmed_bool == 1:
    confocal = confocal.T[0:50]

# axes calibration from meta data values
y_0 = meta[0]
x_0 = meta[2]
y_1 = meta[0]+meta[1]*len(confocal)
x_1 = meta[2]+meta[3]*len(confocal[0])
if rotate == 1:
    x0 = y_0
    x1 = y_1
    y0 = x_0
    y1 = x_1
else:
    x0 = x_0
    x1 = x_1
    y0 = y_0
    y1 = y_1

plt.figure(figsize = (10,10))
plt.imshow(confocal, origin='lower', extent=[x0, x1, y0, y1])
plt.title(plot_title)
if colorbar_rotate == 1:
    cb = plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
    cb.formatter.set_powerlimits((0, 0))
    cb.ax.yaxis.set_offset_position('left')
else:
    cb = plt.colorbar(fraction=0.046, pad=0.04)
    cb.formatter.set_powerlimits((0, 0))
    cb.ax.yaxis.set_offset_position('left')
plt.clim(color_min, color_max)
if save_bool == 1:
    plt.savefig(save_path, bbox_inches='tight')
plt.show()
