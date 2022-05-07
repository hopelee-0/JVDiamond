### 20220416 - Final Data Processing Programme for Hope
'''
Given input csv. file with wavelengths and count data, this programme
allows the user to search in which lines of the file each wavelength shows up,
up to a tolerance to be specified.
'''

### PACKAGES
import csv
import numpy as np


#### HELPERS
def convert_string_to_list(input_str):
    '''
    Each row[0] in the input csv file is a string in the form
    '[wavelengths]'. Each row[1] has the form '[counts]'. Given
    any of two such strings as an input, this function coverts it to
    a list of the wavelenghts/counts. For instance,
    '[734.7966182  737.68852946 740.71152399 748.59581629]'
    becomes [734.7966182, 737.68852946, 740.71152399, 748.59581629].
    '''
    ### DROP FIRST AND FINAL BRAKETS
    input_no_brakets = input_str[1: len(input_str) - 1]
    ### MAKE LIST W/ STR VERSION OF FLOAT DATA
    cleaned = input_no_brakets.split()
    ### CONVERT TO STRS TO FLOAT
    final = [float(wavelength) for wavelength in cleaned]
    ### RETURN FINAL RESULT
    return final


### MAIN
def process_data(filename, tolerance):
    '''
    Processes input data file. Returns dictionary displaying
    in which line of the csv. file input each wavelength value is
    found, up to a specified tolerance.
    '''
    wavelengths_dict = {}
    ### OPEN TEST FILE
    with open(filename) as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        line_count = 0
    ### LOOP OVER ALL LINES IN FILE
        for row in csv_reader:
        # DO DATA LINES
            if line_count % 2 == 0 and line_count > 0:
                line_count += 1
                # Set-up
                wavelengths = convert_string_to_list(row[0]) # convert WL data to list of WLs
                for wavelength in wavelengths: # access each individual WL
                    rounded_wavelength = np.round(wavelength, tolerance)
                # If wavelength of interest, up to tolerance, is not in dict, add it
                    if rounded_wavelength not in wavelengths_dict:
                        wavelengths_dict[rounded_wavelength] = []
                # Add line location to corresponding wavelength entry
                    wavelengths_dict[rounded_wavelength].append(line_count)
        # SKIP EMPTY LINES AND TITLE
            else:
                line_count += 1
    ### OUTPUT
    print('Walengths rounded to ' + str(tolerance) + ' decimals ' + 'found in .csv file in lines:\n')
    print(wavelengths_dict)
    print('\n All done! Yayyy!')
    print('\n\n')
    return wavelengths_dict


### TEST
dat = process_data('test.csv', 3)
print(dat)
