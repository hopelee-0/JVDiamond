import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print('test')

name = '20221129_Integrated_737nm'

file_excite = f'{name}_exc.csv'
file_MM = f'{name}_MM.csv'
file_SM = f'{name}_SM.csv'
# path = 'G:/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20221212/Connected 1/'
path = '/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20221128_LND03/Integrated/'

save_title = f"{name}"
save_path = path+"processed/" 

shift_1 = 2200
shift_2 = 1100

background_threshold = 1

trim_min = 100
trim_max = -2200

scale0 = 1000
scale1 = 5
scale2 = 5
poly_order = 60

threshold = 1000
view_all_bool = 1
view_slices_bool = 1
view_interpolate_bool = 1
background_bool = 1
view_background_bool = 1
trim_data_bool = 1
view_trim_bool = 1
save_bool = 1

# time0, power0 = np.loadtxt(path+file_excite, unpack=True, skiprows=23, delimiter=';')
# time1, power1 = np.loadtxt(path+file_SM, unpack=True, skiprows=23, delimiter=';')
# time2, power2 = np.loadtxt(path+file_MM, unpack=True, skiprows=23, delimiter=';')

data0 = pd.read_csv(path+file_excite, skiprows=22, delimiter=';', decimal=',').astype(float)
data1 = pd.read_csv(path+file_MM, skiprows=22, delimiter=';', decimal=',').astype(float)
data2 = pd.read_csv(path+file_SM, skiprows=22, delimiter=';', decimal=',').astype(float)

time0 = np.asarray(data0['Time (ms)']) 
power0 = np.asarray(data0['Power (W)'])
time1 = np.asarray(data1['Time (ms)'])
power1 = np.asarray(data1['Power (W)'])
time2 = np.asarray(data2['Time (ms)'])
power2 = np.asarray(data2['Power (W)'])

time1 = [i+shift_1 for i in time1]
time2 = [i+shift_2 for i in time2]

if view_all_bool == 1:
    plt.figure(figsize=(10,4))
    plt.title("view all")
    plt.plot(time0, power0/scale0, label="Excitation/{}".format(scale0))
    plt.plot(time1, power1/scale1, label="MM/{}".format(scale1))
    plt.plot(time2, power2/scale2, label="SM/{}".format(scale2))
    plt.legend()
    plt.show()

if background_bool == 1:
    power0_back = np.mean([i for i in power0 if i<=background_threshold*np.mean(power0)])
    power1_back = np.mean([i for i in power1 if i<=background_threshold*np.mean(power1)])
    power2_back = np.mean([i for i in power2 if i<=background_threshold*np.mean(power2)])

    print(sum(power1))
    print(power0_back, power1_back, power2_back)

    power0 -= power0_back
    power1 -= power1_back
    power2 -= power2_back

    if view_background_bool:
        plt.figure(figsize=(10,4))
        plt.title("background subtraction")
        plt.plot(time0, power0/scale0, label="Excitation/{}".format(scale0))
        plt.plot(time1, power1/scale1, label="MM/{}".format(scale1))
        plt.plot(time2, power2/scale2, label="SM/{}".format(scale2))
        plt.legend()
        plt.show()

if trim_data_bool == 1:

    if view_trim_bool == 1:
        plt.figure(figsize=(10,4))
        plt.title("data trimming")
        plt.plot(time0, power0/scale0, label="Excitation/{}".format(scale0))
        plt.plot(time1, power1/scale1, label="MM/{}".format(scale1))
        plt.plot(time2, power2/scale2, label="SM/{}".format(scale2))
        plt.axvspan(time0[trim_min] ,time0[trim_max], alpha=0.2, color='gray')
        plt.legend()
        plt.show()

    time0 = np.asarray(time0[trim_min:trim_max])
    time1 = np.asarray(time1[trim_min:trim_max])
    time2 = np.asarray(time2[trim_min:trim_max])

    power0 = np.asarray(power0[trim_min:trim_max])
    power1 = np.asarray(power1[trim_min:trim_max])
    power2 = np.asarray(power2[trim_min:trim_max])

# find steps to slice data for polynomial fits
excite_grad = np.gradient(power0)
MM_grad = np.gradient(power1)
SM_grad = np.gradient(power2)

def steps(array, threshold):
    edge_list_idx = []
    for i in range(len(array)):
        if np.abs(array[i])<=threshold:
            edge_list_idx.append(i)
    return (edge_list_idx)

excite_steps = steps(excite_grad, np.max(excite_grad)/threshold)
MM_steps = steps(MM_grad, np.max(MM_grad)/threshold)
SM_steps = steps(SM_grad, np.max(SM_grad)/threshold)

excite_sliced = [i for i in excite_steps if power0[i]>= np.mean(power0)]
MM_sliced = [i for i in MM_steps if power1[i]>= np.mean(power1)]
SM_sliced = [i for i in SM_steps if power2[i]>= np.mean(power2)]

time0_s = time0[excite_sliced]
time1_s = time1[MM_sliced]
time2_s = time2[SM_sliced]

power0_s = power0[excite_sliced]
power1_s = power1[MM_sliced]
power2_s = power2[SM_sliced]

if view_slices_bool == 1:
    plt.figure(figsize=(10,4))
    plt.plot(time0, power0/scale0, label="Excitation/{}".format(scale0))
    plt.plot(time1, power1/scale1, label="MM/{}".format(scale1))
    plt.plot(time2, power2/scale2, label="SM/{}".format(scale2))
    plt.scatter(time0_s, power0_s/scale0)
    plt.scatter(time1_s, power1_s/scale1)
    plt.scatter(time2_s, power2_s/scale2)
    plt.legend()
    plt.show()

# interpolate for excitation using a 24th order poly
excite_interpolate = np.polyfit([time0[i] for i in excite_sliced], [power0[i] for i in excite_sliced], poly_order)
excite_f = np.poly1d(excite_interpolate)

if view_interpolate_bool == 1:
    plt.figure(figsize=(10,4))
    plt.scatter([time0[i] for i in excite_sliced], [power0[i]/scale0 for i in excite_sliced])
    plt.plot(time0, excite_f(time0)/scale0)
    plt.scatter(time1_s, [i/scale1 for i in power1_s])
    plt.scatter(time2_s, [i/scale2 for i in power2_s])
    plt.show()

# finding transmissions
MM_transmission = [i/excite_f(j) for i,j in zip(power1_s, time1_s)]

SM_transmission = [i/excite_f(j) for i,j in zip(power2_s, time2_s)]

MM_transmission_avg = np.mean(MM_transmission)*100
SM_transmission_avg = np.mean(SM_transmission)*100

print("MM, SM: {:.2f},{:.2f}".format(MM_transmission_avg, SM_transmission_avg))

# Write results to text file to save
if save_bool == 1:
    f = open(save_path+save_title+".txt", "w")
    f.write("MM, SM: {:.2f},{:.2f}\n".format(MM_transmission_avg, SM_transmission_avg))
    f.write("\n")
    f.write("Parameters:")
    f.write("\n")
    f.write("shift_1: {:}\n".format(shift_1))
    f.write("shift_2: {:}\n".format(shift_2))
    f.write("threshold: {:}\n".format(threshold))
    f.write("background threshold: {:}\n".format(background_threshold))
    if trim_data_bool == 1:
        f.write("trimming range: {:}, {:}\n".format(trim_min, trim_max))
    f.write("polynomial order: {:}\n".format(poly_order))
    f.close()
