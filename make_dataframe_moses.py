# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:16:21 2020

@author: jacqu

Sample random moses molecules in a dataframe with SMILES for docking
"""

import pandas as pd 
import numpy as np

import os 

df = pd.read_csv('../graph2smiles/data/moses_train.csv')

dftest = pd.read_csv('../graph2smiles/data/moses_test.csv')

# Sampling 

rd = df.sample(50000)
rd = pd.concat([rd,dftest.sample(10000)])

rd=rd.reset_index()
rd=rd.rename(columns={"index": "true_index"})

# Save 
rd.to_csv(f'C:/Users/jacqu/Documents/GitHub/vina_docking/data/ligands/moses_sample.csv')