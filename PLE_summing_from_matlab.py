import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

file1 = '(0_21)_(0_77)_g0uW_r0_001uW_002_p5GHz_5s_5min_integration.kns'
path = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20210712_El15_R7_D7\\"

save_title = '(0_21)_(0_77)_g0uW_r0_001uW_002_p5GHz_5s_5min_integration'
save_path = 'C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220516\\'+save_title

plot_title = "PLE Time Averaged"

plot_normalize_bool = 1
x_limits_bool = 0
andor_calibrate = 0
save_bool = 0

wave, counts = np.loadtxt(path+file1, unpack=True, skiprows=0, delimiter="\t")

amp0 = 0.9
w0 = 20
g_back0 = 0.1
line_back0 = 0

x0_2 = -125
amp1 = 0.1
w1 = 25

# cutoffs in terms of indices
x_fit_min = 5
x_fit_max = 5

def gaussian(t, t0, amp, w, g_back, line_back):
    return(amp*np.exp(-(t-t0)**2/2/w**2)+line_back*t+g_back)

def Lorentzian(x, x0, amp, w, back_2, back):
    alpha = (x-x0)/(w/2)
    return  (amp/(1+alpha**2)+back*x+back_2)

def Lorentzian_double(x, amp_1, x0_1, w_1, amp_2, x0_2, w_2, back):
    alpha1 = (x-x0_1)/(w_1/2)
    alpha2 = (x-x0_2)/(w_2/2)
    peak_1 = amp_1/(1+alpha1**2)
    peak_2 = amp_2/(1+alpha2**2)
    return(peak_1 + peak_2+ back)

def Gaussian_double(x, amp_1, x0_1, w_1, amp_2, x0_2, w_2, back):
    alpha1 = (x-x0_1)/(w_1/2)
    alpha2 = (x-x0_2)/(w_2/2)
    peak_1 = amp_1*np.exp(-(x-x0_1)**2/2/w_1**2)
    peak_2 = amp_2*np.exp(-(x-x0_2)**2/2/w_2**2)
    return(peak_1+peak_2+back)

sums, edges = np.histogram(wave, bins=130, weights=counts)
counts_1, _ = np.histogram(wave, bins=130)
revbinned = sums / counts_1

revbinned = revbinned/max(revbinned)
result = np.where(revbinned == np.amax(revbinned))
center_wave = edges[result[0][0]]
center_freq = 3e8/center_wave*1e-9
freq = 3e8/edges[1::]*1e-9
freq_offset = (freq-center_freq)/1e-9*1e3

# y_guess = [Lorentzian(i, center_freq, amp0, w0, g_back0, line_back0) for i in freq_offset]
y_guess = [Lorentzian_double(i, amp0, center_freq, w0, amp1, x0_2, w1, g_back0) for i in freq_offset]

plt.plot(freq_offset, revbinned, '.')
plt.axvline(x=freq_offset[x_fit_min], color='b')
plt.axvline(x=freq_offset[-x_fit_max], color='b')
plt.plot(freq_offset, y_guess)
plt.title("PLE Time Averaged")
plt.ylabel("Counts, normalized")
plt.xlabel("Frequency Offset (MHz)")
plt.show()

# params, params_covariance = optimize.curve_fit(Lorentzian, freq_offset[x_fit_min:-x_fit_max],
#                                                 revbinned[x_fit_min:-x_fit_max],
#                                                 p0=[center_freq, amp0, w0, g_back0, line_back0],
#                                                 bounds=(0.0, np.inf))

params, params_covariance = optimize.curve_fit(Lorentzian_double, freq_offset[x_fit_min:-x_fit_max],
                                                revbinned[x_fit_min:-x_fit_max],
                                                p0=[amp0, center_freq, w0, amp1, x0_2, w1, g_back0])

# y_fit = [Lorentzian(i, params[0], params[1], params[2], params[3], params[4]) for i in freq_offset]
y_fit = [Lorentzian_double(i, params[0], params[1], params[2], params[3], params[4], params[5], params[6]) for i in freq_offset]

plt.plot(freq_offset, revbinned, '.', color='k')
plt.plot(freq_offset, y_fit, color='r', label="Lorentzian Fit")
plt.title(plot_title)
plt.ylabel("Counts, normalized")
plt.xlabel("Frequency Offset (MHz)")
plt.savefig(save_path+save_title+'.png')
plt.show()

f = open(save_path+save_title+".txt", "w")
f.write(plot_title+"\n")
f.write("\n")
f.write("Raw Parameters:{}\n".format(params))
f.write("\n")
f.write("Amplitude 1 (MHz): {:}\n".format(params[0]))
f.write("Center Freq 1: {:}\n".format(params[1]))
f.write("FWHM 1: {:}\n".format(params[2]))
f.write("Amplitude 2 (MHz): {:}\n".format(params[3]))
f.write("Center Freq 2: {:}\n".format(params[4]))
f.write("FWHM 2: {:}\n".format(params[5]))
f.write("Constant Background: {:}".format(params[6]))
f.close()
