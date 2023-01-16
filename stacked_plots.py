import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import scipy.optimize as optimize
import scipy.signal as signal
import os

path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220510_EZ03\\'

file1 = "20220510_EZ03_PLE_200mG_200mR_emitter1.kns"
file2 = "20220510_EZ03_PLE_100mG_50mR_emitter2.kns"
file3 = "20220510_EZ03_PLE_100mG_50mR_emitter3.kns"
file4 = "20220510_EZ03_PLE_100mG_50mR_emitter4.kns"
file5 = "20220510_EZ03_PLE_100mG_50mR_emitter5.kns"

save_name = "20220516_EZ03_PLE_100mG_50mR_PLE"
save_dir = "20220516_EZ03_PLE_100mG_50mR_PLE\\"
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\202205016\\'

save_bool = 1

time1, counts1 = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter="\t")
time2, counts2 = np.loadtxt(path+file2, unpack=True, skiprows=0, delimiter="\t")
time3, counts3 = np.loadtxt(path+file3, unpack=True, skiprows=0, delimiter="\t")
time4, counts4 = np.loadtxt(path+file4, unpack=True, skiprows=0, delimiter="\t")
time5, counts5 = np.loadtxt(path+file5, unpack=True, skiprows=0, delimiter="\t")

# try to calibrate scan frequency
peaks1, __ = signal.find_peaks(counts1, height=max(counts1)/4)
peaks2, __ = signal.find_peaks(counts2, height=max(counts2)/4)
peaks3, __ = signal.find_peaks(counts3, height=max(counts3)/4)
peaks4, __ = signal.find_peaks(counts4, height=max(counts4)/4)
peaks5, __ = signal.find_peaks(counts5, height=max(counts5)/4)

plt.scatter(time1[peaks1], counts1[peaks1])
plt.plot(time1, counts1)
plt.show()
