# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:16:21 2020

@author: jacqu

Sample random moses molecules in a dataframe with SMILES for docking
"""

import pandas as pd 
import numpy as np

import os 


done = pd.read_csv('C:/Users/jacqu/Documents/GitHub/vina_docking/data/ligands/moses_sample.csv')

prev_docked=set(done['can'])
print(len(prev_docked), 'molecules already docked')

df = pd.read_csv('../graph2smiles/data/moses_train.csv')

# Sampling 

rd = df.sample(100000)

rd=rd.reset_index()
rd=rd.rename(columns={"index": "true_index"})

todrop=[]
for i, row in rd.iterrows():
    if row['can'] in prev_docked:
        todrop.append(i)
        
rd = rd.drop(todrop)
rd=rd.reset_index(drop=True)

# Save 

rd.to_csv('docking1.csv')