import matplotlib.pyplot as plt
import numpy as np

file = '20221102_coupler_collect_confocal_excite_0p0mW.kns'
path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20221102_LND03\\saturation_001\\coupler_collect_confocal_excite\\'+file

time, counts = np.loadtxt(path, unpack=True, skiprows=1)

avg = np.mean(counts)
print(avg)
