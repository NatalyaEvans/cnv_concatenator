# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:19:39 2021

Author: Natalya Evans

Designed to read in btl files, which contain hydro data for where bottles were 
fired, and output them into a large, comprehensive spreadsheet as well as a 
smaller spreadsheet for easy pasting. Note that this file is designed to read 
in .btl files generated from OC2102A. It is formatted to rearrange the columns 
using the column structure of the .btl files I have generated and uploaded.

Last updated 17 Apr 2021 with more comments to put in shared lab drive and Github

"""

# %% 1. Load relevant libraries and custom settings
#This chunk gets all the pre-requisites out of the way for you
#Note that this code will overwrite the output file, so if there is already a file with output_name in the folder, it will be replaced

output_name1='out_all.xlsx' #This is the name of the file containing all read data that this code outputs. The default is output_name='out_all.xlsx'
output_name2='out_short.xlsx' #This is the name of the file containing data formatted for the sampling log that this code outputs. The default is output_name='out_short.xlsx'
headerstartstring='bottlesum_in' #first word of the last line in the metadata. Used to indicate where to start concatenating data

import os
import pandas as pd

#%% 1a. This chunk can be used to view the entire data file, which allows you to select where to cut different things

#f = open('014.btl', 'r') # open the file
#data = f.read() # read the file
#f.close() # close the file

#%% 2. Create a list of btl files to iterate through
#This chunk identifies all the btl files in a folder then fills their names into a list, listofout

listoffiles = os.listdir('.') #creates the list, taken from listing 3 on https://stackabuse.com/python-list-files-in-a-directory/
pattern = "*.py" #I don't know what this does
 
listofout_temp=[0]*len(listoffiles) #creates a blank list to get filled with the filenames of files that worked
for name in listoffiles: #iterate through all files
    if '.btl' in listoffiles[listoffiles.index(name)]: #select only the .cnv files
        listofout_temp[listoffiles.index(name)]=name   #create a temporary list with empty space and only cnv files
listofout=list(filter(lambda a: a != 0, listofout_temp))  #removes the file name of the csv output from the files that get searched https://www.geeksforgeeks.org/lambda-filter-python-examples/

#%% 3. Read the files into a list of lists
#This chunk uses the first file to write the header, and the variable order is based on the dataset it was built for and might need adjusting

out=[0]
metadata=1 # binary variable to indicate if currently in the metadata section
header=0 # binary variable to indicate if this line is the header line
timeind=1 # time is currently read in on every other line. This represents the index for where we want to put the time variable in the header.
header=0 # binary variable to indicate if this line is the header line

for entry in listofout: #loop through the rest of the files
    metadata=1 # binary variable to indicate if currently in the metadata section
    timeind=1 # time is currently read in on every other line. This represents the index for where we want to put the time variable in the header.
    f = open(entry, 'r') # open the file
    for line in f:
        line.strip() # what each line says, with invisible text stripped
        if header==1 and entry==listofout[0]: # checks if the header is there and if its the first file. Needs to be above the headerstart string loop because the header follows the line that checks for
            out[0]=line.split()  # initializes the list of list to add to data to
            out[0].insert(timeind,'Time') # insert a column name for the time column we move in
            out[0].insert(timeind+1,'Month') # the split() column splits the day up, so add an extra label
            out[0].insert(timeind+1,'Day') # the split() column splits the day up, so add an extra label
            out[0].insert(0,'Station') # put in a header for which station it is
            header=0 # resets the header variable so it doesn't get overwritten
        if headerstartstring in line: # checks for the last line of metadata is present
            metadata=0 # switches binary to 0, recording starts
            header=1 # indicates that the NEXT LINE will be the header, so the header code has to be above this
        if metadata==0: # this is the data that we look at
            if 'avg' in line: # primary row
                columns = line.split() # pull out columns
                del columns[-1] # remove the "avg" text
            if 'sdev' in line: # secondary column with time
                columns2=line.split() # separate into rows
                columns.insert(timeind,columns2[0]) # add time to main columns
                columns.insert(0,entry[0:3]) # add the station number as a 3 digit number using the btl filename
                out.append(columns) # aggregate data
    if entry==listofout[0]: # only for the first file, fix an issue with the header
        del out[-1] # remove the last entry, which is a remnant of the header
    f.close() # close the file
    
#%% 4. Convert to a pandas dataframe

fullout=out[1:] # all the data but the header
header=out[0] # header
fullout=pd.DataFrame(fullout, columns=header)

#%% 5. Process data structure

fullout=fullout.drop(header[1],axis=1) # remove the bottle column because it's useless

cols = fullout.columns.tolist() # get the column headers
myorder = [0,1,2,3,4,5,6,9,16,7,8,10,11,12,13,14,15,17,18,19] # order of column headers I desire
cols2 = [cols[i] for i in myorder] # rearange header
fullout = fullout[cols2] # rearrange dataframe
fullout.to_excel(output_name1,index=False) #outputs the concatenated data. Change the file name by adjusting "ouput_name" at the top. Index referes to unique numbers on the left side of the xlsx sheet, these aren't really needed.  

#%% 6. Average and write short dataset

myorder=[17,18,11,12,9,10,14,15,16,0,7]
cols3 = [cols2[i] for i in myorder] # rearange header
tempframe=fullout[cols3]
#tempframe.convert_objects(convert_numeric=True)
#shortout=pd.to_numeric(tempframe[cols3])

shortout=pd.DataFrame()
for i in cols3:
    shortout[i]=pd.to_numeric(tempframe[i])

shortout['temp'] = shortout[cols3[0:2]].mean(axis=1)
shortout['sal'] = shortout[cols3[2:4]].mean(axis=1)
shortout['oxy'] = shortout[cols3[4:6]].mean(axis=1)
shortout['pdens'] = shortout[cols3[7:9]].mean(axis=1)
shortout=shortout.drop(cols3[0:6]+cols3[7:9],axis=1) # remove the columns that were averaged

cols4 = shortout.columns.tolist() # get the column headers
myorder=[1,2,3,4,5,0,6]
cols4 = [cols4[i] for i in myorder] # rearange header
shortout=shortout[cols4] # format output into easily pastable structure
shortout.to_excel(output_name2,index=False) #outputs the concatenated data. Change the file name by adjusting "ouput_name" at the top. Index referes to unique numbers on the left side of the xlsx sheet, these aren't really needed.  




