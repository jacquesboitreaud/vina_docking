# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:15:06 2020

@author: jacqu

Download box files from DUDE docking dir. 
"""

import urllib3
import os 

targets = os.listdir('C:/Users/jacqu/Documents/mol2_resource/dude/all')

for t in targets : 
    
    url = f'http://dude.docking.org/targets/{t}/docking/grids/box'
    
    # get the url 
    
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    print(r.data)
 
    with open(f'C:/Users/jacqu/Documents/mol2_resource/dude/box/{t}.txt', 'wb') as f:
        f.write(r.data)