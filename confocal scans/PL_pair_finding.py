import numpy as np
import csv

file_name = "test.csv"
path = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220414\\"+file_name

save_name = "test_pairs"
save_path = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Data\\20220414\\"+save_name

tune_range = 0.001 # value in nm

# open the file in read mode
filename = open(path, 'r')
# creating dictreader object
file = csv.DictReader(filename)

# creating empty lists to hold columns
waves = []
counts = []

# iterating over each row and append values to empty list
for col in file:
    waves.append(col["Wavelengths"])
    counts.append(col["Counts"])
