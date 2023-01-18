# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

folder = "power calib/"
path = "/mnt/g/Shared drives/Diamond team - Vuckovic group/Data/LN+diamond data/20230116/confocal sat curve/"

save_title = "20230116_confocal_sat_curve_001"
save_path = path

save_bool = 1

if save_bool == 1:
    f = open(save_path+save_title+".txt", "w")
    f.write(save_title+"\n")
    f.write("File, mean, std\n")

directory = path+folder
for file in os.listdir(directory):
    full_path = directory+file
    data = pd.read_csv(full_path, skiprows=22, delimiter=';', decimal=',')
    power = np.asarray(data['Power (W)'])
    mean_power = np.mean(power)
    std_power = np.std(power)

    if save_bool == 1:
        f.write("{}, {}, {}\n".format(str(file), mean_power, std_power)) 
    
if save_bool == 1:
    f.close()


