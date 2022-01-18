# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:03:06 2022

@author: Natalya Evans

This script is designed to extract the pin, depth, and time from auto-fire module files from Seabird systems, then concatenate that data into a single csv file

"""

# %% 1. Load relevant libraries
#This chunk gets all the pre-requisites out of the way for you
#Note that this code will overwrite the output file, so if there is already a file with output_name in the folder, it will be replaced

output_name='out.csv' #This is the name of the file that this code outputs. The default is output_name='out.csv'

import os


#%% 2. Create a list of btl files to iterate through
#This chunk identifies all the btl files in a folder then fills their names into a list, listofout

listoffiles = os.listdir('.') #creates the list, taken from listing 3 on https://stackabuse.com/python-list-files-in-a-directory/
pattern = "*.py" #I don't know what this does
 
listofout_temp=[0]*len(listoffiles) #creates a blank list to get filled with the filenames of files that worked
for name in listoffiles: #iterate through all files
    if '.afm' in listoffiles[listoffiles.index(name)]: #select only the .cnv files
        listofout_temp[listoffiles.index(name)]=name   #create a temporary list with empty space and only cnv files
listofout=list(filter(lambda a: a != 0, listofout_temp))  #removes the file name of the csv output from the files that get searched https://www.geeksforgeeks.org/lambda-filter-python-examples/



