import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#takes folder of all PL spectra, and only PL
name = "20220927_dev1_1714g_10s_coupler_8mW.kns"
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220926_LND03_SiV\\20220927_LND03\\"

save_name = "20220927_dev1_1714g_10s_coupler_8mW_peaks"
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220926_LND03_SiV\\20220927_LND03\\"+save_name

# peak finding parameters
threshold_factor = 1.2
distance = 5
pro_min = 0
width = 1

# bools for controllong outputs
view = 1
view_save = 1

data_list = []

wave, counts = np.loadtxt(path+name, unpack=True, skiprows=0)
peaks, _ = find_peaks(counts, distance=distance, height=threshold_factor*np.mean(counts), prominence=(pro_min, ), width=width)
peak_wave = wave[peaks]
peak_counts = counts[peaks]

# optional plotting for visual verification
plt.plot(wave, counts)
plt.scatter(peak_wave, peak_counts, c="C1")
if view_save == 1:
    plt.savefig(save_path+'_.png')
if view == 1:
     plt.show()
data_list.append(peak_wave)


# writing output file, use csv to maintain grouping structure
f = open(save_path+save_name+".txt", "w")
for i in list(data_list):
    f.write(str(i)+"\n")
f.write("\n")
