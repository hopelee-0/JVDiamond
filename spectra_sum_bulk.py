import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#takes folder of all PL spectra, and only PL
folder = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220725_EZ01\\20220725_I15\\"

save_name = "I15_PL_summed"
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220724_EZ01\\"+save_name

plot_title = "I15 PL Summed, 550 LP"

# bools for controllong outputs
view = 1
save_bool = 1

# number of spectrum to survey to determine option parameters
sample = 5

# option to subtract background
background_bool = 1
background_range = [100, 200] # indices range

# option to define plotting background
range_view = 0

x_range_bool = 0
x_min = 615
x_max = 652

y_range_bool = 0
y_min = -700
y_max = 2000

##############################################################################################

if background_bool == 1:
    wave, counts = np.loadtxt(folder+os.listdir(folder)[sample], unpack=True, skiprows=0)
    plt.plot(wave, counts)
    plt.axvspan(wave[background_range[0]], wave[background_range[1]], alpha=0.5, color='red')
    if view == 1:
        plt.show()
    plt.clf()

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

# initialize arrays using first spectrum, will sum subsequent spectrum with initial
sum_wave, sum_counts = wave, counts = np.loadtxt(folder+os.listdir(folder)[0], unpack=True, skiprows=0)
if background_bool == 1:
    background = np.mean(counts[background_range[0]::background_range[1]])
    sum_counts = sum_counts - background

# sum all counts
for file in os.listdir(folder)[1::]:
    wave, counts = np.loadtxt(folder+file, unpack=True, skiprows=0)

    if background_bool == 1:
        background = np.mean(counts[background_range[0]::background_range[1]])
        counts = counts - background

    sum_counts = [i+j for i,j in zip(sum_counts, counts)]

plt.plot(sum_wave, sum_counts)
plt.title(plot_title)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Counts")
if x_range_bool == 1:
    plt.xlim([x_min, x_max])
if y_range_bool == 1:
    plt.ylim([y_min, y_max])
if save_bool == 1:
    plt.savefig(save_path+'_summed.png')
if view == 1:
    plt.show()
