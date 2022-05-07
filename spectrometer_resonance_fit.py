import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

# load data
file = '20210813_g58_d4_bck12_b6_fine_2.kns'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210813_SnV_Cavities\\'+file
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210816\\'

plot_title = "g58, Dose 4, Block 12, Beam 6 Resonance Fit"
save_title = "20210816_g58_d4_bck12_b6_res_fit_1"
save_bool = 1

# choosing sections of data for fitting
a = 700
b = 775

# display regions
a_display = 600
b_display = 600

# parameter guesses
amp = 500
x0 = 701
w = 0.5
back = 0.5
back_2 = 3500

show_data = 0
fit_region = 0
guess_plot = 1
show_fit = 1

wave, counts = np.loadtxt(path, unpack=True, skiprows=0)

if show_data == 1:
    plt.plot(wave, counts)
    plt.show()

data_x = wave[a:-b]
data_y = counts[a:-b]

display_x = wave[a_display:-b_display]
display_y = counts[a_display:-b_display]

if fit_region == 1:
    plt.plot(wave, counts)
    plt.plot(display_x, display_y)
    plt.plot(data_x, data_y)
    plt.show()

def Lorentzian(x, amp, x0, w, back, back_2):
    alpha = (x-x0)/(w/2)
    return  (amp/(1+alpha**2)+back*x+back_2)

if guess_plot == 1:
    y_guess = [Lorentzian(i, amp, x0, w, back, back_2) for i in data_x]
    plt.plot(display_x, display_y)
    plt.plot(data_x, y_guess)
    plt.show()

params, params_covariance = optimize.curve_fit(Lorentzian, data_x, data_y,
                                                    p0=[amp, x0, w, back, back_2])

# calculate quality factor
Q = abs(params[1]/params[2])

y_fit = [Lorentzian(i, params[0], params[1], params[2], params[3], params[4]) for i in display_x]
plt.scatter(display_x, display_y, c="k", marker=".", alpha=0.7)
plt.plot(display_x, y_fit, c="b", label="Q={:.0f}".format(Q))
plt.title(plot_title)
plt.legend()
if save_bool == 1:
    plt.savefig(save_path+save_title+'.png')
if show_fit == 1:
    plt.show()

# Write results to text file to save
if save_bool == 1:
    f = open(save_path+save_title+".txt", "w")
    f.write(plot_title+"\n")
    f.write("\n")
    f.write("Amplitude:{}\n".format(params[0]))
    f.write("x0:{}\n".format(params[1]))
    f.write("FWHM:{}\n".format(params[2]))
    f.write("Background term, linear:{}\n".format(params[3]))
    f.write("Background term, constant:{}\n".format(params[4]))
    f.write("\n")
