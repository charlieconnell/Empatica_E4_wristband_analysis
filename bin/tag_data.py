#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

TAG DATA
Created on Thu Aug 31 12:03:40 2017
@author: Charlie Connell
email: charlotte.connell@gmail.com

"""

# import relevant packages
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pickle
import math

# obtain the filepath and participant name by getting user to pick file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
filename_sep = file_path.split('/')
participant_ID = filename_sep[-1][:-4]

# derive info from tag sheet
tags_info = pd.read_excel(file_path, sheetname='tags', header=None)
tags = round(tags_info.iloc[:,0],0)

# import other sheets as dataframes
acc = pd.read_excel(file_path, sheetname='ACC', header=None)
bvp = pd.read_excel(file_path, sheetname='BVP', header=None)
eda = pd.read_excel(file_path, sheetname='EDA', header=None)
hr = pd.read_excel(file_path, sheetname='HR', header=None) 
ibi = pd.read_excel(file_path, sheetname='IBI', header=None)
temp = pd.read_excel(file_path, sheetname='TEMP', header=None)

# derive recording start time and sampling rate for each measure

acc = {'start_time': acc.iloc[0,0], 'sampling_freq': acc.iloc[1,0], 'data': acc.iloc[2:,:]}
acc['data'].columns = ['x','y','z']

def g_force(columns):
    return math.sqrt(columns[0] * columns[0] + columns[1] * columns[1] + columns[2] * columns[2])

acc['data']['g_force'] = acc['data'][['x', 'y', 'z']].apply(lambda x: g_force(x), axis=1)

bvp = {'start_time': bvp.iloc[0,0], 'sampling_freq': bvp.iloc[1,0], 'data': bvp.iloc[2:,:]}
bvp['data'].columns = ['photoplethysmograph']
eda = {'start_time': eda.iloc[0,0], 'sampling_freq': eda.iloc[1,0], 'data': eda.iloc[2:,:]}
eda['data'].columns = ['microsiemens']
hr = {'start_time': hr.iloc[0,0], 'sampling_freq': hr.iloc[1,0], 'data': hr.iloc[2:,:]}
hr['data'].columns = ['bpm']
ibi = {'start_time': ibi.iloc[0,0],  'data': ibi.iloc[1:,:]}
ibi['data'].columns = ['time', 'ibi_duration']
# create time series for each measure (excl ibi) and add in tags
df_list = [acc, bvp, eda, hr]

for i in df_list:
    sample_rate = i['sampling_freq']
    start = i['start_time']
    stop = start + (len(i['data'])/sample_rate)
    time_series = np.linspace(start, stop, num=len(i['data'])).tolist()
    duration_start = 0
    duration_stop = len(i['data'])/sample_rate  
    #  duration = np.linspace(duration_start, duration_stop, num=len(i['data'])).tolist()
    data = i['data']
    data['time_series'] = time_series
    data['duration(s)'] = time_series - start
    if str(type(tags)) == "<class 'numpy.float64'>":
        data['tag'] = (data[['time_series']] > tags) & (data[['time_series']] < tags + 1)
        i['data'] = data
    elif str(type(tags)) == "<class 'pandas.core.series.Series'>":
        for j in range(len(tags)):
            data['tag' + str(j)] = (data[['time_series']] > tags[j]) & (data[['time_series']] < tags[j] + 1)
            i['data'] = data

# create dictionary of data
data_dict = {'acc': acc['data'], 'bvp' : bvp['data'], 'eda' : eda['data'], 'hr' : hr['data'], 'ibi' : ibi['data']}

# insert the path to the folder you want data to export to
writing_directory = '~/data/interim/'

# save data dictionary as a pickled file
pickle.dump(data_dict, open(writing_directory + participant_ID + '.p', "wb"))
