import numpy as np
import matplotlib.pyplot as plt

file = '20220822_terascan_1.kns'
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\other - equipment characterization\\Monochromator\\"

save_title = '20220822_terascan_1.png'
save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\Color Center Characterization\\20220724_EZ01\\'

plot_title = "E4 Inhomogeneous Broadening, 60s Integration"

time, counts = np.loadtxt(path+file, unpack=True, skiprows=0, delimiter="\t")

# quick check of Data

plt.plot(time, counts)
plt.show()
