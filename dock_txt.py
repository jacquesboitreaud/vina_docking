# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:19:35 2020

@author: jacqu

Main script to run vina docking on molecules stored in .txt file  (1 smiles strings per line, ending \n)
    
    Directory with individual mol2 files 
    Path to receptor PDB file 
    exhaustiveness 
    Suffix for scores file output 
    
(Paths for compute canada server and rupert) 

"""

import sys
import subprocess
import os 
import shutil
import argparse
from time import time
import numpy as np

import openbabel
import pybel 
import pandas as pd
  
def cline():
    # Parses arguments and calls main function with these args
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-t", "--target", default='aa2ar', help="prefix of pdb receptor file. PDB file should be in data/receptors")
    parser.add_argument("-i", "--input_path", default='data/ligands/sample.txt', 
                        help="Path to csv file with 'can' columns containing smiles")
    parser.add_argument("-o", "--out_dataframe_path", default='data/scored/my_ligands_scored.csv', 
                        help="Path to csv file for saving scores")
    parser.add_argument("-s", "--server", default='rup', help="Server to run the docking on, for path and configs.")
    parser.add_argument("-e", "--ex", default=16, help="exhaustiveness parameter for vina. Default to 8")
    args = parser.parse_args()
    
    main(args)
    
def main(args):
    # Runs the docking process with the args provided
    
    
    if(args.server=='rup'):
        home_dir='/home/mcb/users/jboitr'
        install_dir = '/home/mcb/users/jboitr/local'
    elif(args.server=='cedar'):
        home_dir='/home/jboitr/projects/def-jeromew/jboitr'
        install_dir = '/home/jboitr/projects/def-jeromew/docking_setup'
    else:
        print('Error: no install of vina/mgltools found for this server.')
    
    # Uncomment to Copy receptor file from the DUDE dir if first time using this target. 
    #shutil.copyfile(f'/home/mcb/users/jboitr/data/all/{args.target}/receptor.pdb',f'data/receptors/{args.target}.pdb')
    
    receptor_filepath = f'data/receptors/{args.target}.pdb'
    
    # target to pdbqt 
    subprocess.run(['python3','pdb_select.py',f'{receptor_filepath}','! hydro', f'{receptor_filepath}'])
    subprocess.run([f'{install_dir}/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_receptor4.py',
                    f'-r {home_dir}/vina_docking/{receptor_filepath}','-o tmp/receptor.pdbqt', '-A hydrogens'])
    
    # Iterate on molecules
    with open(args.input_path,'r') as f:
        lines = f.readlines()
        mols_list = [l.split()[1] for l in lines]
        seed_list = [l.split()[0] for l in lines]
        
    mols_df = pd.DataFrame.from_dict({'can':mols_list,'seed':seed_list})
    mols_df['score'], mols_df['time'] = pd.Series(dtype=np.float64), pd.Series(dtype=np.float64)
    
    print(f'Docking {len(mols_list)} molecules')

    
    for i,smi in enumerate(mols_list):
        # smiles to mol2 
        SMILES_ERROR_FLAG=False
        with open('tmp/ligand.mol2', 'w') as f:
            try:
                mol = pybel.readstring("smi", smi)
                mol.addh()
                mol.make3D()
                
                txt = mol.write('mol2')
                f.write(txt)
                f.close()
                
            except:
                SMILES_ERROR_FLAG=True
                mean_sc=0.0
                delta_t=0.0
        
        if(not SMILES_ERROR_FLAG):
            # ligand mol2 to pdbqt 
            subprocess.run([f'{install_dir}/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_ligand4.py',
                            f'-l tmp/ligand.mol2', '-o tmp/ligand.pdbqt', '-A hydrogens'])
            
            # RUN DOCKING 
            start=time()
            subprocess.run([f'{install_dir}/autodock_vina_1_1_2_linux_x86/bin/vina',
                        '--config', f'{home_dir}/vina_docking/data/conf/conf_{args.target}.txt','--exhaustiveness', f'{args.ex}', 
                        '--log', 'tmp/log.txt'])
            end = time()
            delta_t=end-start
            print("Docking time :", delta_t)
            
            if(delta_t>1): # Condition to check the molecule was docked 
                #reading output tmp/ligand_out.pdbqt
                with open('tmp/ligand_out.pdbqt','r') as f :
                    lines = f.readlines()
                    slines = [l for l in lines if l.startswith('REMARK VINA RESULT')]
                    #print(f'{len(slines)} poses found' )
                    values = [l.split() for l in slines]
                    # In each split string, item with index 3 should be the kcal/mol energy. 
                    mean_sc=np.mean([float(v[3]) for v in values]) 
            else:
                mean_sc=0.0
                
                            
        # Add to dataframe 
        mols_df.at[i,'score']=mean_sc
        mols_df.at[i,'time']=delta_t
        
        if(i%100==0): # checkpoint , save dataframe 
            mols_df.to_csv(args.out_dataframe_path)
            
    #final save 
    print('Docking finished, saving to csv')        
    mols_df.to_csv(args.out_dataframe_path)
    
if(__name__=='__main__'):
    cline()