import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#takes folder of all PL spectra, and only PL
name = "test folder"
folder = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220318\\"

save_name = "test"
save_path = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220414\\"+save_name

# peak finding parameters
threshold_factor = 1
distance = 5
pro_min = 1
width = 3

# bools for controllong outputs
view = 0
view_save = 1

# start iterating through folder contents, with counter to index figures
counter = 0
# create list of lists of lists to store full data set, will then write to a csv file
data_list = []

for file in os.listdir(folder):
    wave, counts = np.loadtxt(folder+file, unpack=True, skiprows=0)
    peaks, _ = find_peaks(counts, distance=distance, height=threshold_factor*np.mean(counts), prominence=(pro_min, ), width=width)
    peak_wave = wave[peaks]
    peak_counts = counts[peaks]

    # optional plotting for visual verification
    plt.plot(wave, counts)
    plt.scatter(peak_wave, peak_counts, c="C1")
    if view_save == 1:
        plt.savefig(save_path+"_"+str(counter)+'.png')
    if view == 1:
         plt.show()
    data_list.append([peak_wave, peak_counts])
    counter += 1

# writing output file, use csv to maintain grouping structure
with open(save_path+".csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Wavelengths", "Counts"])
    for i in data_list:
        writer.writerows(data_list)
