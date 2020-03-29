# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:16:21 2020

@author: jacqu

Samples random molecules in a dataframe with SMILES for docking
"""

import pandas as pd 
import numpy as np

import os 
import argparse

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-df", "--dataframe_path", default='data/ligands/my_ligands.csv', 
                        help="Path to csv file with 'can' columns containing smiles")
    parser.add_argument("-n", "--num_samples", default=16, help="Number of molecules to sample")
    parser.add_argument("-e", "--exclude", default='data/ligands/docked.csv', help="Molecules to exclude from sample")
    
    # ========
    
    args = parser.parse_args()

    if args.exclude !=None:
        done = pd.read_csv(args.exclude)
    
        prev_docked=set(done['can'])
        print(len(prev_docked), 'molecules already docked will be excluded from sample')
    
    df = pd.read_csv(args.dataframe_path)
    
    # Sampling 
    
    rd = df.sample(args.num_samples)
    
    rd=rd.reset_index()
    rd=rd.rename(columns={"index": "true_index"})
    
    todrop=[]
    for i, row in rd.iterrows():
        if(args.exclude !=None):
            if row['can'] in prev_docked:
                todrop.append(i)
            
    rd = rd.drop(todrop)
    rd=rd.reset_index(drop=True)
    
    # Save 
    print('>>> Saving csv subset to ~/docking_sample.csv')
    rd.to_csv('docking_sample.csv')