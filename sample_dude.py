# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:16:21 2020

@author: jacqu


Sample DUDE molecules in a dataframe with SMILES for docking. 
N_a actives and N_d decoys for each target. 
Path to DUDE download must be provided
"""

import pandas as pd 
import numpy as np

import os 

tars = [ 'braf', 'csf1r','ddp4', 'dyr',\
        'grik1','hdac8','jak2','lck','lkha4','mapk2','met','mk10','plk1',\
        'pnph','urok','wee1']

# If subsample, will select 100 random actives and 900 random decoys from DUDE.
subsample = True 

dud_repo = 'C:/Users/jacqu/Documents/mol2_resource/dude/all'
os.chdir(dud_repo)


for target_folder in os.listdir(dud_repo):
    if(target_folder in tars):
        smiles, active, decoy = [], [], []
        
        with open(f'{target_folder}/actives_final.ism', 'r') as f : 
            actives = f.readlines()
            for l in actives :
                s=l.split(' ')[0]
                if('9' in s or 'p' in s or ' ' in s or '.' in s or len(s)>150):
                    next
                else:
                    smiles.append(s)
                    active.append(1)
                    decoy.append(0)
            
    
        with open(f'{target_folder}/decoys_final.ism', 'r') as f : 
            dec = f.readlines()
            for l in dec :
                s=l.split(' ')[0]
                if('9' in s or 'p' in s or ' ' in s or '.' in s or len(s)>150):
                    next
                else:
                    smiles.append(s)
                    active.append(0)
                    decoy.append(1)
   
         
        df = pd.DataFrame.from_dict({'can':smiles, 'active':active, 'decoy':decoy})
        
        df['other']=0
        
        if(subsample): # Sample random actives and random decoys 
            rand_actives=df[df['active']==1].sample(100)
            rand_decoys = df[df['decoy']==1].sample(900)
            
            df = pd.concat([rand_actives,rand_decoys])
            df=df.reset_index(drop=True)
            
        # Save 
        df.to_csv(f'C:/Users/jacqu/Documents/GitHub/vina_docking/data/ligands/{target_folder}_dude.csv')