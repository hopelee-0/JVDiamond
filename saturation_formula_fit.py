import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

# Enter Data
file = '20220323_SiV_linewidths.csv'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220323\\'+file

save_title = "EL_5_Disk_PL_5.png"
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220302\\El5_Disks\\'+save_title

plot_title = "SiV Linewidth, D Transition"
save_title = "save_title.png"
save_bool = 0

# Enter parameter guesses
p_o = 10
f_o = 1
b = 0.001

power, counts1, counts = np.loadtxt(path, unpack=True, skiprows=0, delimiter=",")

def saturation(power, f_o, p_o, b):
    return(f_o*power/(p_o+power)+b*power)

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
# plt.plot(power, sat_no_back, label="Fit", marker="o")
plt.ylabel("Linewidth (nm)")
plt.xlabel("W")
# plt.yscale('log')
# plt.xscale('log')
plt.legend()
if save_bool == 1:
    plt.savefig(save_path+save_title+'.png', bbox="tight")
plt.show()
