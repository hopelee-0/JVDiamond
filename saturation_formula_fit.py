import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

# Enter Data
file1 = 'confocal_sat.txt'
# file2 = 'coupler_sat.txt'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220922_LND03_SiV\\dev1-saturation-PL-manual\\"

save_title = "20221014_coupler1_collect_log_sat.png"
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221014_LND03\\20221014_LND03_PL\\coupler1_collect_PL\\coupler1_collect_sat\\"+save_title

plot_title = "SiV Saturation Curve, Confocal Excitation, Coupler Collection"
save_bool = 0

log_bool = 1

plot_max = 5

# Enter parameter guesses
p_o = 10
f_o = 10
b = 0.001

# counts1 = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter=",")
# counts1 = [42066.5, 7878.0, 1284.0, 806.5, 1265.5, 32297.0, 197244.5, 227585.0, 212123.5, 175152.0, 1029.0, 154848.0, 3515.5,
            # 22649.5, 15035.5, 1787.5, 132362.5, 76412.5, 108295.5, 2605.5, 18837.5, 10233.0, 58689.0]
# counts2 = np.loadtxt(path+file2, unpack=True, skiprows=0, delimiter=",")
# power = [1, 150e-3, 100e-3, 0, 10e-3, 0.75, 7, 9, 8, 6, 5e-3, 5.1, 50e-3, 500e-3, 300e-3, 20e-3, 4.1, 2, 3, 30e-3, 400e-3, 200e-3, 1.5]

counts1 = [1066.5/15, 5573.0/10, 1275.5/15, 6882.0/10, 4743.5/10, 4362.0/10, 6437.0/10, 6013.5/10, 3373.5/10, 2286.5/10,
            2459.5/10, 7684.0/10, 7359.5/10, 1998.5/15, 1967.0/15, 1399.5/15, 2046.0/15, 1342.5/15, 2439.5/15]
power = [0, 6, 100e-3, 9, 5.1, 4, 8, 7, 3, 1.5, 2, 11, 10, 750e-3, 500e-3, 300e-3, 400e-3, 200e-3, 1]

# additional normalizations if needed
power = [i*0.5 for i in power]
counts1 = [i*2/0.1 for i in counts1]

def saturation(power, f_o, p_o, b):
    return(f_o*power/(p_o+power)+b*power)

# plt.plot(power, counts, marker="o")
# plt.title(plot_title)
# plt.ylabel("Intensity (Counts)")
# plt.xlabel("Power (mW)")
# plt.savefig(save_path+save_title+'.png', bbox="tight")
# plt.show()

params1, params_covariance1 = optimize.curve_fit(saturation, power, counts1, p0=[f_o, p_o, b])
# params2, params_covariance2 = optimize.curve_fit(saturation, power, counts2, p0=[f_o, p_o, b])
print("[fo, po, b]", params1)
# print("[fo, po, b]", params2)

plot_range = np.linspace(0, plot_max, 100)

y_o = [saturation(i, f_o, p_o, b) for i in plot_range]
y_list1 = [saturation(i, params1[0], params1[1], params1[2]) for i in plot_range]
# y_list2 = [saturation(i, params2[0], params2[1], params2[2]) for i in plot_range]

background1 = [params1[2]*i for i in plot_range]
sat_no_back1 = [i-j for i,j in zip(y_list1, background1)]

# background2 = [params2[2]*i for i in plot_range]
# sat_no_back2 = [i-j for i,j in zip(y_list2, background2)]

plt.figure(figsize=(8, 6))
plt.title(plot_title, y=1.08)
# plt.plot(power, y_list, label="Fit", marker="o")
# plt.plot(power, y_o, label="Fit Guess", marker="o")
# plt.plot(power, background, label="Background Fit", marker="o")
plt.plot(plot_range, y_list1, label="Confocal Fit", color='C1', linestyle='--')
plt.scatter(power, counts1, label="Confocal Data", marker="^", color='k')
# plt.plot(plot_range, y_list2, label="Coupler Fit", color='C2', linestyle='--')
# plt.scatter(power, counts2, label="Coupler Data", marker="o", color='k')
plt.ylabel("Intensity (cps)")
plt.xlabel("mW")
if log_bool == 1:
    plt.yscale('log')
else:
    plt.ticklabel_format(style='sci', scilimits=(0,0))
# plt.xscale('log')
plt.legend()
if save_bool == 1:
    plt.savefig(save_path, bbox="tight")
plt.show()

# ratio = [i/j for i,j in zip(y_list2, y_list1)]
# print(ratio)
# plt.plot(plot_range, ratio)
# plt.show()
