# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:03:06 2022
@author: Nathan Chan
This script is designed to extract the pin, depth, and time from auto-fire module files from Seabird systems, then concatenate that data into a single csv file
This script is specifically designed for the filenames used on OC2107A
"""

# %% 1. Load relevant libraries
#This chunk gets all the pre-requisites out of the way for you
#Note that this code will overwrite the output file, so if there is already a file with output_name in the folder, it will be replaced
#This is the name of the file that this code outputs. The default is output_name='out.csv'
output_name='out.csv'
import os, fnmatch, csv, re
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
#%% 2. Create a list of btl files to iterate through
#This chunk identifies all the btl files in a folder then fills their names into a list, listOfFiles
listOfFiles = os.listdir('.') #gets all the files in the directory
pattern = "*.afm" #filters what files get added into the listOfAFM list
listOfAFM = [] #a list to hold all the .afm file names
#gets a list of file names
for name in listOfFiles: #iterate through all files and add files that have .afm
    if fnmatch.fnmatch(name, pattern):
            name = name.lower()
            listOfAFM.append(name)
print("files to be read: ")
print(listOfAFM)
#%% 3. iterates through each file and scans for pin numbers; when it finds a pin number, it takes the next 5 lines of hex numbers and calculates depth
#saves the station, cast, pin, time, and depth into a list of dictionaries that will be exported into a csv
print("reading through " + str(len(listOfAFM)) + " files and keeping track of its data")
listOfAFM.sort(key=lambda f: int(re.sub('\D', '', f))) #sorts files based on numbers
total_data = [] #list to hold the data
for filename in listOfAFM: #loop through every file with .afm
    with open(filename) as file: #open the file
        for line in file: #scan through every line in the file
            if line[0].isnumeric(): #check to see if file line holds important data
                HexString = file.readline() 
                HexString = HexString.strip() #take out whitespace
                if "E+" in HexString: #check if in scientific notation
                    HexString = HexString[ :HexString.find("E")] #splice out the important number
                    HexString = HexString.replace(".", "") #remove the decimal
                else:
                    HexString = HexString[1:4] #splice out the important number
                HexString = "0x" + HexString #convert the hexstring into a hex value
                HexInt = int(HexString, 16)#convert hex into int
                HexInt -= 100 #subtract 100 from the int value
                line = line.split() #split the line into individual words and numbers
                dataDict = {} #dictionary to hold important information from each line
                #dataDict["File"] = filename[:filename.find(".")-len(filename)] (if uncommented out, need to add "File" to fieldnames)
                for z in filename.split()[-1]: #if the sta was improperly formatted, finds the first digit to use later
                    if z.isdigit():
                        number = filename.split()[-1].find(z)
                        break
                dataDict["Station"] = filename.split()[-1][number:filename.find(".")-len(filename)].replace("_", ".") #sets station to station number in filename 
                dataDict["Cast"] = filename.split()[1] #sets cast to cast number in file name
                dataDict["Pin"] = line[0] # sets pin to pin number on line
                dataDict["Time"] = [s for s in line if ":" in s][0] #sets time to timevalue in line
                dataDict["Depth"] = int(round(HexInt, 0)) #averages the 5 trials and rounds to whole number #sets depth to calculated average depth of the 5 hex numbers
                total_data.append(dataDict) 
                

#%% 4. outputs to a csv with "Station", "Cast",  "Pin", "Time", "Depth" as its field names
print("outputting a heading and " + str(len(total_data)) + " lines of data into " + output_name)
with open(output_name, "w") as outputFile: #opens/makes a csv file
    fieldnames = ["Station", "Cast",  "Pin", "Time", "Depth" ] #these are the fieldnames for the csv
    writer = csv.DictWriter(outputFile, fieldnames=fieldnames, lineterminator='\n') #makes a dictwriter to write data into the csv
    total_data = sorted(total_data, key = lambda i: (float(i['Station']), float(i['Cast']), (float(i['Pin'])))) #sort by station then cast then pin
    writer.writeheader() #writes the header
    for row in total_data: #writes all the data from total_data into the csv
        writer.writerow(row)