import matplotlib.pyplot as plt
import numpy as np

save_bool = 1
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210714\\'
file = '20210715_res_g2_rabi_to_power'

x = [0.6, 1.3, 1.6, 2.4, 3.1, 4.8, 9.5, 15.9, 31.7, 63.7]
x = [np.sqrt(i) for i in x]
print(x)
y = [0.0001138590298639178,
    8.752210284172329e-05,
    9.030652341115398e-05,
    4.2754061940050424e-05,
    7.886693399562823e-05,
    0.00011828797865766824,
    0.00017551334629778596,
    0.00022919637122726635,
    5.835751945643557e-05,
    5.090024252899064e-05]

plt.plot(x, y, marker="o")
plt.title("Resonance Power to Rabi Frequency")
plt.ylabel("Rabi Frequency (THz)")
plt.xlabel("Sqrt of Resonance Power (Sqrt(uW))")
if save_bool == 1:
    plt.savefig(path+file+".svg")
plt.show()


file = '20210715_res_g2_rabi_to_power_2'
x = [2.4, 3.1, 4.8, 9.5, 15.9]
x = [np.sqrt(i) for i in x]
print(x)
y = [4.2754061940050424e-05,
    7.886693399562823e-05,
    0.00011828797865766824,
    0.00017551334629778596,
    0.00022919637122726635]

plt.plot(x, y, marker="o")
plt.title("Resonance Power to Rabi Frequency")
plt.ylabel("Rabi Frequency (THz)")
plt.xlabel("Sqrt of Resonance Power (Sqrt(uW))")
if save_bool == 1:
    plt.savefig(path+file+".svg")
plt.show()
