# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:37:28 2020

@author: jacqu

Compare results for different exhaustivenesses, on ligands 
"""

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

ex = 64

ref_scores = np.load(f'exp/out_scores_e64.npy', allow_pickle=True) # most precise scores 
scores = np.load(f'exp/out_scores_e{ex}.npy', allow_pickle=True)
times = np.load(f'exp/out_times_e{ex}.npy', allow_pickle=True)

AE = np.abs(np.array(scores)-np.array(ref_scores))
sns.distplot(AE)
plt.title("Distance between found pose and most precise pose (energy)")
plt.xlim(0,1)

plt.figure()
plt.title("Distribution of docking time / molecule" )
sns.distplot(times)
plt.xlim(0,250)