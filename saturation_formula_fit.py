import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize
from os import listdir
from os.path import isfile,join

# Enter Data
file1 = '202211214_Confocal_PL00.txt'
file2 = '202211214_Coupler_PL00.txt'
file3 = '202211214_Confocal_PL00.txt'

save_title1 = "202211214_Confocal_PL00_sat"
save_title2 = "202211214_Coupler_PL00_sat"
save_title3 = "202211214_Confocal_PL00_sat"

plot_title1 = "SiV Saturation Curve, Confocal"
plot_title2 = "SiV Saturation Curve, Coupler Collect"
plot_title3 = "SiV Saturation Curve, Confocal"

path = "G:/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20221214/"
save_path = "G:/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20221214/"

save_bool = 0

log_bool = 0
plot_max = 15

# Enter parameter guesses
p_o = 3
f_o = 10000
a = 1
b = 150

counts1 = np.loadtxt(path+file1, skiprows=1, usecols=1)
# power1 = [10.3, 11.4, 9.7, 8.8, 7.6, 6.7, 5.5,
#         4.2, 3.25, 2.55, 1.9, 1.35, 0.9, 0.565,
#         0.335, 0.2, 0.106, 0.056, 0.029, 0.015, 0, 0.008]
# #
# power1 = [10.4, 11.3, 9.5, 8.3, 7.85, 6.5, 5.2,
#             4.2, 3.35, 2.6, 2, 1.3, 0.880, 0.575,
#             0.350, 0.195, 0.110, 0.059, 0.029, 0.015,
#             0.007, 0]

power1 = [5.2, 3.55, 31, 21.8, 16.9, 7.9, 13.8, 11.5, 0, 0.150, 0.285, 0.51, 0.9, 1.52, 2.38]

# power1 = [6.75,5.35,4.25,3.35,3.2,2.25,1.75,1.145,0.89,0.4285,0.2715,0.117,0.062,0.032,0.018,0.0072,0]

# power1 = [8.7, 8.07, 12.5, 10, 10.6, 12.5, 17.7, 19.1, 22.4, 6.68, 3.77, 0, 0.007, 0.014,
#             0.027, 0.042, 0.06, 0.225, 0.410, 0.547, 0.920, 0.715,
#             1.16, 1.36, 1.78, 2.16, 2.88]

# power2 = [0, 0.0178, 0.034, 0.07, 0.13, 0.23, 0.405, 0.67, 0.83,
#         1.56, 2.09, 3, 3.96, 5, 5.78, 7.65, 9.9, 11.2, 13.5]

# power1 = [7.5, 5.4, 4.6, 3.5, 2.6, 2.0, 1.7, 1.3, 0.88,
#             0.41, 0.27, 0.12, 0.06, 0.03, 0.02, 0.007, 0]

power2 = [31, 26, 14, 0.28, 0.11, 0.7, 1.5, 2.4, 3.4, 10.3, 6.5, 5.2]


counts2 = np.loadtxt(path+file2, skiprows=1, usecols=1)
# power2 = [0, 0.02, 0.038, 0.067, 0.136, 0.245, 0.385,
#             0.575, 0.883, 1.03, 1.56, 2.22, 2.61, 3.5,
#             4.45, 5.5, 7.45, 9.01]
# power2 = [3.2, 4.3, 5.85, 7.92, 9.54, 12.2, 14.5, 16.1, 19.4, 22.1,19.1,
#         2.22, 1.53, 1.14, 0.870, 0.695, 0.513, 0.403, 0.282, 0.207,
#         0.102, 0.055, 0.029, 0.014, 0.007, 0.00]

# power1 = [13.5, 11.36, 9.5, 8.23, 7.27, 0.0685, 0.0358, 0.840,
#         0.530, 0.410, 0.230, 0, 0.0174, 0.132, 1.38, 2.02,
#         2.86, 3.9, 5.02, 6.01]

# power2 = power1

counts3 = np.loadtxt(path+file3, skiprows=1, usecols=1)
# power3 = [0, 0.0178, 0.034, 0.07, 0.13, 0.23,
#             0.405, 0.67, 0.83, 1.56, 2.09,
#             3.0, 3.96, 5.0, 5.78, 7.65, 9.9,
#             11.2, 13.5]
power3 = [4.14, 4.67, 3.5, 2.85, 2.0, 1.1, 0.9, 0.62, 0.49, 0.43, 0.27, 0.19, 0.11, 0.063, 0, 0.010, 0.020, 0.039]
# power3 = [0.405, 0.680, 1.01, 2.15, 3.3, 5.9, 7, 0.25, 0.006, 0.012, 0.071, 0.190, 0]

# power3 = [0, 0.02, 0.038, 0.067, 0.136, 0.245, 0.385, 0.575,
#         0.883, 1.03, 1.56, 2.22, 2.61, 3.5, 4.45, 5.5, 7.45, 9.01]

power3 = power1 

# additional normalizations if needed
power1 = [i*0.9*0.5 for i in power1]
counts1 = [i/0.9 for i in counts1]

power2 = [i*0.9*0.5 for i in power2]
counts2 = [i/0.9 for i in counts2]

power3 = power1
counts3 = counts1

def saturation(power, f_o, p_o, a, b):
    return(f_o*power/(p_o+power)+a*power+b)

def sat_fit(counts, power, f_o, p_o, a, b, save_title):
    params, params_covariance1 = optimize.curve_fit(saturation, power, counts, p0=[f_o, p_o, a, b], bounds=([0.0, 0.0, 0.00, 0.0],[np.inf, np.inf, np.inf, np.inf]))
    print("f_o, p_o, a, b: ", params)
    if save_bool == 1:
        f = open(save_path+save_title+"_meta.txt", "w")
        f.write(save_title+"\n")
        f.write("f_o: {:.3f}\n".format(params[0]))
        f.write("p_o: {:.3f}\n".format(params[1]))
        f.write("a: {:.3f}\n".format(params[2]))
        f.write("b: {:.3f}\n".format(params[3]))
        f.close()
    return(params)

def plot_lists(counts, power, params, plot_max):
    # finer list of x-values for plotting to smooth out curves
    plot_range = np.linspace(0, plot_max, 100)
    y_list = [saturation(i, params[0], params[1], params[2], params[3]) for i in plot_range]

    # remove background to extract only saturation behavior
    background = [params[2]*i+params[3] for i in plot_range]
    sat_no_back = [i-j for i,j in zip(y_list, background)]
    return(plot_range, y_list, background, sat_no_back)

def fit_check(counts, power, params, save_title, plot_title, plot_max, log_bool):

    plot_range, y_list, background, sat_no_back = plot_lists(counts, power, params, plot_max)

    plt.figure(figsize=(8, 6))
    plt.title(plot_title, y=1.08)
    plt.plot(plot_range, background, label="Background")
    plt.plot(plot_range, y_list, label="Confocal Fit", color='C1', linestyle='--')
    plt.scatter(power, counts, label="Confocal Data", marker="^", color='k')
    plt.plot(plot_range, sat_no_back, label="Confocal Fit, Background Removed")
    plt.ylabel("Intensity (cps)")
    plt.xlabel("mW")
    if log_bool == 1:
        plt.yscale('log')
    else:
        plt.ticklabel_format(style='sci', scilimits=(0,0))
    plt.legend()
    if save_bool == 1:
        plt.savefig(save_path+save_title+".png")
    plt.show()
    return()

params1 = sat_fit(counts1, power1, f_o, p_o, a, b, save_title1)
plot_range_A, y_list_A, background_A, sat_no_back_A = plot_lists(counts1, power1, params1, plot_max)
# fit_check(counts1, power1, params1, save_title1, plot_title1, plot_max, log_bool)

params2 = sat_fit(counts2, power2, f_o, p_o, a, b, save_title2)
plot_range_B, y_list_B, background_B, sat_no_back_B = plot_lists(counts2, power2, params2, plot_max)
# fit_check(counts2, power2, params2, save_title2, plot_title2, plot_max, log_bool)

params3 = sat_fit(counts3, power3, f_o, p_o, a, b, save_title3)
plot_range_C, y_list_C, background_C, sat_no_back_C = plot_lists(counts3, power3, params3, plot_max)
# fit_check(counts3, power3, params3, save_title3, plot_title3, plot_max, log_bool)

# additional plotting for figures
plt.plot(figsize=(12,12))
# plt.title("Emitter 1", y=1.08)
plt.plot(plot_range_B, y_list_B, color='r')
plt.plot(plot_range_C, y_list_C, color='b')
plt.plot(plot_range_B, sat_no_back_B, color='r', linestyle='--')
plt.plot(plot_range_C, sat_no_back_C, color='b', linestyle='--')
plt.scatter(power2, counts2,  marker="o", color='k')
plt.scatter(power3, counts3,  marker="o", color='k')
plt.ylabel("Intensity (cps)")
plt.xlabel("mW")
# plt.ylim(plot_max)
# plt.legend()
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.show()
