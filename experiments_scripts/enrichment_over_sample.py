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


df = pd.read_csv('../data/scored_exp/drd3_dude_scored_64_1mode.csv')

actives = df[:100]
decoys = df[100:]
na, nd, ntot = actives.shape[0], decoys.shape[0] , df.shape[0]

# Enrichment and separate distributions 
plt.figure()

#sns.distplot(decoys['drd3'], label = 'decoys', bins=20)

p=sns.color_palette()

df_docking = pd.read_csv('../../graph2smiles/data/moses_sc_f.csv')
df_docking = df_docking[df_docking['drd3']<0]
sns.distplot(df_docking['drd3'], bins=20,color=p[0], label='random ZINC')
sns.distplot(actives['drd3'], label = 'actives', color='green', bins=20)

plt.xlabel('Energy (kcal/mol)')
plt.xlim(-12,-4)
plt.legend()
#plt.title(f'Distributions for sample with {na} actives and {nd} decoys')

# Difference in means : 
delta = np.mean(actives['drd3']) - np.mean(decoys['drd3'])
print('mean(a)-mean(d) = ',delta)


# Enrichment factor
df=df.sort_values('score')
percent = 5
pct = int(percent*df.shape[0]/100)
top_df = df.iloc[:pct]

# ef = pct actives in top k% divided by pct actives in the whole dataset 
ef = (top_df[top_df['active']==1].shape[0]/pct) / (na/ntot)
print(f'enrichment at {percent}% over {df.shape[0]} molecules : {ef} // exhaustiveness = 4')

# Time versus smiles length 
plt.figure()
lens = np.array([len(s) for s in df['can']])
sns.lineplot(x=lens, y=df['time'])
plt.ylabel('Time per molecule (s),')
plt.xlabel('length of SMILES string (number of chars)')
plt.title('Docking time vs molecule size // 24 cores, exhaustiveness = 4')