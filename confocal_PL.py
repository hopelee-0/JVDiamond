import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

# Import PL confocal data
file = '202220325_siv_transfer_717exc_740BP_BS_2_300UW_confocal_scan_WG3.kns'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220324\\'+file

save_name = "20220405_PL_confocal.png"
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220405\\'+save_name

save_bool = 1
rotate = 1

confocal = np.loadtxt(path)
if rotate == 1:
    confocal = np.rot90(confocal)

plt.imshow(confocal, norm=colors.LogNorm())
if rotate == 1:
    plt.colorbar(orientation='horizontal')
else:
    plt.colorbar()
if save_bool == 1:
    plt.savefig(save_path+save_name, bbox_inches='tight')
plt.show()
