import matplotlib.pyplot as plt
import numpy as np

file = '20220922_LND03_SiV_dev1_15s_1714_PL_manual_at_flip_6p2mw_coupler.kns'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220922_LND03_SiV\\dev1-saturation-PL-manual\\"+file

wave, counts = np.loadtxt(path, unpack=True, skiprows=0, delimiter="\t")

plot_simple = 0
plot_ranges = 0

int_range = [560, 680]
background_range = [0, 200]

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

background_counts = np.mean(counts[background_range[0]:background_range[1]])
# print(background_counts)
integration = np.sum([i- background_counts for i in counts[int_range[0]:int_range[1]]])
print(integration)
