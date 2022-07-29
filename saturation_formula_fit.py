import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

# Enter Data
file = '20220629_Saturation_Curve.txt'
path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220629_SiV_LN\\'+file

save_title = "20220629_Saturation_Curve.png"
save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220629_SiV_LN\\'+save_title

plot_title = "SiV Saturation Curve"
save_title = "20220703_siv_LN_saturation"
save_bool = 0

# Enter parameter guesses
p_o = 10000
f_o = 10000
b = 0.001

counts = np.loadtxt(path, unpack=True, skiprows=1, delimiter=",")
power = [1, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70]
power = [i*0.077 for i in power]

def saturation(power, f_o, p_o, b):
    return(f_o*power/(p_o+power)+b*power)

plt.plot(power, counts, marker="o")
plt.title(plot_title)
plt.ylabel("Intensity (Counts)")
plt.xlabel("Power (mW)")
plt.savefig(save_path+save_title+'.png', bbox="tight")
plt.show()

params, params_covariance = optimize.curve_fit(saturation, power, counts, p0=[f_o, p_o, b])
print("[fo, po, b]", params)

y_o = [saturation(i, f_o, p_o, b) for i in power]
y_list = [saturation(i, params[0], params[1], params[2]) for i in power]

background = [b*i for i in power]
sat_no_back = [i-j for i,j in zip(y_list, background)]

plt.figure(figsize=(6, 6))
plt.title(plot_title)
# plt.plot(power, y_list, label="Fit", marker="o")
# plt.plot(power, y_o, label="Fit Guess", marker="o")
plt.plot(power, counts, label="Data", marker="^")
# plt.plot(power, background, label="Background Fit", marker="o")
plt.plot(power, sat_no_back, label="Fit", marker="o")
plt.ylabel("Intensity (counts)")
plt.xlabel("mW")
# plt.yscale('log')
# plt.xscale('log')
plt.legend()
if save_bool == 1:
    plt.savefig(save_path+save_title+'.png', bbox="tight")
plt.show()
