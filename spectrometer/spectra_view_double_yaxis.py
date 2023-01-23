import numpy as np
import matplotlib.pyplot as plt

file1 = '20221128_58power_150g_2s_SM_connected_01.kns'
file2 = '20221128_63power_150g_1s_MM_connected_01.kns'
path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221128_LND03\\'

save_title1 = '20221130_connected1_transmissions.png'
save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221128_LND03\\'

plot_title = ""

plot_normalize_bool = 1
background_bool = 1
x_limits_bool = 1
y_limits_bool = 1
save_bool = 1

x_min = 700
x_max = 770

x_shift = -1.2

y_min = 0
y_max = 5.7

background_range = [100, 200]
show_background = 0

wave, counts = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter="\t")
wave2, counts2 = np.loadtxt(path+file2, unpack=True, skiprows=0, delimiter="\t")

wave_list = [720
,725.1
,730.3
,735.2
,737
,740
,745
,750
,755
,760
]
transmission_list_MM = [2.97
,4.01
,5.43
,6.8
,7.53
,6.4
,3.74
,1.98
,1.84
,0.99
]

transmission_list_SM = [0.56
,1.25
,2.33
,3.49
,4.27
,3.55
,1.87
,0.8
,0.51
,0.21
]


if plot_normalize_bool == 1:
    counts = counts/max(counts)
    # counts1 = counts1/max(counts1)

if show_background == 1:
    plt.plot(wave, counts, marker=".")
    plt.axvspan(wave[background_range[0]], wave[background_range[1]], color='r')
    plt.show()

background_counts = np.mean(counts[background_range[0]:background_range[1]])
if background_bool == 1:
    counts = counts-background_counts
    # counts1  = counts1-background_counts

fig, ax1 = plt.subplots(figsize=(8,6))
plt.title(plot_title)

color = 'tab:red'
ax1.set_ylabel("Spectrum Intensity, SM (abu)", color=color)
ax1.set_xlabel("Wavelength (nm)")
ax1.plot(wave+x_shift, counts, marker='.', markersize=2, color=color)
ax1.tick_params(axis='y', labelcolor=color)
if x_limits_bool == 1:
    ax1.set_xlim(x_min, x_max)
if y_limits_bool == 1:
    ax1.set_ylim(0, 1.05)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'black'
ax2.set_ylabel('Transmission Percentage', color=color)  # we already handled the x-label with ax1
ax2.scatter(wave_list, transmission_list_SM, marker='o', color=color, label="SM")
ax2.scatter(wave_list, transmission_list_MM, marker='^', color=color, label="MM")
ax2.tick_params(axis='y', labelcolor=color)
if x_limits_bool == 1:
    ax2.set_xlim(x_min, x_max)
if y_limits_bool == 1:
    ax2.set_ylim(y_min, y_max)

# plt.legend()

if save_bool == 1:
    plt.savefig(save_path+save_title1+'.png')
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
