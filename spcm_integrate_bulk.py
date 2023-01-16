import numpy as np
import os

folder = "Confocal_Sat_PL01/"
path = "G:/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20221214/"

save_title = "202211214_Confocal_PL01"
save_path = path

save_bool = 1

if save_bool == 1:
    f = open(save_path+save_title+".txt", "w")
    f.write(save_title+"\n")
    print('created file')

directory = path+folder
for file in os.listdir(directory):
    full_path = directory+file
    time, counts = np.loadtxt(full_path, unpack=True, skiprows=1)
    avg = np.mean(counts)
    print(file)

    if save_bool == 1:
        f.write(str(file)+', '+str(avg)+'\n')
        print('written')
f.close()
