import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

# Enter Data
file1 = 'confocal_sat.txt'
file2 = 'coupler_sat.txt'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220922_LND03_SiV\\dev1-saturation-PL-manual\\"

save_title = "combined_sat_polarization_log.png"
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220922_LND03_SiV\\dev1-saturation-PL-manual\\"+save_title

plot_title = "SiV Saturation Curve"
save_bool = 1

plot_max = 4

# Enter parameter guesses
p_o = 10
f_o = 10
b = 0.001

counts1 = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter=",")
counts2 = np.loadtxt(path+file2, unpack=True, skiprows=0, delimiter=",")
power = [10e-3, 26e-3, 51e-3, 100e-3, 210e-3, 400e-3, 600e-3,
        800e-3, 1, 2, 3, 4.3, 5.1, 6.2]

# additional normalizations if needed
power = [i*0.3 for i in power]
counts1 = counts1/15/0.7*0.4
counts2 = counts2/15

def saturation(power, f_o, p_o, b):
    return(f_o*power/(p_o+power))

# plt.plot(power, counts, marker="o")
# plt.title(plot_title)
# plt.ylabel("Intensity (Counts)")
# plt.xlabel("Power (mW)")
# plt.savefig(save_path+save_title+'.png', bbox="tight")
# plt.show()

params1, params_covariance1 = optimize.curve_fit(saturation, power, counts1, p0=[f_o, p_o, b])
params2, params_covariance2 = optimize.curve_fit(saturation, power, counts2, p0=[f_o, p_o, b])
print("[fo, po, b]", params1)
print("[fo, po, b]", params2)

plot_range = np.linspace(0, plot_max, 100)

y_o = [saturation(i, f_o, p_o, b) for i in plot_range]
y_list1 = [saturation(i, params1[0], params1[1], params1[2]) for i in plot_range]
y_list2 = [saturation(i, params2[0], params2[1], params2[2]) for i in plot_range]

background1 = [params1[2]*i for i in plot_range]
sat_no_back1 = [i-j for i,j in zip(y_list1, background1)]

background2 = [params2[2]*i for i in plot_range]
sat_no_back2 = [i-j for i,j in zip(y_list2, background2)]

plt.figure(figsize=(8, 6))
plt.title(plot_title)
# plt.plot(power, y_list, label="Fit", marker="o")
# plt.plot(power, y_o, label="Fit Guess", marker="o")
# plt.plot(power, background, label="Background Fit", marker="o")
plt.plot(plot_range, y_list1, label="Confocal Fit", color='C1', linestyle='--')
plt.scatter(power, counts1, label="Confocal Data", marker="^", color='k')
plt.plot(plot_range, y_list2, label="Coupler Fit", color='C2', linestyle='--')
plt.scatter(power, counts2, label="Coupler Data", marker="o", color='k')
plt.ylabel("Intensity (cps)")
plt.xlabel("mW")
plt.yscale('log')
# plt.xscale('log')
plt.legend()
if save_bool == 1:
    plt.savefig(save_path, bbox="tight")
plt.show()

ratio = [i/j for i,j in zip(y_list2, y_list1)]
print(ratio)
plt.plot(plot_range, ratio)
plt.show()
