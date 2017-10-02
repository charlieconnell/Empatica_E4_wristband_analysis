#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMPORTS DATA FILES FROM A SUBJECT FOLDER AND COMBINES INTO ONE EXCEL FILE
Created on Tue Aug 22 11:03:58 2017
@author: Charlie Connell
email: charlotte.connell@gmail.com

"""
# import relevant packages

import pandas as pd
from tkinter import filedialog
import os
from os import listdir
from os.path import isfile, join


# prompt user to select the folder that contains the participant data of interest
directory = filedialog.askdirectory()
os.chdir(directory)

# insert the path to the folder you want files to export to
writing_directory = '~/data/raw/'

# use folder name to assign unique identifier
filename_sep = directory.split('/')
participant_identifier = 'Participant_' + filename_sep[-1]

# obtain the list of files in the subject data directory
filelist = [f for f in listdir(directory) if isfile(join(directory, f))]
fileimport = []
for file in filelist:
    if file.endswith('.csv'):
        fileimport.append(file)

# import all the .csv files within the participant folder as a dictionary of data frames
dfs = {}
for datasheet in fileimport:
    dfs[datasheet[:-4]] = pd.read_csv(directory + '/' + datasheet, header=None)

#initialise the excel writer
writer = pd.ExcelWriter(writing_directory + participant_identifier + '.xls', engine='xlsxwriter')

#now loop through and put each dataframe on a specific sheet
for sheet, frame in  dfs.items(): 
    frame.to_excel(writer, sheet_name = sheet, index=False, header=False)

#critical last step
writer.save()




        
        
