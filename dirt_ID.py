import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

file_name = "EZ_06_1.png"
save_name = "EZ06_postetch_process_1.png"
title = "EZ06, Post Etch"
threshold = 0.72 # set identification threshold
save_bool = 1

img=mpimg.imread('C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220224\\'+file_name)

img_R = img[:,:,0]
img_G = img[:,:,1]
img_B = img[:,:,2]

img_grey = np.sinh(0.2989*img_R+0.5870*img_G+0.1140*img_B) # convert to greyscale

mask = img_grey <= threshold
dirt_density = np.sum(mask)/mask.size

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(13, 6))

im = axs[0].imshow(np.arcsinh(img_grey), vmin=0, vmax=1)
axs[0].set_title(title + ", Original Image")
divider = make_axes_locatable(axs[0])
cax = divider.append_axes('right', size='5%', pad=0)
plt.colorbar(im, cax=cax)

im = axs[1].imshow(mask, vmin=0, vmax=1)
axs[1].set_title(title + ", Dirt Identification")
axs[1].text(50, 100, f'Dirt Density: {dirt_density*100:.2f}%', bbox=dict(fc='w', alpha=0.5, pad=5))

if save_bool == 1:
    plt.savefig('C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220224\\'+save_name, bbox_inches='tight')
plt.show()
