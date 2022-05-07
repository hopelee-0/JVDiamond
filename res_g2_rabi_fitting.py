import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

# Fitting script for g2 dips with observed Rabi oscillations

file = '20210720_EL15_R6D7_res_g2_r6p7uW_g0p67uW_2.dat'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210721\\'+file
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210721\\'
scan1 = np.loadtxt(path, unpack=True, skiprows=10)

plot_title = "Resonant g2 Rabi, 6.7uW Red/ 0.67uW Green"
save_title = "20210721_res_g2_rabi_r6p7uW_g0p67uW_2"
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
aftershock_cutoff= 2000

b_cutoff = 1150
t_cutoff = 1680

background_range = 110
dip_location = 264

# Fitting parameter guesses, in units of 1/resolution
omega_R_guess = 0.1
gamma_1_guess = 0.05
gamma_2_guess =  0.04
b_guess = 0.5

# Define g2 with Rabi expression, added scaling to sinusoidal to account for nonideal dip
def g2_Rabi(t, omega_R, gamma_1, gamma_2, b):
    omega_damp = np.sqrt(omega_R**2-(gamma_1-gamma_2)**2/4)
    sinusoidal = (np.cos(omega_damp*t)+(gamma_1+gamma_2)/(2*omega_damp)*np.sin(omega_damp*abs(t)))*b
    exponential = np.exp(-1/2*(gamma_1+gamma_2)*abs(t))
    return(1-sinusoidal*exponential)

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
y_guess = [g2_Rabi(i, omega_R_guess, gamma_1_guess, gamma_2_guess, b_guess) for i in x_list]

if guess_plot == 1:
    plt.figure(figsize=(10,4))
    plt.plot(x_list, dat_dip, marker=".")
    plt.plot(x_list, y_guess)
    plt.show()

params, params_covariance = optimize.curve_fit(g2_Rabi, x_list, dat_dip,
                                                p0=[omega_R_guess, gamma_1_guess, gamma_2_guess, b_guess],
                                                bounds=(0.0, np.inf))


y_fit = [g2_Rabi(i, params[0], params[1], params[2], params[3]) for i in x_list]

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
print("Omega Rabi(radians): {:}".format(params[0]/res))
print("Gamma1(1/ps): {:}".format(params[1]/res))
print("Gamma2(1/ps): {:}".format(params[2]/res))
print("Background: {:}".format(params[3]))

print("")

print("Omega Rabi (THz): {:}".format(params[0]/res/2/np.pi))
print("T1 (ps): {:}".format(1/params[1]/res))
print("T2 (ps): {:}".format(1/params[2]/res))
print("Background: {:}".format(params[3]))

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
    f.write("Omega Rabi(radians): {:}\n".format(params[0]/res))
    f.write("Gamma1(1/ps): {:}\n".format(params[1]/res))
    f.write("Gamma2(1/ps): {:}\n".format(params[2]/res))
    f.write("Background: {:}\n".format(params[3]))
    f.write("\n")
    f.write("Omega Rabi (THz): {:}\n".format(params[0]/res/2/np.pi))
    f.write("T1 (ps): {:}\n".format(1/params[1]/res))
    f.write("T2 (ps): {:}\n".format(1/params[2]/res))
    f.write("Background: {:}\n".format(params[3]))
    f.close()
