# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:15:06 2020

@author: jacqu

Writes conf files for different targets 
"""
import os

targets = os.listdir('C:/Users/jacqu/Documents/mol2_resource/dude/all')

n_modes=3 # Number of binding modes to return in output file 

volumes = []

for t in targets : 
    
    with open(f'C:/Users/jacqu/Documents/mol2_resource/dude/box/{t}.txt', 'r') as f:
        lines = f.readlines()
        center = lines[1].split()
        print(center)
        cx, cy, cz = center[-3:]
        dims = lines[2].split()
        print(dims)
        hx, hy, hz = dims[-3:]
        volumes.append(float(hx)*float(hy)*float(hz))
        
    print(f'Writing conf file for target {t}')
    with open(f'C:/Users/jacqu/Documents/GitHub/vina_docking/data/conf/conf_{t}.txt', 'w') as f:
        f.write('receptor = tmp/receptor.pdbqt\n')
        f.write('ligand = tmp/ligand.pdbqt\n')
        
        f.write('\n')
        f.write(f'center_x = {cx}\n')
        f.write(f'center_y = {cy}\n')
        f.write(f'center_z = {cz}\n')
        
        f.write('\n')
        f.write(f'size_x = {hx}\n')
        f.write(f'size_y = {hy}\n')
        f.write(f'size_z = {hz}\n')
        
        f.write('\n')
        f.write(f'num_modes = {n_modes}\n')