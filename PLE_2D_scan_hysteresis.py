import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import os

# Import PL confocal data
file = '20220505_PLE_high_power_3.kns'
path = 'C:\\Users\\hopel\\Documents\\Data\\20220505_EZ03\\'+file

save_name = "20220505_EZ03_PLE_high_power_3"
save_dir = "20220505_EZ03_PLE_high_power_3_linecuts\\"
save_path = 'C:\\Users\\hopel\\Documents\\Data\\20220505_EZ03\\'

save_bool = 1
rotate = 0
delete_bool = 1

confocal = np.loadtxt(path)

if os.path.exists(save_path+save_dir) == False: # create a folder to hold all the figures for a PLE scan
    os.makedirs(save_path+save_dir)

if delete_bool == 1:
    confocal = np.delete(confocal, list(range(0, confocal.shape[1], 2)), axis=1) #removes every other column in order to deal with hysteresis

if rotate == 1:
    confocal = np.rot90(confocal)

plt.imshow(confocal, aspect='auto', origin='lower')
if rotate == 1:
    plt.colorbar(orientation='horizontal')
else:
    plt.colorbar()
if save_bool == 1:
    plt.savefig(save_path+save_dir+save_name+".png", bbox_inches='tight')
plt.show()
