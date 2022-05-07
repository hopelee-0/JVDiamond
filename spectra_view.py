import numpy as np
import matplotlib.pyplot as plt

file = 'LN_1366_0_5s_SuperK_75_1350bandpass_block1_2_1.txt'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220228\\'+file

save_title = "20220405_1366nm_transmission_gc_spectrum.png"
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220405\\'+save_title

plot_title = "1366nm Grating Coupler Transmission Spectrum"

plot_normalize_bool = 1
x_limits_bool = 1
andor_calibrate = 0
save_bool = 1

wave, blank, counts = np.loadtxt(path, unpack=True, skiprows=0, delimiter=",")

if plot_normalize_bool == 1:
    counts = counts/max(counts)

if andor_calibrate == 1:
    def calib(pixel):
        return(-1E-08*pixel**3 + 3E-05*pixel**2 + 0.2076*pixel + 528.88)

if andor_calibrate == 1:
    wave = calib(wave)

x_min = 1300
x_max = 1400

plt.figure(figsize=(8,6))
plt.plot(wave, counts)
plt.plot()
plt.title(plot_title)
plt.ylabel("Optical Density")
plt.xlabel("Wavelength (nm)")
if x_limits_bool == 1:
    plt.xlim(x_min, x_max)
    # plt.ylim(0.63, 1.01)
if save_bool == 1:
    plt.savefig(save_path+save_title+'.png', bbox="tight")
plt.show()
