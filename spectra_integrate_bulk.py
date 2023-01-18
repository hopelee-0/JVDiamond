import matplotlib.pyplot as plt
import numpy as np
import os

folder = "spectra/"
path = "/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20230116/confocal sat curve/"

save_title = "20230116_confocal_sat_curve_counts_001"
save_path = path

plot_simple = 0
plot_ranges = 0
save_bool = 1

integration = 2

int_range = [800, 1200]
background_range = [0, 500]

if save_bool == 1:
    f = open(save_path+save_title+".txt", "w")
    f.write(save_title+"\n")
    f.write("File, cps\n")

directory = path+folder
for file in os.listdir(directory):
    full_path = directory+file
    wave, counts = np.loadtxt(full_path, unpack=True, skiprows=0, delimiter="\t")
    print(file)
    if plot_simple == 1:
        plt.figure(figsize=(8,6))
        plt.plot(wave, counts)
        plt.ylabel("Optical Density")
        plt.xlabel("Wavelength (nm)")
        plt.show()
    if plot_ranges == 1:
        plt.figure(figsize=(8,6))
        plt.plot(wave, counts)
        plt.axvspan(wave[int_range[0]], wave[int_range[1]], alpha=0.5, color='black')
        plt.axvspan(wave[background_range[0]], wave[background_range[1]], alpha=0.5, color='red')
        plt.ylabel("Optical Density")
        plt.xlabel("Wavelength (nm)")
        plt.show()

    background = np.mean(counts[background_range[0]:background_range[1]])
    integration = np.sum(counts[int_range[0]:int_range[1]])
    signal_count = integration - background*(int_range[1]-int_range[0])/integration

    f.write(str(file)+', '+str(signal_count)+'\n')
    # print('written')

f.close()
