#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 21:49:30 2022

@author: ericrosenthal
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.fft import fft, ifft, fftshift, ifftshift
from scipy import signal

#%%import data
df = np.loadtxt('20221104_8p35mW_2000sint_couplers_PL00.sint.dat')
data = df[4:]

ns_per_pixel = 0.064

#%% process data and fit

# g2
def g2(t,tau_a,tau_b,amp_a,amp_b,scale,t0):
    y_a = (1 - amp_a*np.exp(-abs(t/tau_a))) * np.heaviside(t, t0)
    y_b = (1 - amp_b*np.exp(-abs(t/tau_b))) * (1-np.heaviside(t, t0))
    y = scale * (y_a + y_b)
    return y

# gaussian
def gaussian(t,t0,sigma):
    y = 1/(sigma*np.sqrt(np.pi)) * np.exp(-0.5*((t-t0)/sigma)**2)
    return y

# exponential + gaussian
def g2_real(t,tau,amp,scale_g2,t0,sigma,scale_gaussian):
    
    # exponential
    y_g2_a = (1 - amp*np.exp(-abs(t/tau))) * np.heaviside(t, t0)
    y_g2_b = (1 - amp*np.exp(-abs(t/tau))) * (1-np.heaviside(t, t0))
    y_g2 = abs(scale_g2*(y_g2_a + y_g2_b))
        
    # gaussian on top of g2
    y_gaussian = abs(scale_gaussian*np.exp(-0.5*abs((t-t0)/abs(sigma))**2))
    y = y_g2 + y_gaussian
            
    return y

# exponential + gaussian, convolved with gaussian filter
def g2_real_conv(t,tau,amp,scale_g2,t0,sigma,scale_gaussian,sigma_timeres):
    
    # exponential
    y_g2_a = (1 - amp*np.exp(-abs(t/tau))) * np.heaviside(t, t0)
    y_g2_b = (1 - amp*np.exp(-abs(t/tau))) * (1-np.heaviside(t, t0))
    y_g2 = abs(scale_g2*(y_g2_a + y_g2_b))
        
    # gaussian on top of g2
    y_gaussian = abs(scale_gaussian*np.exp(-0.5*abs((t-t0)/abs(sigma))**2))
    y = y_g2 + y_gaussian
    
    # sigma_timeres = 6
    y_gaussian_timeres = 1/(sigma_timeres*np.sqrt(np.pi)) * np.exp(-0.5*abs((t-t0)/sigma_timeres)**2)  

    y_conv = signal.convolve(y, y_gaussian_timeres, 'same')

    ####### this should work too #######
    # y_conv = abs(ifft(fft(y_g2) * fft(y_gaussian)))

    return y_conv

def g2_real_conv_known_timeres(t,tau,amp,scale_g2,t0,sigma,scale_gaussian):
    
    # exponential
    y_g2_a = (1 - amp*np.exp(-abs(t/tau))) * np.heaviside(t, t0)
    y_g2_b = (1 - amp*np.exp(-abs(t/tau))) * (1-np.heaviside(t, t0))
    y_g2 = abs(scale_g2*(y_g2_a + y_g2_b))
        
    # gaussian on top of g2
    y_gaussian = abs(scale_gaussian*np.exp(-0.5*abs((t-t0)/abs(sigma))**2))
    y = y_g2 + y_gaussian
    
    sigma_timeres = 6 # corresponds to 6 * ns_per_pixel = 400 ps timing resolution 
    y_gaussian_timeres = 1/(sigma_timeres*np.sqrt(np.pi)) * np.exp(-0.5*abs((t-t0)/sigma_timeres)**2)  

    y_conv = signal.convolve(y, y_gaussian_timeres, 'same')

    ####### this should work too #######
    # y_conv = abs(ifft(fft(y_g2) * fft(y_gaussian)))

    return y_conv

min_idx = 2124
max_idx = 2900
mid_idx = (max_idx - min_idx)/2
num_t = max_idx - min_idx

t = np.linspace(0,num_t-1,num_t) - mid_idx
y = data[min_idx:max_idx]

# input guesses for fit
tau_guess = 10
min_guess = 400
background_guess = 700
t0_guess = 0
sigma_guess = 100
gaussian_background_guess = 150
sigma_timeres_guess = 6

# fit g2, "ideal" exponential only
popt, pcov = curve_fit(g2, t, y, p0=[tau_guess,tau_guess,min_guess,min_guess,background_guess,t0_guess])
y_fit = g2(t,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])

# convolution theorem: 
# F[f*g] = F[f]F[g]
# therefore f*g = Finverse[F[f]F[g]], i.e. what we're trying to find
# see https://mathworld.wolfram.com/ConvolutionTheorem.html for more details

# fit exponential + Gaussian background
popt, pcov = curve_fit(g2_real, t, y, p0=[tau_guess,min_guess,background_guess,t0_guess,sigma_guess,gaussian_background_guess])
y_fit_real = g2_real(t,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])

# fit exponential + Gaussian background, convolved with another gaussian to account for timing resolution
popt, pcov = curve_fit(g2_real_conv, t, y, p0=[tau_guess,min_guess,background_guess,t0_guess,sigma_guess,gaussian_background_guess,sigma_timeres_guess])
y_fit_real_conv = g2_real_conv(t,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6])

# fit exponential + Gaussian background, convolved with another gaussian to account for timing resolution (known timing resolution)
popt, pcov = curve_fit(g2_real_conv_known_timeres, t, y, p0=[tau_guess,min_guess,background_guess,t0_guess,sigma_guess,gaussian_background_guess])
y_fit_real_conv_known_timeres = g2_real_conv_known_timeres(t,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])

#%% plot data

plt.plot(t*ns_per_pixel, y, 'o', label='data')
# plt.plot(t*ns_per_pixel, y_fit, label='fit, exp only')
# plt.plot(t*ns_per_pixel, y_fit_real, label='fit, exp + gaussian')
plt.plot(t*ns_per_pixel, y_fit_real_conv, label='fit, (fitting sigma_timeres)')
plt.plot(t*ns_per_pixel, y_fit_real_conv_known_timeres, label='fit, (fixed sigma_timeres)')
plt.grid()
plt.legend()
plt.xlabel('time (ns)')
plt.ylabel('counts (units?)')
plt.title('zoomed out')
plt.xlim([-22,22])
plt.show()

plt.plot(t*ns_per_pixel, y, 'o', label='data')
# plt.plot(t*ns_per_pixel, y_fit, label='fit, exp only')
# plt.plot(t*ns_per_pixel, y_fit_real, label='fit, exp + gaussian')
plt.plot(t*ns_per_pixel, y_fit_real_conv, label='fit, (fitting sigma_timeres)')
plt.plot(t*ns_per_pixel, y_fit_real_conv_known_timeres, label='fit, (fixed sigma_timeres)')
plt.grid()
plt.legend()
plt.xlabel('time (ns)')
plt.ylabel('counts (units?)')
plt.title('zoomed in on dip')
plt.xlim([-3,3])
plt.show()



