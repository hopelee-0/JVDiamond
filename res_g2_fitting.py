import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

# Fitting scripts for g2 dips without any osbserved Rabi oscillations

file = '20210714_El15_R7D7_res_g2_r1p6uW_g1p6uW.dat'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210714\\'+file
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210721\\'
scan1 = np.loadtxt(path, unpack=True, skiprows=10)

plot_title = "Resonant g2, 1.6uW Red/ 1.6uW Green"
save_title = "20210721_res_g2_r1p6uW_g1p6uW"
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
arbitrary_x_fit_plot = 0
final_plot_show = 1

# Data selection
aftershock_cutoff= 1250

b_cutoff = 500
t_cutoff = 900

background_range = 110
dip_location = 205

# Fitting parameter guesses, in units of 1/resolution
tau_guess = 100
b_guess = 0.1

# Define g2 with Rabi expression, added scaling to sinusoidal to account for nonideal dip
def g2(t, tau, b):
    exponential = 1-(1-b)*np.exp(-abs((t)/tau))
    return(exponential)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid')

if moveing_avg_toggle == 1:
    dat = moving_average(dat, pt_avg_num)

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

### Move onto data fitting ###

# First check guesses
y_guess = [g2(i, tau_guess, b_guess) for i in x_list]

if guess_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(x_list, dat_dip, marker=".")
    plt.plot(x_list, y_guess)
    plt.show()

params, params_covariance = optimize.curve_fit(g2, x_list, dat_dip,
                                                p0=[tau_guess, b_guess],
                                                bounds=(0.0, np.inf))


y_fit = [g2(i, params[0], params[1]) for i in x_list]

if arbitrary_x_fit_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(x_list, dat_dip, marker=".")
    plt.plot(x_list, y_fit)
    plt.ylabel("Normalized Relative Counts")
    plt.xlabel("Arbitrary Binning Units")
    plt.show()

print("Results")
print("Raw Parameters:{}".format(params))
print(" ")
print("tau (ps): {:}".format(params[0]*res))
print("g0: {:}".format(params[1]))

time_list = [res*i for i in x_list] # calibration of x-axis to have meaningful units
plt.figure(figsize=(10,4))
plt.scatter(time_list, dat_dip, label="Data", marker=".", c="C0")
plt.plot(time_list, y_fit, label="Fit Function", c="C1")
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
    f.close()
