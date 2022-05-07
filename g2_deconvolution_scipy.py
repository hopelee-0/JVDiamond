import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize
import scipy.signal

# Fitting scripts for g2 dips without any osbserved Rabi oscillations

file = '20220323_siv_transfer_717nmExcite_740BP_BS_2_8mW_WG2.dat'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220323\\'+file
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220323\\'

scan1 = np.loadtxt(path, unpack=True, skiprows=10)

plot_title = "SiV Waveguide g(2)"
save_title = "20220323_siv_waveguide_g2_fit"
save_bool = 1

dat = scan1 # Fitting code works for one data set at a time, save and then move to next
res = 128 # resolution, in ps

moveing_avg_toggle = 1 # adds moving average to the data to help reduce noise
pt_avg_num = 3 # numer of points averaged

# Procesdure Plotting toggles
all_plot = 0
aftershock_cutoff_plot = 0
dip_cutoff_plot = 0
dip_location_plot = 0
deconv_plot = 1
guess_plot = 0
arbitrary_x_fit_plot = 0
final_plot_show = 0

# Data selection
aftershock_cutoff= 1250

# Secondary data selection for 'dip cutoff plot'
b_cutoff = 1100
t_cutoff = 1250

# parameters for initial normalization and dip locating
background_range = 50
dip_location = 72

# Fitting parameter guesses, in units of 1/resolution
# g2 parameters
tau_guess = 10
b_guess = 0.5

# instrument response gaussian parameters
amp_guess = 0.05
w_guess = 20
g_back_guess = 0

# Define g2
def g2(t, tau, b):
    exponential = 1-(1-b)*np.exp(-abs((t)/tau))
    return(exponential)

# Define instrument response gaussian filter
def gaussian(t, t0):
    w = 300/res
    return(1/w/np.sqrt(2*3.14159)*np.exp(-(t-t0)**2/2/w**2))

# Define deconvolution function prior to g2 Fitting
def deconv(signal, gaussian):
    recovered, remainder = scipy.signal.deconvolve(np.asarray(signal), np.asarray(gaussian))
    return(recovered)

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

# first deconvolve to isolate actual g2 signature
gauss_plot = [gaussian(i, dip_location) for i in x_list]
filter_list = np.arange(start=0, stop=len(x_list)/5, step=1)
gauss_filter = [gaussian(i, len(x_list)//10)+0.01 for i in filter_list]
deconvolved_data = deconv(dat, gauss_filter)
print(len(deconvolved_data))

if deconv_plot == 1:
    plt.figure(figsize=(10,4))
    # plt.plot(dat_dip, marker=".", label="raw data")
    plt.plot(deconvolved_data, label="g2")
    # plt.plot(x_list, gauss_plot, label="gaussian")
    # plt.plot(filter_list, gauss_filter, label="gaussian filter")
    plt.legend()
    plt.show()

### Move onto data fitting ###
x_list = [i-dip_location for i in x_list] # center axis with offset
# First check guesses
y_guess_g2 = [g2(i, tau_guess, b_guess) for i in x_list]
y_guess_gauss = [gaussian(i) for i in x_list]
# y_guess_signal = [signal(i, tau_guess, b_guess, amp_guess, g_back_guess) for i in x_list]
y_guess_signal = signal(y_guess_g2, y_guess_gauss)

if guess_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(x_list, dat_dip, marker=".")
    plt.plot(x_list, y_guess_g2, label="g2")
    plt.plot(x_list, y_guess_gauss, label="gaussian")
    plt.plot(x_list, y_guess_signal, label="signal")
    plt.legend()
    plt.show()

params, params_covariance = optimize.curve_fit(signal, x_list, dat_dip,
                                                p0=[tau_guess, b_guess],
                                                bounds=(0.0, np.inf))

plot_x_list = np.linspace(x_list[0], x_list[-1], 3000)
y_fit_g2 = [g2(i, params[0], params[1]) for i in plot_x_list]
y_fit_gauss = [gaussian(i, params[2], params[3]) for i in plot_x_list]
y_fit_signal = [signal(i, params[0], params[1], params[2], params[3]) for i in plot_x_list]

if arbitrary_x_fit_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(x_list, dat_dip, marker=".")
    plt.plot(plot_x_list, y_fit_g2, label="g2")
    plt.plot(plot_x_list, y_fit_gauss, label="gaussian")
    plt.plot(plot_x_list, y_fit_signal, label="signal")
    plt.ylabel("Normalized Relative Counts")
    plt.xlabel("Arbitrary Binning Units")
    plt.legend()
    plt.show()

print("Results")
print("Raw Parameters:{}".format(params))
print(" ")
print("tau (ps): {:}".format(params[0]*res))
print("g0: {:}".format(params[1]))
print("Gaussian amp: {:}".format(params[2]))
# print("Gaussian FWHM: {:}".format(params[3]))
# print("Gaussian background: {:}".format(params[4]))

time_list = [res*i for i in x_list]
plot_time_list = [res*i for i in plot_x_list] # calibration of x-axis to have meaningful units
plt.figure(figsize=(10,4))
plt.scatter(time_list, dat_dip, label="Data", marker=".", c="C0")
plt.plot(plot_time_list, y_fit_signal, label="Fit Function", c="C1")
plt.plot(plot_time_list, y_fit_g2, label="Fit Function, g2, dip={:.2}".format(params[1]), c="C2")
plt.plot(plot_time_list, y_fit_gauss, label="Fit Function, Gaussian", c="C3")
plt.ylabel("Normalized Relative Counts")
plt.xlabel("Time Offset (ps)")
plt.legend()
plt.title(plot_title)
if save_bool == 1:
    plt.savefig(save_path+save_title+'.png')
if final_plot_show == 1:
    plt.show()

# Write results to text file to save
if save_bool == 1:
    f = open(save_path+save_title+".txt", "w")
    f.write(plot_title+"\n")
    if moveing_avg_toggle == 1:
        f.write("Moving Average Number of Points:{}\n".format(pt_avg_num))
    f.write("\n")
    f.write("Raw Parameters:{}\n".format(params))
    f.write("\n")
    f.write("tau (ps): {:}\n".format(params[0]*res))
    f.write("g0: {:}\n".format(params[1]))
    f.write("Gaussian amp: {:}".format(params[2]))
    f.write("Gaussian FWHM: {:}".format(params[3]))
    # f.write("Gaussian background: {:}".format(params[4]))
    f.close()
