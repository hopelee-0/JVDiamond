import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

# Import PL confocal data
file = '20220510_EZ03_001_500mV_AOM_PLE_28ghz.kns'
path = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220510_EZ03\\"+file

save_name = "20220510_EZ03_001_500mV_AOM_PLE_28ghz.png"
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220516\\'+save_name

save_bool = 1
rotate = 0

confocal = np.loadtxt(path)
if rotate == 1:
    confocal = np.rot90(confocal)

confocal_trimmed = confocal.T[0:50]

plt.imshow(confocal_trimmed.T, origin='lower')
plt.title("PLE Confocal")
if rotate == 1:
    plt.colorbar(orientation='horizontal')
else:
    cb = plt.colorbar()
    cb.formatter.set_powerlimits((0, 0))
    cb.ax.yaxis.set_offset_position('left')
if save_bool == 1:
    plt.savefig(save_path, bbox_inches='tight')
plt.show()
