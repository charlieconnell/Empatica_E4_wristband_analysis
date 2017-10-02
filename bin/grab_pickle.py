#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRABS PICKLED FILES AND COLLATES THEM INTO SUMMARY FILES FOR EACH MEASURE 
Created on Fri Sep  1 17:23:38 2017
@author: Charlie Connell
email: charlotte.connell@gmail.com
"""
import pickle
import pandas as pd
from os import listdir
from os.path import isfile, join

directory = '~/data/interim/'
filelist = [f for f in listdir(directory) if isfile(join(directory, f))]
fileimport = []
for file in filelist:
    if file.endswith('.p'):
        fileimport.append(file)

pickle_index = 0
pickles_df = {}
acc = pd.DataFrame()
acc.name = 'acc'
bvp = pd.DataFrame()
bvp.name = 'bvp'
eda = pd.DataFrame()
eda.name = 'eda'
hr = pd.DataFrame()
hr.name = 'hr'
ibi = pd.DataFrame()
ibi.name = 'ibi'
pickle_keys = {'acc': 3, 'bvp': 2, 'eda': 1, 'hr': 0, 'ibi': 0}

time_pre_tag = 60 #if you want longer before the tag, change this number

for pickles in fileimport:
    pickles = pickle.load(open(directory + pickles, "rb"))
    for key, value in pickle_keys.items():
        if key != 'ibi':
            pickles[key] = pickles[key].set_index('duration(s)')
            idex = pickles[key][pickles[key].tag0].index
            idex = idex[0] - time_pre_tag
            pickles[key] = pickles[key].loc[pickles[key].index > idex]
            pickles[key] = pickles[key].reset_index()
            pickles[key]['normalized_time'] = pickles[key]['duration(s)'] - pickles[key]['duration(s)'][0]
            pickles[key]['normalized_time'] = round(pickles[key]['normalized_time'], value)
            pickles[key]['participantID'] = fileimport[pickle_index]
            del pickles[key]['time_series']
            if key == 'acc':
                acc = acc.append(pickles[key])
            if key == 'bvp':
                bvp = bvp.append(pickles[key])
            if key == 'eda':
                eda = eda.append(pickles[key])
            if key == 'hr':
                hr = hr.append(pickles[key])
        else:
            pickles[key] = pickles[key].loc[pickles[key].time > idex]
            pickles[key]['participantID'] = fileimport[pickle_index] 
            ibi = ibi.append(pickles[key])
    pickles_df[fileimport[pickle_index]] = pickles

    pickle_index += 1
    
bvp_pivot = bvp.pivot(index='normalized_time', columns='participantID', values='photoplethysmograph')
eda_pivot = eda.pivot(index='normalized_time', columns='participantID', values='microsiemens')
hr_pivot = hr.pivot(index='normalized_time', columns='participantID', values='bpm')
acc_pivot = acc.pivot(index='normalized_time', columns='participantID', values='g_force')

bvp_cols = bvp_pivot.columns.tolist()
bvp_pivot[bvp_cols] = bvp_pivot[bvp_cols].fillna(method='ffill', axis=1, limit=5)
eda_cols = eda_pivot.columns.tolist()
eda_pivot[eda_cols] = eda_pivot[eda_cols].fillna(method='ffill', axis=1, limit=5)
acc_cols = acc_pivot.columns.tolist()
acc_pivot[acc_cols] = acc_pivot[acc_cols].fillna(method='ffill', axis=1, limit=5)
hr_cols = hr_pivot.columns.tolist()
hr_pivot[hr_cols] = hr_pivot[bvp_cols].fillna(method='ffill', axis=1, limit=5)

# export processed files to csv
export_path = '~/data/processed/'
acc_pivot.to_csv(export_path + 'acc.csv')
bvp_pivot.to_csv(export_path + 'bvp.csv')
eda_pivot.to_csv(export_path + 'eda.csv')
hr_pivot.to_csv(export_path + 'hr.csv')
ibi.to_csv(export_path + 'ibi.csv')

# export full dataframes to csv in interim
export_path2 = '~/data/dump/'
acc.to_csv(export_path2 + 'acc_long.csv')
bvp.to_csv(export_path2 + 'bvp_long.csv')
eda.to_csv(export_path2 + 'eda_long.csv')
hr.to_csv(export_path2 + 'hr_long.csv')
ibi.to_csv(export_path2 + 'ibi_long.csv')



