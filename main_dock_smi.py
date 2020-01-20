# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:19:35 2020

@author: jacqu

File to run vina docking on a dataframe with smiles strings
    
    Directory with individual mol2 files 
    Path to receptor PDB file 
    exhaustiveness 
    Suffix for scores file output 

"""

import sys
import subprocess
import os 
import argparse
from time import time
import numpy as np

import openbabel
import pybel 
import pandas as pd
  
def cline():
    # Parses arguments and calls main function with these args
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-df", "--dataframe", default='data/to_dock.csv', help="csv file with 'can' columns containing smiles")
    parser.add_argument("-r", "--receptor_file", default='data/receptors/receptor.pdb', help="path to receptor pdb")
    parser.add_argument("-e", "--ex", default=4, help="exhaustiveness parameter for vina")
    parser.add_argument("-o", "--output_suffix", default='', help="Suffix for output scores files")
    args = parser.parse_args()
    
    main(args)
    
def main(args):
    # Runs the docking process with the args provided
    
    # target to pdbqt 
    subprocess.run(['python3','pdb_select.py',f'{args.receptor_file}','! hydro', f'{args.receptor_file}'])
    subprocess.run(['/home/mcb/users/jboitr/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_receptor4.py',
                    f'-r /home/mcb/users/jboitr/vina_docking/{args.receptor_file}','-o tmp/receptor.pdbqt', '-A hydrogens'])
    
    # Iterate on molecules
    mols_df = pd.read_csv(args.dataframe)
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
        subprocess.run(['/home/mcb/users/jboitr/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_ligand4.py',
                        f'-l tmp/ligand.mol2', '-o tmp/ligand.pdbqt', '-A hydrogens'])
        
        # RUN DOCKING 
        start=time()
        subprocess.run(['/home/mcb/users/jboitr/local/autodock_vina_1_1_2_linux_x86/bin/vina',
                        '--config', '/home/mcb/users/jboitr/vina_docking/data/conf.txt','--exhaustiveness', f'{args.ex}', 
                        '--log', 'tmp/log.txt'])
        end = time()
        print("Docking time :", end-start)
        
        #reading output tmp/ligand_out.pdbqt
        with open('tmp/ligand_out.pdbqt','r') as f :
            lines = f.readlines()
            sline = lines[1]
            values = sline.split()
            sc=float(values[3])
            
        # Add to dataframe 
        mols_df.loc[i,'score']=sc
        mols_df.loc[i,'time']=end-start
        
        if(i%100==0): # checkpoint , save dataframe 
            mols_df.to_csv(args.dataframe[:-4]+'_scored.csv')
            
    #final save 
    print('Docking finished, saving to csv')        
    mols_df.to_csv(args.dataframe[:-4]+'_scored.csv')
    
if(__name__=='__main__'):
    cline()