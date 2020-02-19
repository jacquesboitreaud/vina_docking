#!/bin/bash
#SBATCH --account=def-jeromew
#SBATCH --time=00:01:00
#SBATCH --job-name=virtual_screen
#SBATCH --output=out/%x.out
python3 dock_df.py -t drd3 -df data/split/mol_batch_1.csv -o data/scored/scored_1.csv
