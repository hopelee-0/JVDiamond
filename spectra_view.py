import numpy as np
import matplotlib.pyplot as plt

file1 = '20220722_J15_60s_550LP_600grating_inhomogeneous.kns'
# file2 = '20220629_SiV_SM_710nm_excite_confocal_PL_1714_3s_010.kns'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220722_EZ01\\20220722_EZ01\\J15_1s\\"

save_title1 = '20220722_J15_60s_550LP_150grating_inhomogeneous.png'
save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220724_EZ01\\'

plot_title = "E4 Inhomogeneous Broadening, 60s Integration"

plot_normalize_bool = 0
background_bool = 1
x_limits_bool = 1
y_limits_bool = 0
andor_calibrate = 0
save_bool = 1

x_min = 608
x_max = 652

y_min = 0
y_max = 4000

background_range = [0, 200]
show_background = 1

wave, counts = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter="\t")
# wave1, counts1 = np.loadtxt(path+file2, unpack=True, skiprows=0, delimiter="\t")

if plot_normalize_bool == 1:
    counts = counts/max(counts)
    # counts1 = counts1/max(counts1)

if andor_calibrate == 1:
    def calib(pixel):
        return(-1E-08*pixel**3 + 3E-05*pixel**2 + 0.2076*pixel + 528.88)

if andor_calibrate == 1:
    wave = calib(wave)

if show_background == 1:
    plt.plot(wave, counts, marker=".")
    plt.axvspan(wave[background_range[0]], wave[background_range[1]], color='r')
    plt.show()

background_counts = np.mean(counts[background_range[0]:background_range[1]])
if background_bool == 1:
    counts = counts-background_counts
    # counts1  = counts1-background_counts

plt.figure(figsize=(8,6))
plt.plot(wave, counts, marker='.', markersize=2, label="Confocal Collection")
# plt.plot(wave1, counts1, marker='.', markersize=2, label="Coupler Collection")
# plt.plot(wave1, counts1)
plt.plot()
plt.title(plot_title)
# plt.legend()
plt.ylabel("Intensity (counts)")
plt.xlabel("Frequency Offset")
if x_limits_bool == 1:
    plt.xlim(x_min, x_max)
if y_limits_bool == 1:
    plt.ylim(y_min, y_max)
if save_bool == 1:
    plt.savefig(save_path+save_title1+'.png', bbox="tight")
plt.show()
