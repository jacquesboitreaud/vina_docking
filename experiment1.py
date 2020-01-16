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

# Exhaustiveness to plot 
ex = 2

# Actives 
scores_a = np.load(f'exp/out_scores_e{ex}_actives.npy', allow_pickle=True)
times_a = np.load(f'exp/out_times_e{ex}_actives.npy', allow_pickle=True)

# Decoys 
scores_d = np.load(f'exp/out_scores_e{ex}_decoys.npy', allow_pickle=True)
times_d = np.load(f'exp/out_times_e{ex}_decoys.npy', allow_pickle=True)

# All times and scores 
times= times_a + times_d
scores = scores_a + scores_d


plt.figure()
plt.title("Distribution of docking time / molecule; for 100 actives + 100 inactives" )
sns.distplot(times)
plt.xlim(0,250)


# Enrichment and separate distributions 
plt.figure()
scores_a = np.delete(scores_a,np.where(scores_a==0))
scores_d = np.delete(scores_d,np.where(scores_d==0))
sns.distplot(scores_a, label = 'actives', bins=20)
sns.distplot(scores_d, label = 'decoys', bins=20)
plt.legend()

# Difference in means : 
delta = np.mean(scores_a) - np.mean(scores_d)
print('mean(a)-mean(d) = ',delta)

# Rank correlation coefficient :
d={'cat':[], 'score':[]} 
for s in scores_a:
    d['cat'].append('active')
    d['score'].append(s)
for s in scores_d:
    d['cat'].append('decoy')
    d['score'].append(s)
df = pd.DataFrame.from_dict(d)

df=df.sort_values('score')
percent = 10 
pct = int(percent*df.shape[0]/100)
top_df = df.iloc[:pct]
e = top_df[top_df['cat']=='active'].shape[0]/ max(top_df[top_df['cat']=='decoys'].shape[0],1)
print(f'enrichment at {percent}% over {df.shape[0]} molecules : {e} // exhaustiveness = {ex}')