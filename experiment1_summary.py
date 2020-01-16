# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:33:32 2020

@author: jacqu

Summary of experiment conducted for different exhaustiveness params 
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Exhaustiveness to plot 
exs = [2,4,8,16,32,64]

avg_t=[]
deltas = []

for ex in exs : 
    
    # Actives 
    scores_a = np.load(f'exp/out_scores_e{ex}_actives.npy', allow_pickle=True)
    times_a = np.load(f'exp/out_times_e{ex}_actives.npy', allow_pickle=True)
    
    # Decoys 
    scores_d = np.load(f'exp/out_scores_e{ex}_decoys.npy', allow_pickle=True)
    times_d = np.load(f'exp/out_times_e{ex}_decoys.npy', allow_pickle=True)
    
    scores_a = np.delete(scores_a,np.where(scores_a==0))
    scores_d = np.delete(scores_d,np.where(scores_d==0))
    
    # All times and scores 
    times= times_a + times_d
    
    delta = np.mean(scores_a) - np.mean(scores_d)
    
    avg_t.append( np.mean(times))
    deltas.append(delta)

#plot
sns.lineplot(exs, avg_t)
plt.xlabel('exhaustiveness')
plt.ylabel('Average time / molecule (seconds)')
plt.figure()
sns.lineplot(exs, deltas)
plt.xlabel('exhaustiveness')
plt.ylabel('Difference in average affinities (kcal/mol)')
    
    