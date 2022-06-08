import numpy as np
import matplotlib.pyplot as plt

file1 = 'PL_20220505_EZ03_002.kns'
path = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220505_EZ03\\"

save_title = 'PL_20220505_EZ03_002.png'
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220516\\'+save_title

plot_title = "4.7K PL Spectrum, 532nm Excitation"

plot_normalize_bool = 1
x_limits_bool = 1
andor_calibrate = 0
save_bool = 1

wave, counts = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter="\t")
# wave1, counts1 = np.loadtxt(path+file2, unpack=True, skiprows=0, delimiter=",")


if plot_normalize_bool == 1:
    counts = counts/max(counts)
    # counts1 = counts1/max(counts1)

if andor_calibrate == 1:
    def calib(pixel):
        return(-1E-08*pixel**3 + 3E-05*pixel**2 + 0.2076*pixel + 528.88)

if andor_calibrate == 1:
    wave = calib(wave)

x_min = 618.5
x_max = 621

plt.figure(figsize=(8,6))
plt.plot(wave, counts, marker='.')
# plt.plot(wave1, counts1)
plt.plot()
plt.title(plot_title)
plt.ylabel("Intensity (counts)")
plt.xlabel("Frequency Offset")
if x_limits_bool == 1:
    plt.xlim(x_min, x_max)
    # plt.ylim(0.63, 1.01)
if save_bool == 1:
    plt.savefig(save_path+'.png', bbox="tight")
plt.show()
