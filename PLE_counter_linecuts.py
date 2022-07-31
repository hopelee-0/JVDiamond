import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import scipy.optimize as optimize
import scipy.signal as signal
import os

path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Attodry\\2022-05-27_EL15\\EL15_R1D4_r3c3\\'
file1 = "PLE_30ms_15GHz_scantime10s_619p29498nm_14uWred_100uWgreen_0.kns"

save_name = "PLE_30ms_15GHz_scantime10s_619p29498nm_14uWred_100uWgreen_0"
# save_dir = "EL15_R1D4_r3c3\PLE_30ms_15GHz_scantime10s_619p29498nm_14uWred_100uWgreen_0_cuts_estimate\\"
save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Attodry\\2022-05-27_EL15\\EL15_R1D4_r3c3\\linecut_folder\\'

##############################################################################################

def pick_scan(peaks, interval_pick):
    scan_start = (peaks[0+interval_pick]+peaks[1+interval_pick])//2
    scan_end = (peaks[1+interval_pick]+peaks[2+interval_pick])//2
    return(scan_start, scan_end)

time1, counts1 = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter="\t")

# try to calibrate scan frequency
peaks1, __ = signal.find_peaks(counts1, height=max(counts1)/1.5, distance=90)

interval_pick1 = 5

start1, stop1 = pick_scan(peaks1, interval_pick1)

plt.plot(time1, counts1)
plt.scatter(time1[peaks1], counts1[peaks1])
plt.savefig(save_path+save_name+"_full.png")
plt.show()

for i in range(len(peaks1)-1):
    print(i)
    start1, stop1 = pick_scan(peaks1, i)
    plt.plot(time1[start1:stop1]-time1[start1], counts1[start1:stop1]/max(counts1[start1:stop1]), label="Emitter 1")
    plt.legend()
    plt.ylabel("Intensity (normalized)")
    plt.xlabel("28GHz Scan Range")
    plt.xticks([])
    plt.savefig(save_path+save_name+"_line_fit"+"_{}".format(i)+".png", bbox_inches='tight')
    plt.clf()
    # plt.show()
