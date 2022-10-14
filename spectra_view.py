import numpy as np
import matplotlib.pyplot as plt

file1 = '20220926_dev1_1714g_10s_confocal_polarizer.kns'
file2 = '20220926_dev1_1714g_10s_coupler_polarizer.kns'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220926_LND03_SiV\\20220926_dev1_PL_study\\"

save_title1 = '20220926_dev1_1714g_10s_comparison_polarizer.png'
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220926_LND03_SiV\\20220926_dev1_PL_study\\"

plot_title = "Photoluminescence Spectra, 710nm Excitation"

plot_normalize_bool = 0
background_bool = 1
x_limits_bool = 1
y_limits_bool = 0
andor_calibrate = 0
save_bool = 1

x_min = 735.5
x_max = 738.5

y_min = -200
y_max = 101000

background_range = [0, 200]
show_background = 1

wave, counts = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter="\t")
wave1, counts1 = np.loadtxt(path+file2, unpack=True, skiprows=0, delimiter="\t")

if plot_normalize_bool == 1:
    counts = counts/max(counts)
    # counts1 = counts1/max(counts1)

if andor_calibrate == 1:
    def calib(pixel):
        return(-1E-08*pixel**3 + 3E-05*pixel**2 + 0.2076*pixel + 528.88)

if andor_calibrate == 1:
    wave = calib(wave)

if show_background == 1:
    plt.plot(wave, counts/10, marker=".")
    plt.plot(wave1, counts1/10, marker='.')
    plt.axvspan(wave[background_range[0]], wave[background_range[1]], color='r')
    plt.show()

background_counts = np.mean(counts[background_range[0]:background_range[1]])
print(background_counts)

if background_bool == 1:
    counts = counts-background_counts
    counts1  = counts1-background_counts

plt.figure(figsize=(8,6))
plt.plot(wave, counts/10, linestyle="-", marker='.', markersize=2, label="Confocal Collection", color="C1")
plt.plot(wave1, counts1/10, linestyle='-', marker='.', markersize=2, label="Coupler Collection", color="C0", zorder=1)
plt.plot()
plt.title(plot_title)
plt.legend()
plt.ylabel("Intensity (cps)")
plt.xlabel("Wavelength (nm)")
if x_limits_bool == 1:
    plt.xlim(x_min, x_max)
if y_limits_bool == 1:
    plt.ylim(y_min, y_max)
if save_bool == 1:
    plt.savefig(save_path+save_title1+'.png', bbox="tight")
plt.show()
