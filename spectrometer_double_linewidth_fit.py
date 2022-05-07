import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

# load data
file = '20220321_siv_transfer_717nm_740BP_BS_210uW_1714_1s_sat_curve.knspl'
path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220322_SiV_WG_on_LN\\'+file

save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220323\\'

plot_title = "SiV Line Widths, 210uW"
save_title = "20220323_SiV_linewidth_210uW"
save_bool = 1

# choosing sections of data for fitting
a = 1350
b = 1470

# display regions
a_display = 1220
b_display = 1500

# parameter guesses: amp, x0, w; background is separate
params_1 = [500, 737.05, 0.01]
params_2 = [500, 737.17, 0.01]
back = 3900

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

def Lorentzian_double(x, amp_1, x0_1, w_1, amp_2, x0_2, w_2, back):
    alpha1 = (x-x0_1)/(w_1/2)
    alpha2 = (x-x0_2)/(w_2/2)
    peak_1 = amp_1/(1+alpha1**2)
    peak_2 = amp_2/(1+alpha2**2)
    return(peak_1 + peak_2+ back)

# unpack parameter lists from above
amp_1 = params_1[0]
x0_1 = params_1[1]
w_1 = params_1[2]
amp_2 = params_2[0]
x0_2 = params_2[1]
w_2 = params_2[2]

if guess_plot == 1:
    y_guess = [Lorentzian_double(i, amp_1, x0_1, w_1, amp_2, x0_2, w_2, back) for i in data_x]
    plt.plot(display_x, display_y)
    plt.plot(data_x, y_guess)
    plt.show()

params, params_covariance = optimize.curve_fit(Lorentzian_double, data_x, data_y,
                                                    p0=[amp_1, x0_1, w_1, amp_2, x0_2, w_2, back])

# create denser x values list to feed into fit function
function_x = np.linspace(display_x[0], display_x[-1], 3000)
y_fit = [Lorentzian_double(i, params[0], params[1], params[2], params[3], params[4], params[5], params[6]) for i in function_x]

# generate final figure plot
plt.scatter(display_x, display_y, c="k", marker=".", alpha=0.7)
plt.plot(function_x, y_fit, c="b", label="FWHM1={:.4f},{:.4f}".format(params[2], params[5]))
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
    f.write("Amplitude:{}, {}\n".format(params[0], params[3]))
    f.write("x0:{}, {}\n".format(params[1], params[4]))
    f.write("FWHM:{}, {}\n".format(params[2], params[5]))
    f.write("Background term, constant:{}\n".format(params[6]))
    f.write("\n")
