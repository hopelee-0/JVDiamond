import matplotlib.pyplot as plt
import numpy as np

offset = 0.1

save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210824\\'
save_bool = 0

file = 'Diamond_EL9_C_HR.csv'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210824\\C HR\\'+file
energy1, counts1 = np.loadtxt(path, unpack=True, skiprows=2, delimiter=",")

file = 'Diamond_ACS_Photonics_C_HR.csv'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210824\\C HR\\'+file
energy2, counts2 = np.loadtxt(path, unpack=True, skiprows=2, delimiter=",")

file = 'Diamond_EL_Blank_C_HR.csv'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210824\\C HR\\'+file
energy3, counts3 = np.loadtxt(path, unpack=True, skiprows=2, delimiter=",")

file = 'Diamond_general_blank_C_HR.csv'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210824\\C HR\\'+file
energy4, counts4 = np.loadtxt(path, unpack=True, skiprows=2, delimiter=",")

counts1 = [i/max(counts1) for i in counts1]
counts2 = [i/max(counts2) for i in counts2]
counts3 = [i/max(counts3) for i in counts3]
counts4 = [i/max(counts4) for i in counts4]

# offset1 = -3.1
# offset3 = -2.1
# offset4 = -3.8
#
# energy1 = [i+offset1 for i in energy1]
# energy3 = [i+offset3 for i in energy3]
# energy4 = [i+offset4 for i in energy4]


ax = plt.gca()
plt.plot(energy1, counts1, label="EL9")
plt.plot(energy2, counts2, label="ACS Photonics 2020 Chip", linestyle="dotted")
plt.plot(energy3, counts3, label="Blank EL Grade", linestyle="dashed")
plt.plot(energy4, counts4, label="Blank General", linestyle="dashdot")
plt.xlim([290, 280])
plt.legend()
plt.ylabel("Arbitrary Normalized Intensity")
plt.xlabel("Energy (eV)")
plt.show()
