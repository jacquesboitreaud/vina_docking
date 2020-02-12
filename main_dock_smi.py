# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:19:35 2020

@author: jacqu

File to run vina docking on a dataframe with smiles strings
    
    Directory with individual mol2 files 
    Path to receptor PDB file 
    exhaustiveness 
    Suffix for scores file output 
    
(Paths for compute canada server) 

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
    parser.add_argument("-df", "--dataframe", default='to_dock', help="csv file with 'can' columns containing smiles. Should be in ./data.ligands")
    parser.add_argument("-e", "--ex", default=8, help="exhaustiveness parameter for vina. Default to 8")
    args = parser.parse_args()
    
    main(args)
    
def main(args):
    # Runs the docking process with the args provided
    
    home_dir='/home/jboitr/projects/def-jeromew/jboitr'
    
    # Uncomment to Copy receptor file from the DUDE dir if first time using this target. 
    #shutil.copyfile(f'/home/mcb/users/jboitr/data/all/{args.target}/receptor.pdb',f'data/receptors/{args.target}.pdb')
    
    receptor_filepath = f'data/receptors/{args.target}.pdb'
    
    # target to pdbqt 
    subprocess.run(['python3','pdb_select.py',f'{receptor_filepath}','! hydro', f'{receptor_filepath}'])
    subprocess.run([f'{home_dir}/local/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_receptor4.py',
                    f'-r {home_dir}/vina_docking/{receptor_filepath}','-o tmp/receptor.pdbqt', '-A hydrogens'])
    
    # Iterate on molecules
    mols_df = pd.read_csv(f'data/ligands/{args.dataframe}.csv')
    mols_df['score'], mols_df['time'] = 0, 0
    mols_list = mols_df['can']
    print(f'Docking {len(mols_list)} molecules')
    
    for i,smi in enumerate(mols_list):
        # smiles to mol2 
        with open('tmp/ligand.mol2', 'w') as f:
            mol = pybel.readstring("smi", smi)
            mol.addh()
            mol.make3D()
            
            txt = mol.write('mol2')
            f.write(txt)
            f.close()
        
        # ligand mol2 to pdbqt 
        subprocess.run([f'{home_dir}/local/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_ligand4.py',
                        f'-l tmp/ligand.mol2', '-o tmp/ligand.pdbqt', '-A hydrogens'])
        
        # RUN DOCKING 
        start=time()
        subprocess.run([f'{home_dir}/local/autodock_vina_1_1_2_linux_x86/bin/vina',
                    '--config', f'{home_dir}/vina_docking/data/conf/conf_{args.target}.txt','--exhaustiveness', f'{args.ex}', 
                    '--log', 'tmp/log.txt'])
        end = time()
        print("Docking time :", end-start)
        
        #reading output tmp/ligand_out.pdbqt
        with open('tmp/ligand_out.pdbqt','r') as f :
            lines = f.readlines()
            slines = [l for l in lines if l.startswith('REMARK VINA RESULT')]
            #print(f'{len(slines)} poses found' )
            values = [l.split() for l in slines]
            # In each split string, item with index 3 should be the kcal/mol energy. 
            mean_sc=np.mean([float(v[3]) for v in values]) 
            
        # Add to dataframe 
        mols_df.loc[i,'score']=mean_sc
        mols_df.loc[i,'time']=end-start
        
        if(i%100==0): # checkpoint , save dataframe 
            mols_df.to_csv(f'data/scored/{args.dataframe}_scored.csv')
            
    #final save 
    print('Docking finished, saving to csv')        
    mols_df.to_csv(f'data/scored/{args.dataframe}_scored.csv')
    
if(__name__=='__main__'):
    cline()