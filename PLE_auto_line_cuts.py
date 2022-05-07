import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import scipy.optimize as optimize
import os

# Import PL confocal data
file = '20220505_PLE_high_power_4.kns'
path = 'C:\\Users\\hopel\\Documents\\Data\\20220505_EZ03\\'+file

save_name = "20220505_EZ03_PLE_high_power_4"
save_dir = "20220505_EZ03_PLE_high_power_4_linecuts\\"
save_path = 'C:\\Users\\hopel\\Documents\\Data\\20220505_EZ03\\'

cuts_show = 0
confocal_check = 1
save_bool = 1
rotate = 0
delete_bool = 1 # removes every other scan due to hysteresis

# parameters for fitting
line_fit = 1
guess_plot = 1 # shows fit starting parameters
linecut_sample = 1 # linecut being used to determine starting params
fit_show = 0
type = 'gauss' # options of 'gauss' or 'lorentz'
amp = 30000
x0 = 750 # all x units uncalibrated until the end
w = 20
back = 0 #linear background term
back_2 = 30000 #constant background term


confocal = np.loadtxt(path)
x_list = range(len(confocal.T[0]))

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

count = 0
for i in confocal.T:
    plt.plot(i)
    if save_bool == 1:
        plt.savefig(save_path+save_dir+save_name+"_{}".format(count)+".png", bbox_inches='tight')
    if cuts_show == 1:
        plt.show()
    plt.clf()
    count += 1

# does its best to fit all line cuts seperately
def Lorentzian(x, amp, x0, w, back, back_2):
    alpha = (x-x0)/(w/2)
    return  (amp/(1+alpha**2)+back*x+back_2)

def Gaussian(x, amp, x0, w, back, back_2):
    alpha = (x-x0)**2/2/w**2
    return(amp*np.exp(-alpha)+back*x+back_2)

if line_fit == 1:
    if guess_plot == 1: # guess plot now only shows the first linecut
        if type == 'gauss':
            y_guess = [Gaussian(i, amp, x0, w, back, back_2) for i in x_list]
        elif type == 'lorentz':
            y_guess = [Lorentzian(i, amp, x0, w, back, back_2) for i in x_list]
        plt.plot(confocal.T[linecut_sample])
        plt.plot(y_guess)
        plt.show()
        plt.clf()

    count = 0
    for i in confocal.T:
        if type == 'gauss':
            params, params_covariance = optimize.curve_fit(Gaussian, x_list, i,
                                                                p0=[amp, x0, w, back, back_2])
            y_fit = [Gaussian(i, params[0], params[1], params[2], params[3], params[4]) for i in x_list]
        elif type == 'lorentz':
            params, params_covariance = optimize.curve_fit(Lorentzian, x_list, i,
                                                                p0=[amp, x0, w, back, back_2])
            y_fit = [Lorentzian(i, params[0], params[1], params[2], params[3], params[4]) for i in x_list]

        plt.plot(y_fit, color='r', label="Fit")
        plt.scatter(x_list, i, color='k', marker=".", label="Data")
        plt.title("PLE Linecut, Fit")
        plt.legend()
        if save_bool == 1:
            plt.savefig(save_path+save_dir+save_name+"_line_fit"+"_{}".format(count)+".png", bbox_inches='tight')
        if fit_show == 1:
            plt.show()
        plt.clf()

        f = open(save_path+save_dir+save_name+"fit_params".format(count)+".txt", "w")
        f.write("{}\n".format(save_name))
        f.write("\n")
        f.write("Function Type:{}\n".format(type))
        f.write("Amplitude:{}\n".format(params[0]))
        f.write("x0:{}\n".format(params[1]))
        f.write("FWHM:{}\n".format(params[2]))
        f.write("Background term, linear:{}\n".format(params[3]))
        f.write("Background term, constant:{}\n".format(params[4]))
        f.write("\n")

        count += 1
