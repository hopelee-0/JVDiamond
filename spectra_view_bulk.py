import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#takes folder of all PL spectra, and only PL
name = "test"
folder = "C:\\Users\\hopel\\Documents\\Data\\20220729_EZ01\\J15_PSB\\"

save_name = "J15_PSB_PL"
save_folder = "J15_PSB\\"
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220729_EZ01\\20220729_J15_PL\\"+save_folder+save_name

# bools for controllong outputs
view = 0
save_bool = 0

# number of spectrum to survey to determine option parameters
sample = 5

# option to subtract background
background_bool = 1
background_range = [0, 200] # indices range

# option to define plotting background
range_view = 0

x_range_bool = 0
x_min = 615
x_max = 625

y_range_bool = 0
y_min = -5
y_max = 6000

##############################################################################################

if background_bool == 1:
    wave, counts = np.loadtxt(folder+os.listdir(folder)[sample], unpack=True, skiprows=0)
    plt.plot(wave, counts)
    plt.axvspan(wave[background_range[0]], wave[background_range[1]], alpha=0.5, color='red')
    plt.show()

if range_view == 1:
    wave, counts = np.loadtxt(folder+os.listdir(folder)[sample], unpack=True, skiprows=0)
    if background_bool == 1:
        counts = counts - np.mean(counts[background_range[0]::background_range[1]])
    plt.plot(wave, counts)
    if x_range_bool == 1:
        plt.xlim([x_min, x_max])
    if y_range_bool == 1:
        plt.ylim([y_min, y_max])
    plt.show()

# start iterating through folder contents, with counter to index figures
counter = 0

for file in os.listdir(folder):
    wave, counts = np.loadtxt(folder+file, unpack=True, skiprows=0)

    if background_bool == 1:
        background = np.mean(counts[background_range[0]::background_range[1]])
        counts = counts - background

    # optional plotting for visual verification
    plt.plot(wave, counts)
    if x_range_bool == 1:
        plt.xlim([x_min, x_max])
    if y_range_bool == 1:
        plt.ylim([y_min, y_max])
    if save_bool == 1:
        plt.savefig(save_path+"_"+str(counter)+'.png')
    if view == 1:
         plt.show()
    plt.clf()
    print(counter)
    counter += 1
