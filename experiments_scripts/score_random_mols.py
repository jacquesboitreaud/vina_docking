# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:37:28 2020

@author: jacqu

Compare results for different exhaustivenesses, on 100 actives and 100 decoys
"""

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('../../rupert_scored.csv')
df=df[df['score']<0]

# Enrichment and separate distributions 
plt.figure()
plt.xlim(-12,-4)
sns.distplot(df['score'], label = 'random sample', bins=20, norm_hist=False, color = 'green')
plt.xlabel('Energy (kcal/mol)')
plt.legend()
plt.title(f'Distributions for {df.shape[0]} molecules')


# Actives and decoys to compare : 

df = pd.read_csv('../data/scored/drd3_dude_scored.csv')
actives = df[df['active']==1]
decoys = df[df['decoy']==1]
na, nd, ntot = actives.shape[0], decoys.shape[0] , df.shape[0]

# Enrichment and separate distributions 
sns.distplot(actives['score'], label = 'actives', bins=20, norm_hist=False)
sns.distplot(decoys['score'], label = 'decoys', bins=20, norm_hist=False)
plt.legend()


# Time versus smiles length 
plt.figure()
lens = np.array([len(s) for s in df['can']])
sns.lineplot(x=lens, y=df['time'])
plt.ylabel('Time per molecule (s),')
plt.xlabel('length of SMILES string (number of chars)')
plt.title('Docking time vs molecule size // 24 cores, exhaustiveness = 4')


