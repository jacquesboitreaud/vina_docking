# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:19:35 2020

@author: jacqu

File to run vina docking on all mol2s in a directory 

TODO : trouver comment on run une commande avec subprocess 
"""

import sys
import subprocess
import os 
import argparse



  
def cline():
    # Parses arguments and calls main function with these args
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d", "--mols_dir", default='data/split', help="directory with mol2 files")
    parser.add_argument("-r", "--receptor_file", default='receptor.pdb', help="path to receptor pdb")
    parser.add_argument("-e", "--ex", default=8, help="exhaustiveness parameter for vina")
    args = parser.parse_args()
    
    main(args)
    
def main(args):
    # Run the docking process with the args provided
    
    #TODO : prepare PDB with pdbselect script (Guillaume)
    
    # target to pdbqt 
    subprocess.run(['python3','pdb_select.py',f'data/{args.receptor_file}', f'data/{args.receptor_file}'])
    subprocess.run(['/home/mcb/users/jboitr/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_receptor4.py', f'-r /home/mcb/users/jboitr/vina_docking/data/{args.receptor_file} -A hydrogens'])
    
    # Iterate on molecules
    mols_list = os.listdir(args.mols_dir)
    mols_list=mols_list[:10]
    for file in mols_list:
        # ligand to pdbqt 
        subprocess.run(['/home/mcb/users/jboitr/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_ligand4.py', f'-l /home/mcb/users/jboitr/vina_docking/data/split/{file} -A hydrogens'])
        
    # RUN DOCKING 
    subprocess.run(['/home/mcb/users/jboitr/local/autodock_vina_1_1_2_linux_x86/bin/vina','--config', '/home/mcb/users/jboitr/vina_docking/data/conf.txt','--exhaustiveness', f'{args.ex}'])
    
    
if(__name__=='__main__'):
    cline()