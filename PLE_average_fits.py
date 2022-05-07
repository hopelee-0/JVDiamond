import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import scipy.optimize as optimize
import os

# Import PL confocal data
file = '20220505_PLE_high_power_3.kns'
path = 'C:\\Users\\hopel\\Documents\\Data\\20220505_EZ03\\'+file

save_name = "20220505_EZ03_PLE_high_power_3"
save_dir = "20220505_EZ03_PLE_high_power_3_linecuts\\"
save_path = 'C:\\Users\\hopel\\Documents\\Data\\20220505_EZ03\\'

confocal_check = 0
sum_show = 1
rotate = 0
delete_bool = 1 # removes every other scan due to hysteresis
save_bool = 1

# parameters for fitting
sum_fit = 1
guess_plot = 1 # shows fit starting parameters
type = 'gauss' # options of 'gauss' or 'lorentz'
amp = 30000
x0 = 380 # all x units uncalibrated until the end
w = 20
back = 0 #linear background term
back_2 = 30000 #constant background term

confocal = np.loadtxt(path)

if delete_bool == 1:
    confocal = np.delete(confocal, list(range(0, confocal.shape[1], 2)), axis=1) #removes every other column in order to deal with hysteresis

if rotate == 1:
    confocal = np.rot90(confocal)

if confocal_check == 1:
    plt.imshow(confocal, aspect='auto', origin='lower')
    if rotate == 1:
        plt.colorbar(orientation='horizontal')
    else:
        plt.colorbar()
    plt.show()

if os.path.exists(save_path+save_dir) == False: # create a folder to hold all the linecuts for a PLE scan
    os.makedirs(save_path+save_dir)

sum_PLE = np.sum(confocal, axis=1)
x_list = range(len(sum_PLE))

plt.plot(sum_PLE, label="Delete:{}".format(delete_bool))
plt.legend()
plt.title("PLE Sum")
if save_bool == 1:
    plt.savefig(save_path+save_dir+save_name+"_sum.png", bbox_inches='tight')
if sum_show == 1:
    plt.show()

# summed PLE fitting
def Lorentzian(x, amp, x0, w, back, back_2):
    alpha = (x-x0)/(w/2)
    return  (amp/(1+alpha**2)+back*x+back_2)

def Gaussian(x, amp, x0, w, back, back_2):
    alpha = (x-x0)**2/2/w**2
    return(amp*np.exp(-alpha)+back*x+back_2)

if sum_fit == 1:
    if guess_plot == 1:
        if type == 'gauss':
            y_guess = [Gaussian(i, amp, x0, w, back, back_2) for i in x_list]
        elif type == 'lorentz':
            y_guess = [Lorentzian(i, amp, x0, w, back, back_2) for i in x_list]
        plt.plot(sum_PLE)
        plt.plot(y_guess)
        plt.show()

    if type == 'gauss':
        params, params_covariance = optimize.curve_fit(Gaussian, x_list, sum_PLE,
                                                            p0=[amp, x0, w, back, back_2])
        y_fit = [Gaussian(i, params[0], params[1], params[2], params[3], params[4]) for i in x_list]
    elif type == 'lorentz':
        params, params_covariance = optimize.curve_fit(Lorentzian, x_list, sum_PLE,
                                                            p0=[amp, x0, w, back, back_2])
        y_fit = [Lorentzian(i, params[0], params[1], params[2], params[3], params[4]) for i in x_list]

    plt.plot(y_fit, color='r', label="Fit")
    plt.scatter(x_list, sum_PLE, color='k', marker=".", label="Data")
    plt.title("PLE Sum, Fit")
    plt.legend()
    if save_bool == 1:
        plt.savefig(save_path+save_dir+save_name+"_sum_fit.png", bbox_inches='tight')
    if sum_show == 1:
        plt.show()

    f = open(save_path+save_dir+save_name+"fit_params.txt", "w")
    f.write("{}\n".format(save_name))
    f.write("\n")
    f.write("Function Type:{}\n".format(type))
    f.write("Amplitude:{}\n".format(params[0]))
    f.write("x0:{}\n".format(params[1]))
    f.write("FWHM:{}\n".format(params[2]))
    f.write("Background term, linear:{}\n".format(params[3]))
    f.write("Background term, constant:{}\n".format(params[4]))
    f.write("\n")
