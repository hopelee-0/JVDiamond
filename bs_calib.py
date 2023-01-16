# import matplotlib.pyplot as plt
import numpy as np
import os

folder = "bs_calibrations\\"
path = "G:\\Shared drives\\Diamond team - Vuckovic group\\Data\\LN+diamond data\\20230113\\"

save_title = "20230116_bs_calibration_processed"
save_path = path

if save_bool == 1:
    f = open(save_path+save_title+".txt", "w")
    f.write(save_title+"\n")
    f.write("File, mean, std\n")

directory = path+folder
for file in os.listdir(directory):
    full_path = directory+file
    power = pd.read_csv(path+file_excite, skiprows=22, delimiter=';', decimal=',')
    mean_power = np.mean(power)
    std_power = np.std(power)
    print(file)
    print(mean_power)
    print(std_power)

    if save_bool == 1:
        f.write(file, mean_power, std_power) 
    
if save_bool == 1:
    f.close()


