# Project Title

This project is designed to save time concatenating 1 m binned cnv files from Seabird into a single Excel sheet.

## Getting Started

Download the Python script and place it in a folder with the cnv files that you want to read

### Prerequisites

I used Spyder with Anaconda 3 as my Python viewer and engine. You will also need the Python Seabird library, which can be found at https://github.com/castelao/seabird


### Installing

Once Seabird is downloaded and this file is in the correct folder, feel free to try if it works with the two test cnv files uploaded.
I attached the output I get from this script using those two files as "out.xlsx".

When I run my code, my console prints:

#######################
runfile('C:/Users/zheva/Github stuff/CTD_hydro_data_concatenator/cnv_to_xlsx.py', wdir='C:/Users/zheva/Github stuff/CTD_hydro_data_concatenator')

The variables in this file are
[[0, 'timeS'], [1, 'scan'], [2, 'PRES'], [3, 'LONGITUDE'], [4, 'LATITUDE'], [5, 'DEPTH'], [6, 'TEMP'], [7, 'TEMP2'], [8, 'CNDC'], [9, 'CNDC2'], [10, 'flSP'], [11, 'CStarAt0'], [12, 'CStarTr0'], [13, 'par'], [14, 'modError'], [15, 'v0'], [16, 'v1'], [17, 'v2'], [18, 'v3'], [19, 'v4'], [20, 'v5'], [21, 'v6'], [22, 'v7'], [23, 'oxygenvoltage'], [24, 'PSAL'], [25, 'PSAL2'], [26, 'sigma-�00'], [27, 'sigma-�11'], [28, 'sbeox0Mg/L'], [29, 'sbox0Mm/Kg'], [30, 'sbeox0PS'], [31, 'flag']]

The variables being carried through this program are
['timeS', 'scan', 'PRES', 'LONGITUDE', 'LATITUDE', 'DEPTH', 'TEMP', 'TEMP2', 'CNDC', 'CNDC2', 'flSP', 'CStarAt0', 'CStarTr0', 'par', 'modError', 'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'oxygenvoltage', 'PSAL', 'PSAL2', 'sigma-�00', 'sigma-�11', 'sbeox0Mg/L', 'sbox0Mm/Kg', 'sbeox0PS', 'flag']

These files are missing the following variables and therefore these files were not concatenated.
[]

These files failed to concatenate due to a cnv formatting error. I recommend adding them manually.
[]

You have successfully written 2 cnv files into a single xlsx file named out.xlsx
##########################

fCNV can print a line of text like "This file have 26 variables". I believe that this is normal operation for the Seabird library.




Happy concatenating!
-Zach


I got this readme template from https://gist.github.com/PurpleBooth/109311bb0361f32d87a2#file-readme-template-md




