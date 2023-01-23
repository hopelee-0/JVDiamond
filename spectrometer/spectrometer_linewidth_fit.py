import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

# load data
file = 'PL_monochromator.kns'
path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220919_SiV_LND03\\20220919_LND03\\'+file

save_path = 'G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20220919_SiV_LND03\\20220919_LND03\\'

plot_title = "Monochromator Bandwidth"
save_title = "monochromator_pl"
save_bool = 1

# choosing sections of data for fitting
a = 700
b = 950

# display regions
a_display = 650
b_display = 1000

# parameter guesses
amp = 500
x0 = 673.5
w = 0.01
back_2 = 2000

show_data = 0
fit_region = 0
guess_plot = 1
show_fit = 1

wave, counts = np.loadtxt(path, unpack=True, skiprows=0, delimiter="\t")

if show_data == 1:
    plt.plot(wave, counts)
    plt.show()

data_x = wave[a:b]
data_y = counts[a:b]

display_x = wave[a_display:b_display]
display_y = counts[a_display:b_display]

if fit_region == 1:
    plt.plot(wave, counts)
    plt.plot(display_x, display_y)
    plt.plot(data_x, data_y)
    plt.show()

def Lorentzian(x, amp, x0, w, back, back_2):
    alpha = (x-x0)/(w/2)
    return  (amp/(1+alpha**2)+back*x+back_2)

def Lorentzian(x, amp, x0, w, back_2):
    alpha = (x-x0)/(w/2)
    return  (amp/(1+alpha**2)+back_2)

if guess_plot == 1:
    y_guess = [Lorentzian(i, amp, x0, w, back_2) for i in data_x]
    plt.plot(display_x, display_y)
    plt.plot(data_x, y_guess)
    plt.show()

params, params_covariance = optimize.curve_fit(Lorentzian, data_x, data_y,
                                                    p0=[amp, x0, w, back_2])

# create denser x values list to feed into fit function
function_x = np.linspace(display_x[0], display_x[-1], 3000)
y_fit = [Lorentzian(i, params[0], params[1], params[2], params[3]) for i in function_x]

# generate final figure plot
plt.scatter(display_x, display_y, c="k", marker=".", alpha=0.7)
plt.plot(function_x, y_fit, c="b", label="FWHM={:.4f} nm".format(params[2]))
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
    f.write("Amplitude: {}\n".format(params[0]))
    f.write("x0: {}\n".format(params[1]))
    f.write("FWHM: {}\n".format(params[2]))
    f.write("Background term, linear: {}\n".format(params[3]))
    # f.write("Background term, constant: {}\n".format(params[4]))
    f.write("\n")
