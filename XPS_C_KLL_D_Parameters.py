import numpy as np
import scipy
import matplotlib.pyplot as plt
import statsmodels
from statsmodels.nonparametric.smoothers_lowess import lowess

file = '20210817_Diamond_EL15_HR_cKLL.csv'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210817\\20210817_XPS\\'+file
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210813\\'
energy, counts = np.loadtxt(path, unpack=True, skiprows=4, delimiter=",")

plot_title = "cKLL XPS D parameter of EL15"
save_title = "20210818_Diamond_EL15_parameter_f0p35"
save_bool = 1
data_print = 1

all_plot = 0
diff_plot = 0
moving_avg_toggle = 0
filter_toggle = 1
min_max_plot = 1

cutoff_range = [0,-1]
pt_avg_num = 60
filter_frac = 0.35

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same')

if moving_avg_toggle == 1:
    moving_filter = pt_avg_num-1
    counts = moving_average(counts, pt_avg_num)
    energy = energy[moving_filter:-moving_filter]
    counts = counts[moving_filter:-moving_filter]

if filter_toggle == 1:
    counts = lowess(counts, energy, frac=filter_frac, return_sorted=False)

dx = abs(energy[1]-energy[0])
counts_diff = np.gradient(counts, dx)
energy_diff = energy

if all_plot == 1:
    ax = plt.gca()
    plt.plot(energy, counts)
    ax.invert_xaxis()
    plt.show()

if diff_plot == 1:
    ax = plt.gca()
    plt.plot(energy_diff, counts_diff)
    ax.invert_xaxis()
    plt.show()

energy_diff = energy_diff[cutoff_range[0]: cutoff_range[1]]
counts_diff = counts_diff[cutoff_range[0]: cutoff_range[1]]

# find max and min:
max_counts = max(counts_diff)
min_counts = min(counts_diff)
max_energy = energy_diff[np.where(counts_diff==max_counts)]
min_energy = energy_diff[np.where(counts_diff==min_counts)]

d_parameter = abs(max_energy-min_energy)
print(d_parameter)

d_percent = (d_parameter[0]-21)/(-8)
print("Diamond percentage: ", d_percent)

ax = plt.gca()
plt.title(plot_title)
plt.plot(energy_diff, counts_diff)
plt.scatter([min_energy, max_energy], [min_counts, max_counts], color="C1", label="{:.2f} eV".format(d_parameter[0]))
plt.legend()
ax.invert_xaxis()
if save_bool == 1:
    plt.savefig(save_path+save_title+'.png')
if min_max_plot == 1:
    plt.show()

if data_print == 1:
    f = open(save_path+save_title+"_data.txt", "w")
    f.write("d Parameter: {0:.4f}\n".format(d_parameter[0]))
    f.write("Nominal Diamond Percentage: {0:.4f}\n".format(d_percent))
    f.write('\n')
    for i,j in zip(energy_diff, counts_diff):
        f.write('{},{}\n'.format(i,j))
