import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import scipy.fftpack as fftpack

file_name = "EZ_02_1.png"
save_name = "EZ02_postetch_process_1.png"
title = "EZ02, Post Etch"
threshold = 0.74 # set identification threshold
n = 0 # defines filtered frequencies
save_bool = 0

img=mpimg.imread('C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220224\\'+file_name)
title = "EZ03, Post Etch"

img_R = img[:,:,0]
img_G = img[:,:,1]
img_B = img[:,:,2]

img_grey = 0.2989*img_R+0.5870*img_G+0.1140*img_B # convert to greyscale

# image FFT
F1 = fftpack.fft2((img_grey).astype(float))
F2 = fftpack.fftshift(F1)
plt.imshow( (20*np.log10( 0.1 + F2)).astype(int))
plt.show()

(w, h) = img_grey.shape
half_w, half_h = int(w/2), int(h/2)

# high pass filter
F2[half_w-n:half_w+n+1,half_h-n:half_h+n+1] = 0 # select all but the first 50x50 (low) frequencies
plt.imshow( (20*np.log10( 0.1 + F2)).astype(int))
plt.show()

img_filtered = 1-fftpack.ifft2(fftpack.ifftshift(F2)).real

# dirt identification through masking via a threshold
mask = img_filtered <= threshold
dirt_density = np.sum(mask)/mask.size

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(13, 6))

im = axs[0].imshow(img_filtered, vmin=0, vmax=1)
axs[0].set_title(title + ", Original Image")
divider = make_axes_locatable(axs[0])
cax = divider.append_axes('right', size='5%', pad=0)
plt.colorbar(im, cax=cax)

im = axs[1].imshow(mask, vmin=0, vmax=1)
axs[1].set_title(title + ", Dirt Identification")
axs[1].text(100, 150, f'Dirt Density: {dirt_density*100:.2f}%', bbox=dict(fc='w', alpha=0.5, pad=5))

if save_bool == 1:
    plt.savefig('C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220223\\EZ\\'+file_name, bbox_inches='tight')
plt.show()
