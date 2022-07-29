import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#takes folder of all PL spectra, and only PL
name = "test"
folder = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220725_EZ01\\20220725_I15\\"

save_name = "20220725_I15_1s_PL"
save_folder = "20220725_I15_1s\\"
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220724_EZ01\\"+save_folder+save_name

# bools for controllong outputs
view = 0
view_save = 1

# start iterating through folder contents, with counter to index figures
counter = 0

for file in os.listdir(folder):
    wave, counts = np.loadtxt(folder+file, unpack=True, skiprows=0)

    # optional plotting for visual verification
    plt.plot(wave, counts)
    if view_save == 1:
        plt.savefig(save_path+"_"+str(counter)+'.png')
    if view == 1:
         plt.show()
    plt.clf()
    counter += 1
