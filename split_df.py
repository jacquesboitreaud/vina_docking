# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:16:21 2020

@author: jacqu


Split dataframe into chunks for parallel docking using sbatch 
"""

import pandas as pd 
import numpy as np
import os 
import argparse

def splitDataFrame(df, chunkSize): 
    listOfDf = list()
    numberChunks = len(df) // chunkSize
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf

def cline():
    # Parses arguments and calls main function with these args
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-df", "--dataframe", default='data/ligands/abl1_dude.csv', help="pd dataframe file to split")
    parser.add_argument("-n", "--num_chunks",default=3, help="Number of chunks to split in ")
    args = parser.parse_args()
    
    main(args)
    
def main(args):
    
    df = pd.read_csv(args.dataframe)
    print('Dataframe loaded. Chunks will be saved in data/ligands')
    
    chunkSize = df.shape[0]//(args.num_chunks)
    
    chunks = splitDataFrame(df,chunkSize)
    
    for i,c in enumerate(chunks):
        chunks[i].to_csv(f'data/ligands/split_batch_{i+1}.csv')
        
    print(f'Saved {args.num_chunks} chunks of {chunkSize} mols to data/ligands/')
    
    
if(__name__=='__main__'):
    cline()