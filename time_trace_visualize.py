import matplotlib.pyplot as plt
import numpy as np

file = '20210714_time_trace.txt'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210714\\'+file
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210716\\'
time, amplitude = np.loadtxt(path, unpack=True, skiprows=1)

plot_title = "Resonant g2 Rabi, 0.6uW Red/ 1.6uW Green"
save_title = "20210715_res_g2_rabi_r0p6uW_g1p6uW"
save_bool = 0

plt.figure(figsize=(10,4))
plt.plot(time, amplitude)
plt.show()
