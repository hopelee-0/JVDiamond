import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import numpy.fft as fft
import scipy.integrate as integrate
import scipy.special as special
from scipy.interpolate import UnivariateSpline

from scipy import optimize
from scipy.optimize import curve_fit

# Fitting scripts for g2 dips without any osbserved Rabi oscillations

file = '20221104_8p35mW_2000sint_couplers_PL00.sint.dat'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221104_LND03\\g2\\"+file
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221104_LND03\\g2\\processed\\"

scan1 = np.loadtxt(path, unpack=True, skiprows=10)

plot_title = "g2, Coupler Detection"
save_title = "g2_coupler_01"
save_bool = 0

dat = scan1 # Fitting code works for one data set at a time, save and then move to next
res = 64 # resolution, in ps

moveing_avg_toggle = 1 # adds moving average to the data to help reduce noise
pt_avg_num = 3 # numer of points averaged

# Procesdure Plotting toggles
all_plot = 0
aftershock_cutoff_plot = 0
dip_cutoff_plot = 0
dip_location_plot = 0
guess_plot = 1
arbitrary_x_fit_plot = 1
final_plot_show = 0

# Data selection
aftershock_cutoff= 5000

# Secondary data selection for 'dip cutoff plot'
b_cutoff = 1000
t_cutoff = 4000

# parameters for initial normalization and dip locating
background_range = 300
dip_location = 1515

# Fitting parameter guesses, in units of 1/resolution
# g2 parameters
tau0_guess = 10
tau1_guess = 500
g20_guess = 0.2
a_guess = 1.3

# define functions
def g2(tau, a, tau_offset, tau0, g20):
    return a*(1-(1-g20)*np.e**(-np.abs(tau-tau_offset)/tau0))

def g2_bunched(tau, a, tau0, tau1, g20):
    tau = np.abs(tau)
    return(a*(np.e**(-tau/tau1))*(1-(1-g20)*np.e**(-tau/tau0)))

def gaussian(tau, tau0, stdev):
    return (((1/stdev/np.sqrt(2*np.pi))*np.exp(-((tau-tau0)/stdev)**2/2)))
    # return np.exp(-((tau-tau0)/stdev)**2/2)

if all_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(dat)
    plt.show()

# Use aftershock feature as a starting cutoff point
dat = dat[0:aftershock_cutoff]

if aftershock_cutoff_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(dat)
    plt.show()

# From selected data, now more carefully select around the actual dip
dat_dip = dat[b_cutoff: t_cutoff]

if dip_cutoff_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(dat_dip)
    plt.show()

# First to find the background and to select dip location
dat_dip_background = np.average([*dat_dip[0:background_range], *dat_dip[-background_range:]]) # determine background
dat_dip = [i/dat_dip_background for i in dat_dip] # normalize data
x_list = range(len(dat_dip)) # create an x-axis list, currently arbitrary units, later will calibrate

if dip_location_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(dat_dip)
    plt.vlines(dip_location, min(dat_dip), max(dat_dip), colors="red")
    plt.show()

x_list = [i-dip_location for i in x_list] # center axis with offset

# deconvolve gaussian from Data
print(len(x_list))
x_gauss = x_list
gauss = [gaussian(i, np.mean(x_gauss), 350/res) for i in x_gauss]
print(np.min(gauss))

# plt.plot(x_list, dat_dip)
# plt.plot(x_gauss, gauss)
# plt.show()

smoothed = signal.savgol_filter(dat_dip, 11, 2)
fft_smooth = fft.fft(smoothed)
fft_gauss  = fft.fft(gauss)
epsilon=100
ratio = fft_smooth/(fft_gauss+epsilon)
print(ratio)

inverse_ratio = fft.ifft(ratio)


#deconv,  _ = signal.deconvolve(smoothed, gauss)
##smooth_deconv = signal.savgol_filter(deconv, 11, 2)
#recover=signal.convolve(deconv,gauss)
#print(len(deconv))
#plt.plot(x_list, dat_dip)
# plt.plot(x_gauss, gauss)
plt.plot(x_list, abs(inverse_ratio))
plt.plot(x_list,fft_smooth)
print(inverse_ratio)
# plt.plot(x_list,recover)
# plt.plot(x_list[0:-1],np.pad(deconv,(np.abs(len(deconv)-len(x_list))//2)))
# plt.scatter(range(len(deconv)),deconv)
# plt.plot(x_list, smoothed)
# plt.ylim(-10, 20)
plt.show()


# ### Move onto data fitting ###
#
# # First check guesses
# y_guess_g2 = [g2_bunched(i, a_guess, tau0_guess, tau1_guess, g20_guess) for i in x_list]
# y_guess_signal = [g2_convolved_gaussian_bunched_simpler(i, a_guess, tau0_guess, tau1_guess, g20_guess) for i in x_list]
#
# if guess_plot == 1:
#     plt.figure(figsize=(10,4))
#     plt.plot(x_list, dat_dip, marker=".")
#     plt.plot(x_list, y_guess_g2, label="g2")
#     plt.plot(x_list, y_guess_signal, label="signal")
#     plt.plot(x_list, gaussian(x_list), label="Gaussian")
#     plt.legend()
#     plt.show()
#
# params, params_covariance = optimize.curve_fit(g2_bunched, x_list, dat_dip,
#                                                 p0=[a_guess, tau0_guess, tau1_guess, g20_guess],
#                                                 bounds=(0.0, np.inf))
#
# plot_x_list = np.linspace(x_list[0], x_list[-1], 3000)
# y_fit_g2 = [g2_bunched(i, params[0], params[1], params[2], params[3]) for i in plot_x_list]
# # y_fit_signal = [g2_convolved_gaussian_simpler(i, params[0], params[1], params[2], params[3]) for i in plot_x_list]
#
#
# if arbitrary_x_fit_plot == 1:
#     plt.figure(figsize=(10,4))
#     plt.plot(x_list, dat_dip, marker=".")
#     plt.plot(plot_x_list, y_fit_g2, label="g2")
#     # plt.plot(plot_x_list, y_fit_signal, label="signal")
#     plt.ylabel("Normalized Relative Counts")
#     plt.xlabel("Arbitrary Binning Units")
#     plt.legend()
#     plt.show()
#
# print("Results")
# print("Raw Parameters:{}".format(params))
# print(" ")
# print("tau (ps): {:}".format(params[0]*res))
# print("g0: {:}".format(params[1]))
# #
# # time_list = [res*i/1000 for i in x_list]
# # plot_time_list = [res*i/1000 for i in plot_x_list] # calibration of x-axis to have meaningful units
# # plt.rcParams.update({'font.size': 12})
# # plt.figure(figsize=(10,4.5))
# # plt.scatter(time_list, dat_dip, label="Data", marker=".", c="C0")
# # plt.plot(plot_time_list, y_fit_signal, label="Fit Function, Convolved, dip={:.2}".format(min(y_fit_signal)), c="C1")
# # # plt.plot(plot_time_list, y_fit_g2, label="Fit Function, g2, dip={:.2}".format(params[1]), c="C2")
# # plt.ylabel("Normalized Relative Counts")
# # plt.xlabel("Time Offset (ns)")
# # plt.ylim(0.0, 1.5)
# # plt.legend()
# # plt.title(plot_title)
# # if save_bool == 1:
# #     plt.savefig(save_path+save_title+'.png')
# # if final_plot_show == 1:
# #     plt.show()
# #
# # # Write results to text file to save
# # if save_bool == 1:
# #     f = open(save_path+save_title+".txt", "w")
# #     f.write(plot_title+"\n")
# #     if moveing_avg_toggle == 1:
# #         f.write("Moving Average Number of Points:{}\n".format(pt_avg_num))
# #     f.write("\n")
# #     f.write("Raw Parameters:{}\n".format(params))
# #     f.write("\n")
# #     f.write("tau (ps): {:}\n".format(params[1]*res))
# #     f.write("g0: {:}\n".format(params[2]))
# #     f.close()
