import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import scipy.integrate as integrate
import scipy.special as special
from scipy.interpolate import UnivariateSpline

from scipy import optimize
from scipy.optimize import curve_fit

# Fitting scripts for g2 dips without any osbserved Rabi oscillations

# file = '20221104_2p45mW_couplers_PL00.sint.dat'
file = '20221108_PL00_6mW.sint.dat'
# path = "/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20221104_LND03/g2/PL 00/"+file
path = "/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20221108_LND03/"+file
save_path = "/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20221108_LND03/"

scan1 = np.loadtxt(path, unpack=True, skiprows=10)

plot_title = "g2, Confocal"
save_title = "g2_confocal_PL00"
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
guess_plot = 0
arbitrary_x_fit_plot = 0
final_plot_show = 1

# Data selection
aftershock_cutoff= 1000

# Secondary data selection for 'dip cutoff plot'
b_cutoff = 200
t_cutoff = 900

# parameters for initial normalization and dip locating
background_range = 340
dip_location = 353

# Fitting parameter guesses, in units of 1/resolution
# g2 parameters
tau0_guess = 10
g20_guess = 0.2

# define functions
def g2_convolved_gaussian(tau, a, tau_offset, tau0, g20, stdev):
    #tau - independent variable. delay.
    #a - normalization value. value at tau--> inf.
    #tau_offset - offset of dip on x axis.
    #tau0 - lifetime
    #g20 - g^(2)[0] value
    #stdev - standard deviation of gaussian
    f = 1+1/2*np.e**((stdev**2-2*tau0*(tau-tau_offset))/(2*tau0**2))*(-1+g20)*(special.erfc((stdev**2-tau0*(tau-tau_offset))/(np.sqrt(2)*stdev*tau0))+np.e**((2*(tau-tau_offset))/tau0)*special.erfc((stdev**2+tau0*(tau-tau_offset))/(np.sqrt(2)*stdev*tau0)))
    return a*f
# return (np.sqrt(2*np.pi)/np.sqrt(1/stdev**2)+(np.e**(stdev**2/(2*tau0**2)-(tau-tau_offset)/tau0)*(1-g20)*np.sqrt(np.pi/2)*(-1-np.e**((2*(tau-tau_offset))/tau0)+np.sqrt(1/stdev**2)*stdev*special.erf((stdev**2-tau0*(tau-tau_offset))/(np.sqrt(2)*stdev*tau0))+np.e**((2*(tau-tau_offset))/tau0)*np.sqrt(1/stdev**2)*stdev*special.erf((stdev**2+tau0*(tau-tau_offset))/(np.sqrt(2)*stdev*tau0))))/np.sqrt(1/stdev**2))/(np.sqrt(2*np.pi)*stdev)

def g2_convolved_gaussian_simpler(tau, tau0, g20):
    #tau - independent variable. delay.
    #a - normalization value. value at tau--> inf.
    #tau_offset - offset of dip on x axis.
    #tau0 - lifetime
    #g20 - g^(2)[0] value
    #stdev - standard deviation of gaussian
    return g2_convolved_gaussian(tau, 1, 0, tau0 , g20, 300/res) #0.92360631


def g2(tau, a, tau_offset, tau0, g20):
    #tau - independent variable. delay.
    #a - normalization value. value at tau--> inf.
    #tau_offset - offset of dip on x axis.
    #tau0 - lifetime
    #g20 - g^(2)[0] value
    return a*(1-(1-g20)*np.e**(-np.abs(tau-tau_offset)/tau0))


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
dat_dip_background = np.average([*dat_dip[320:background_range], *dat_dip[-background_range:]]) # determine background
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
y_guess_g2 = [g2(i, 1, 0, tau0_guess, g20_guess) for i in x_list]
y_guess_signal = [g2_convolved_gaussian_simpler(i, tau0_guess, g20_guess) for i in x_list]

if guess_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(x_list, dat_dip, marker=".")
    plt.plot(x_list, y_guess_g2, label="g2")
    plt.plot(x_list, y_guess_signal, label="signal")
    plt.legend()
    plt.show()

params, params_covariance = optimize.curve_fit(g2_convolved_gaussian_simpler, x_list, dat_dip,
                                                p0=[tau0_guess, g20_guess],
                                                bounds=(0.0, np.inf))

plot_x_list = np.linspace(x_list[0], x_list[-1], 12000)
y_fit_g2 = [g2(i, 1, 0, params[0], params[1]) for i in plot_x_list]
y_fit_signal = [g2_convolved_gaussian_simpler(i, params[0], params[1]) for i in plot_x_list]

if arbitrary_x_fit_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(x_list, dat_dip, marker=".")
    plt.plot(plot_x_list, y_fit_g2, label="g2")
    plt.plot(plot_x_list, y_fit_signal, label="signal")
    plt.ylabel("Normalized Relative Counts")
    plt.xlabel("Arbitrary Binning Units")
    plt.xlim(-200,200)
    plt.legend()
    plt.show()

print("Results")
print("Raw Parameters:{}".format(params))
print(" ")
print("tau (ps): {:}".format(params[0]*res))
print("g0: {:}".format(params[1]))

time_list = [res*i/1000 for i in x_list]
plot_time_list = [res*i/1000 for i in plot_x_list] # calibration of x-axis to have meaningful units
plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(5,4))
plt.scatter(time_list, dat_dip, marker=".", c="k")
plt.plot(plot_time_list, y_fit_signal, label="$g_2 (0)$={:.2}".format(min(y_fit_signal)), c="r")
plt.plot(plot_time_list, y_fit_g2, label="$g_2 (0)$ with Deconvolution={:.2}".format(params[1]), c="b")
plt.axhline(y=0.5, linestyle="--", color='k')
plt.ylabel("Normalized Relative Counts")
plt.xlabel("Time Offset (ns)")
plt.ylim(0.0, 1.3)
plt.legend(loc='lower left')
plt.xlim(-5,5)
# plt.title("Confocal Detection")
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
    f.write("tau (ps): {:}\n".format(params[1]*res))
    f.write("g0: {:}\n".format(params[1]))
    f.close()
