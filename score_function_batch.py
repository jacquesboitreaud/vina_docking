# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:19:35 2020

@author: jacqu

Function to run vina docking on a batch of smiles (active learning iter)

"""

import sys
import subprocess
import os 
import shutil
from time import time
import numpy as np

import openbabel
import pybel 
    
def dock_batch(smiles, repo_path ='/home/mcb/users/jboitr/vina_docking', 
               install_dir='/home/mcb/users/jboitr/local'):
    # Args: 
    #'smiles' : a list of smiles strings 
    # install_dir : Dir with vina/mgltools installs
    # repo_path : Path to 'vina_docking' repo from root. Used so that we use no relative path at all,
    # to avoid confusion. 
    
    target = 'drd3'
    exhaustiveness = 32
    
    # Uncomment to Copy receptor file from the DUDE dir if first time using this target. 
    #shutil.copyfile(f'/home/mcb/users/jboitr/data/all/{args.target}/receptor.pdb',f'data/receptors/{args.target}.pdb')
    
    receptor_filepath = f'{repo_path}/data/receptors/{target}.pdb' # path to receptor pdb file
    
    working_dir = os.getcwd()
    os.chdir(repo_path)
    
    # target to pdbqt 
    subprocess.run(['python3',f'{repo_path}/pdb_select.py',f'{receptor_filepath}','! hydro', f'{receptor_filepath}'])
    subprocess.run([f'{install_dir}/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', f'{repo_path}/prepare_receptor4.py',
                    f'-r {receptor_filepath}',f'-o {repo_path}/tmp/receptor.pdbqt', '-A hydrogens'])
    
    # Iterate on molecules
    mols_list = smiles
    scores_list = []
    times_list = []
    print(f'Docking {len(mols_list)} molecules')

    ok_counter = 0
    for i,smi in enumerate(mols_list):
        # smiles to mol2 
        SMILES_ERROR_FLAG=False
        with open(f'{repo_path}/tmp/ligand.mol2', 'w') as f:
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
            subprocess.run([f'{install_dir}/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', f'{repo_path}/prepare_ligand4.py',
                            f'-l {repo_path}/tmp/ligand.mol2', f'-o {repo_path}/tmp/ligand.pdbqt', '-A hydrogens'])
            
            # RUN DOCKING 
            start=time()
            subprocess.run([f'{install_dir}/autodock_vina_1_1_2_linux_x86/bin/vina',
                        '--config', f'{repo_path}/data/conf/conf_{target}.txt','--exhaustiveness', f'{exhaustiveness}', 
                        '--log', f'{repo_path}/tmp/log.txt'])
            end = time()
            delta_t=end-start
            print("Docking time :", delta_t)
            
            if(delta_t>1): # Condition to check the molecule was docked 
                #reading output tmp/ligand_out.pdbqt
                with open(f'{repo_path}/tmp/ligand_out.pdbqt','r') as f :
                    lines = f.readlines()
                    slines = [l for l in lines if l.startswith('REMARK VINA RESULT')]
                    #print(f'{len(slines)} poses found' )
                    values = [l.split() for l in slines]
                    # In each split string, item with index 3 should be the kcal/mol energy. 
                    mean_sc=np.mean([float(v[3]) for v in values]) 
                    ok_counter += 1
            else:
                mean_sc=0.0
                
        print(f'>>> Docking finished. {ok_counter}/{len(mols_list)} smiles were successfully docked')
        # Add to dataframe 
        scores_list.append(mean_sc)
        times_list.append(delta_t)
        
        os.chdir(working_dir) # set back to working directory 

    return scores_list, times_list