import matplotlib.pyplot as plt
import numpy as np

file = '20220321_siv_transfer_717nm_740BP_BS_210uW_1714_1s_sat_curve.knspl'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220322_SiV_WG_on_LN\\'+file

wave, counts = np.loadtxt(path, unpack=True, skiprows=0, delimiter="\t")

plot_simple = 1
plot_ranges = 1

int_range = [1200, 1500]
background_range = [0, 500]

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

background = np.mean(counts[background_range[0]::background_range[1]])
# print(background)
integration = np.sum(counts[int_range[0]:int_range[1]])
# print(integration)
signal_count = integration - background*(int_range[1]-int_range[0])
print(signal_count)
