# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 19:19:42 2020

@author: jacqu

Script to split a big file with several mol2s into multiple small mol2 files (1 molecule per file) 

"""

import sys
import subprocess
import argparse

from split import *

    
def cline():
    # Parses arguments and calls main function with these args
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-m", "--mol2", default='data/decoys.mol2', help="mol2 file to split")
    parser.add_argument("-d", "--out_dir", default='data/decoys_split', help="directory to write mol2s")
    parser.add_argument("-n", "--num_chunks",default=-1, help="Number of chunks to split the big mol2 ")
    args = parser.parse_args()
    
    main(args)
    
def main(args):
    # Run the docking process with the args provided
    
    # Run the splitting of mol2 file 
    if(args.num_chunks==-1):
        write_multimol2(multimol2=args.mol2, out_dir=args.out_dir)
        print(f'Split {args.mol2} and wrote single molecule files to {args.out_dir}')
    else: 
        chunk_size = int(len(split_multimol2(args.mol2))/args.num_chunks)
        write_multimol2_chunks(multimol2=args.mol2, chunk_size=chunk_size, out_dir=args.out_dir)
        print(f'Split {args.mol2} and wrote chunk files to {args.out_dir}')
    
    
if(__name__=='__main__'):
    cline()