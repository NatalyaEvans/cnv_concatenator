# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 13:31:35 2020
Last updated Jan 5 2020

@author: zheva

This script is designed to concatenate all of the Seabird cnv files in a single folder into an Excel sheet, which this script writes.
It uses a pre-existing python library called "Seabird" for parsing the cnv files. You must download this library before this code works.
This script reads through all files that contain ".cnv" in the folder that this script sits in, so you must organize this folder to concatenate the files you desire.
If this library cannot read the cnv, this script does not concatenate that file and reports that it failed

This code is designed to run in chunks. The third chunk allows the user to view which variables are present in the cnv
The next chunk, chunk 4, allows the user to select which variables they do not want in the output csv
Nevertheless, if you know which variables you want to keep, you can run the entire code in one go.
If you open this code, start running chunks, and chunk 3 doesn't work, run the code in its entirety. There appears to be an issue with setting the path using chunks
versus running the whole thing.

"""
# %% 1. Load relevant libraries
#This chunk gets all the pre-requisites out of the way for you
#Note that this code will overwrite the output file, so if there is already a file with output_name in the folder, it will be replaced

output_name='out.xlsx' #This is the name of the file that this code outputs. The default is output_name='out.xlsx'

import seabird
from seabird.cnv import fCNV
from seabird.exceptions import CNVError
import numpy as np
import numpy.ma as ma
import os
import pandas as pd

#If chunk 2 does not populate a listofout, it is likely that the current working directory is not in the correct location. The following three lines of code in this chunk could help.
#Alternatively, running the entire script at once, rather than chunks, fixed this issue for me every time I tried it.

#print(os.getcwd)
#ROOT_PATH = os.path.dirname(os.path.abspath('cnv to csv_backup.py')) # #https://stackoverflow.com/questions/21934731/how-to-set-current-working-directory-in-python-in-a-automatic-way
#myfile_path = os.path.join(ROOT_PATH, "cnv to csv_backup.py")

#%% 2. Create a list of cnv files to iterate through
#This chunk identifies all the cnv files in a folder then fills their names into a list, listofout

listoffiles = os.listdir('.') #creates the list, taken from listing 3 on https://stackabuse.com/python-list-files-in-a-directory/
pattern = "*.py" #I don't know what this does
 
listofout_temp=[0]*len(listoffiles) #creates a blank list to get filled with the filenames of files that worked
for name in listoffiles: #iterate through all files
    if '.cnv' in listoffiles[listoffiles.index(name)]: #select only the .cnv files
        listofout_temp[listoffiles.index(name)]=name   #create a temporary list with empty space and only cnv files
listofout=list(filter(lambda a: a != 0, listofout_temp))  #removes the file name of the csv output from the files that get searched for energies https://www.geeksforgeeks.org/lambda-filter-python-examples/

# %% 3. View variables of selected cnv
#This chunk allows you to view which variables are in these cnv's so you can select which ones to keep.
#If this chunk of code returns CNVError, it is likely that the first file cannot be read. Change the first line of code in this chunk to try a different file

file = fCNV(listofout[0]) #selects which cnv file to set the order of variables with. Default is file = fCNV(listofout[0])
vars=file.keys() #read the variables so you can select which ones to carry through
print('')
print('The variables in this file are')
print([[vars.index(i), i] for i in vars])


# %% 4. Which variables do you want?
#This chunk allows you to ignore specific variables from the cnv files so they are not carried over into the output.
#All of the cnv files you are concatenating must have the variables specified in vars2

#Select the variables you want to output
vars2=file.keys() #Pick which variables you want to follow through with. This command must be repeated if you want run this chunk several times in a row

#insert the index of the variables you do not want to carry through. The indexes are printed in chunk three. If you want a complete copy, remove=[]. If you want to remove variable 4 and 5, remove=[4,5].
#remove=[4,5,23] #use this format to remove some variables
remove=[] #use this format to remove no variables


[vars2.remove(vars[i]) for i in remove]; #removes variables from vars2 as specified by their index in vars
print('')
print('The variables being carried through this program are')
print(vars2)

# %% 5. Generate the output list of lists and print which files don't work
fail=list() #create a list of file names that the cnv reader couldn't read
diffvar=list() #create a list of file names that don't have all the variables in vars2 requests

if 'data' in globals(): #data is the object that concatenates all of the cnv values. We clear it before concatenation in case this code is ran multiple times.
    del data

for entry in listofout: #loop through all the files
    try:
        file = fCNV(entry) #checks if the seabird package can read the cnv
    except (CNVError):  #if seabird can't read the cnv, 
        fail.append(entry) #store which files couldn't be read
        continue
    else:                   #business as usual, the file can be read
        vars=file.keys() #check which variables are in the file
        if False in [i in vars for i in vars2]: #checks if the variables you're looking for are in this cnv
            badvars = [vars2[i] for i, x in enumerate([i in vars for i in vars2]) if x == False] #provides which variables in vars2 are not present
            diffvar.append([entry,badvars]) #label which file doesn't have the correct variables
            break   #if a variable isn't present, stop concatenating this file and proceed with the next file
        temp=list() #create a dummy list to fill with data from each cnv, and wipe it for each cnv
        for i in vars2: #for each variable
            col=ma.getdata(file[vars2[vars2.index(i)]]).tolist()  #extract each variable from the cnv and convert it into a list. I believe that this command ignores any data masks, like -999, that might be applied to the data
            temp.append(col) #create a list of lists with all the selected variables in a given cnv
            #There needs to be a line that appends each col individually to temp2 here, where temp 2 accumulates each run because it concatenates every cnv
    temp2=np.array(temp) #converts the dummy list into a numpy array to concatenate it
    if not 'data' in globals(): #this is the base case to generate the object that will be concatenated
        data=temp2 #defines the concatenation variable
    else:
        data = np.concatenate((data, temp2), axis=1) #if the concatentation variable exists, concatenate to it
        
print('')
print('These files are missing the following variables and therefore these files were not concatenated.')
print(diffvar)

print('')
print('These files failed to concatenate due to a cnv formatting error. I recommend adding them manually.')
print(fail)
            
 # %% 6. Output the data file  
data2 = data.T #transpose your output
data2=pd.DataFrame(data2,columns=vars2) #converts your data into a panda dataframe to make the output xlsx file easier to generate
data2.to_excel(output_name,index=False) #outputs the concatenated data. Change the file name by adjusting "ouput_name" at the top. Index referes to unique numbers on the left side of the xlsx sheet, these aren't really needed.  

print('')
print("You have successfully written "+str(len(listofout)-len(fail)-len(diffvar)) +" cnv files into a single xlsx file named " +str(output_name))

