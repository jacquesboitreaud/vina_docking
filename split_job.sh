#!/bin/bash
#SBATCH --account=def-jeromew
#SBATCH --time=00:01:00
#SBATCH --job-name=split
#SBATCH --output=%x.out
python3 split_df.py -df data/docking1.csv -n 10
