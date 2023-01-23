import matplotlib.pyplot as plt
import scipy.optimize as optimize
import numpy as np
from matplotlib import gridspec

# Fitting scripts for g2 dips without any osbserved Rabi oscillations

file1 = '20221104_8p35mW_2000sint_couplers_PL00.sint.dat'
file2 = '20221104_6p15mW_couplers_PL00.sint.dat'
file3 = '20221104_5p3mW_couplers_PL00.sint.dat'
file4 = '20221104_4p15mW_couplers_PL00.sint.dat'
file5 = '20221104_3p3mW_couplers_PL00.sint.dat'
file6 = '20221104_2p45mW_couplers_PL00.sint.dat'
file7 = '20221104_1p035mW_couplers_PL00.sint.dat'

path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221104_LND03\\g2\\PL 00\\"
save_path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221104_LND03\\g2\\PL 00\\"

plot_title = "g2, Coupler Detection"
save_title = "g2_coupler_PL00"
save_bool = 0

scan1 = np.loadtxt(path+file1, unpack=True, skiprows=10)
scan2 = np.loadtxt(path+file2, unpack=True, skiprows=10)
scan3 = np.loadtxt(path+file3, unpack=True, skiprows=10)
scan4 = np.loadtxt(path+file4, unpack=True, skiprows=10)
scan5 = np.loadtxt(path+file5, unpack=True, skiprows=10)
scan6 = np.loadtxt(path+file6, unpack=True, skiprows=10)
scan7 = np.loadtxt(path+file7, unpack=True, skiprows=10)

dat = scan4 # set of data used to check plotting parameters
res = 64 # resolution, in ps

smoothing_toggle = 1

# Procesdure Plotting toggles
plot_check = 0
all_plot = 0
aftershock_cutoff_plot = 1
dip_cutoff_plot = 1
dip_location_plot = 1

# Data selection
aftershock_cutoff= 5000

b_cutoff = 1700
t_cutoff = 3300

background_range = 110
dip_location = 1510

# Define g2 with Rabi expression, added scaling to sinusoidal to account for nonideal dip
def g2(t, tau, b):
    exponential = 1-(1-b)*np.exp(-abs((t)/tau))
    return(exponential)

def aftershock_cutoff_func(data):
    return(data[0:aftershock_cutoff])

def dip_cutoff_func(data):
    return(data[b_cutoff: t_cutoff])

def normalize(data):
    dat_dip_background = np.average([*data[0:background_range], *data[-background_range:]]) # determine background
    return([i/dat_dip_background for i in data]) # normalize data

def x_list(data):
    x = range(len(data))
    x = [i-dip_location for i in x] # center axis with offset
    return(x)

def processed_data(data):
    data = aftershock_cutoff_func(data)
    data = dip_cutoff_func(data)
    data_dip = normalize(data)
    return(data_dip)

# series of optional plots for checking data trimming and plot Parameters
if plot_check == 1:
    if all_plot == 1:
        plt.figure(figsize=(10,4))
        plt.plot(dat)
        plt.show()

    # Use aftershock feature as a starting cutoff point
    dat = aftershock_cutoff_func(dat)

    if aftershock_cutoff_plot == 1:
        plt.figure(figsize=(10,4))
        plt.plot(dat)
        plt.show()

    # From selected data, now more carefully select around the actual dip
    dat_dip = dip_cutoff_func(dat)

    if dip_cutoff_plot == 1:
        plt.figure(figsize=(10,4))
        plt.plot(dat_dip)
        plt.show()

    # First to find the background and to select dip location
    dat_dip = normalize(dat_dip)

    if dip_location_plot == 1:
        plt.figure(figsize=(10,4))
        plt.plot(dat_dip)
        plt.vlines(dip_location, min(dat_dip), max(dat_dip), colors="red")
        plt.show()


# now processing for each scan
data1 = processed_data(scan1)
x_coord = x_list(data1)
data2 = processed_data(scan2)
data3 = processed_data(scan3)
data5 = processed_data(scan5)
data6 = processed_data(scan6)
data7 = processed_data(scan7)

b_cutoff = 1900
t_cutoff = 3200
dip_location = 671
data4 = processed_data(scan4)
x_shift = x_list(data4)

# plotting all figures stacked with shared x axis
fig = plt.figure(figsize=(6,12))
plt.subplots_adjust(hspace=0)
gs = gridspec.GridSpec(7, 1)

ax0 = plt.subplot(gs[0])
line0, = ax0.plot(x_coord, data1)
ax0.set_xticks([])
ax0.set_yticks([0, 1])
ax0.set_ylim(-0.3, 1.75)

ax1 = plt.subplot(gs[1])
line1, = ax1.plot(x_coord, data2)
ax1.set_xticks([])
ax1.set_yticks([0, 1])
ax1.set_ylim(-0.3, 1.75)

ax2 = plt.subplot(gs[2])
line2, = ax2.plot(x_coord, data3)
ax2.set_xticks([])
ax2.set_yticks([0, 1])
ax2.set_ylim(-0.3, 1.75)

ax3 = plt.subplot(gs[3])
line3, = ax3.plot(x_shift, data4)
ax3.set_xticks([])
ax3.set_yticks([0, 1])
ax3.set_ylim(-0.3, 1.75)

ax4 = plt.subplot(gs[4])
line4, = ax4.plot(x_coord, data5)
ax4.set_xticks([])
ax4.set_yticks([0, 1])
ax4.set_ylim(-0.3, 1.75)

ax5 = plt.subplot(gs[5])
line5, = ax5.plot(x_coord, data6)
ax5.set_xticks([])
ax5.set_yticks([0, 1])
ax5.set_ylim(-0.3, 1.75)

ax6 = plt.subplot(gs[6])
line6, = ax6.plot(x_coord, data7)
ax6.set_xticks([])
ax6.set_yticks([0, 1])
ax6.set_ylim(-0.3, 1.75)

plt.show()
