import numpy as np

path = "/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20230116/confocal sat curve/"
power_file = "20230116_confocal_sat_curve_power_001.txt"
counts_file = "20230116_confocal_sat_curve_counts_001.txt"

save_title = "20230116_confocal_sat_curve_counts_001"
save_path = path

power_list = np.loadtxt(path+power_file, unpack=True, skiprows=2, delimiter=",", usecols=range(1))
counts_list = np.loadtxt(path+counts_file, unpack=True, skiprows=2, delimiter=",", usecols=range(1))

power_list = np.sort(power_list)
counts_list = np.sort(counts_list)

plt.plot(power_list, counts_list)
plt.show()