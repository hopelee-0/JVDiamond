import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

# Import PL confocal data
file = 'test'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220729_EZ01\\"

save_name = "J15_PSB_002" # no extension since added later
save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220729_EZ01\\'+save_name

plot_title = "O15 ZPL Scan"

save_bool = 0
trimmed_bool = 0
colorbar_rotate = 0
rotate = 0

color_min = 200
color_max = 20000

##############################################################################################

confocal = np.loadtxt(path+file+".kns")
meta = np.loadtxt(path+file+".kns1")

if rotate == 1:
    confocal = np.rot90(confocal)

if trimmed_bool == 1:
    confocal = confocal.T[0:50]

# axes calibration from meta data values
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
    print('saved')
plt.show()
