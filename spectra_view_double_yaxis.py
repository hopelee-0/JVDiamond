import numpy as np
import matplotlib.pyplot as plt

file1 = '20221025_transmissions_5s_150g_001.kns'
# file2 = '20220629_SiV_SM_710nm_excite_confocal_PL_1714_3s_010.kns'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221025_LND03\\"

save_title1 = '20221025_transmissions_5s_150g_001.png'
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221025_LND03\\"

plot_title = "Transmission Spectrum"

plot_normalize_bool = 1
background_bool = 1
x_limits_bool = 0
y_limits_bool = 0
andor_calibrate = 0
save_bool = 0

x_min = 608
x_max = 652

y_min = 0
y_max = 4000

background_range = [100, 200]
show_background = 1


wave, counts = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter="\t")

wave_list = [700,705, 710, 715, 720, 725, 730, 735, 740, 745, 750, 760, 765, 770, 775, 780]
transmission_list = [0.570588235
,0.863013699
,1.058823529
,1.416666667
,2.916666667
,3.857142857
,3.384615385
,3.25
,3.75
,3.6
,1.85915493
,0.534883721
,0.367857143
,0.476635514
,0.391093117
,0.37037037
]

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

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_ylabel("Intensity (abu)", color=color)
ax1.set_xlabel("Wavelength (nm)")
ax1.plot(wave, counts, marker='.', markersize=2, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Total Transmission Percentage', color=color)  # we already handled the x-label with ax1
ax2.scatter(wave_list, transmission_list, marker='o', color=color)
ax2.tick_params(axis='y', labelcolor=color)

if save_bool == 1:
    plt.savefig(save_path+save_title1+'.png', bbox="tight")
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
