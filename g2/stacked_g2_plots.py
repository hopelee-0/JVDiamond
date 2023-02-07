import numpy as np
import matplotlib.pyplot as plt

# Stacked g2 plots in order for comparison

# Import data from PLE files to temp
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210714\\'
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210715\\'

file = '20210714_EL15_R7D7_res_g2_r0p6uW_g1p6uW.dat'
data1 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r1p3uW_g1p6uW.dat'
data2 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r1p6uW_g1p6uW.dat'
data3 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r2p4uW_g1p6uW.dat'
data4 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r3p1uW_g1p6uW.dat'
data5 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r4p8uW_g1p6uW.dat'
data6 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r9p5uW_g1p6uW.dat'
data7 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r15p9uW_g1p6uW.dat'
data8 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r31p7uW_g1p6uW.dat'
data9 = np.loadtxt(path+file, unpack=True, skiprows=10)

file = '20210714_EL15_R7D7_res_g2_r63p7uW_g1p6uW.dat'
data10 = np.loadtxt(path+file, unpack=True, skiprows=10)


data_all = [data1, data1, data3, data4, data5, data6, data7, data8, data9, data10] # populate with all data sets
label_all = ["0.6uW", "1.3uW", "1.6uW", "2.4uW", "3.1uW", "4.8uW", "9.5uW", "15.9uW", "31.7uW", "63.7uW"] # populate with all labels

plot_title = "Stacked g2 Plots, EL15 R7 D7"
save_title = "20210715_res_g2_EL15_R7D7_stacked"
save_bool = 1

moveing_avg_toggle = 1 # adds moving average to the data to help reduce noise
pt_avg_num = 5 # numer of points averaged

all_plot = 0
aftershock_cutoff_plot = 0
dip_cutoff_plot = 1

aftershock_cutoff= 1200

b_cutoff = 500
t_cutoff = 900

dip_location = 205

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid')

if moveing_avg_toggle == 1:
    data_all = [moving_average(i, pt_avg_num) for i in data_all]

# normalizing
data_all = [[j/np.average(i[0:100]) for j in i] for i in data_all]

# to find offsets, use maximum ranges
y_offset = max([(max(i)-min(i)) for i in data_all])

data_all_stacked = []
for i,j in zip(data_all, range(len(data_all))):
    i = [k+j*y_offset/10 for k in i]
    data_all_stacked.append(i)


if all_plot == 1:
    for i,j in zip(data_all_stacked, label_all):
        plt.plot(i, label=j)
    plt.legend()
    plt.show()

# Use aftershock feature as a starting cutoff point
data_all_aftershock_cutoff = [i[0:aftershock_cutoff] for i in data_all_stacked]

if aftershock_cutoff_plot == 1:
    plt.figure(figsize=(10,4))
    for i,j in zip(data_all_aftershock_cutoff, label_all):
        plt.plot(i, label=j)
    plt.legend()
    plt.show()

# From selected data, now more carefully select around the actual dip
data_all_dip = [i[b_cutoff: t_cutoff] for i in data_all_aftershock_cutoff]
x_list = [i-dip_location for i in range(len(data_all_dip[0]))]

if dip_cutoff_plot == 1:
    plt.figure(figsize=(6,8))
    for i,j in zip(data_all_dip, label_all):
        plt.plot(x_list, i, label=j)
    plt.legend(bbox_to_anchor=(0.8, 0.7))
    ax = plt.gca()
    ax.axes.yaxis.set_visible(False)
    if save_bool == 1:
        plt.savefig(save_path+save_title+".png")
    plt.show()
