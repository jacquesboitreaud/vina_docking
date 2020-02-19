#!/bin/bash
#SBATCH --account=def-jeromew
#SBATCH --array 1-10
#SBATCH --time=24:00:00
#SBATCH --job-name=v_screen
#SBATCH --output=%x_$SLURM_ARRAY_TASK_ID.out
python3 dock_smi.py -t drd3 -df data/split/mol_batch_$SLURM_ARRAY_TASK_ID.csv -o data/scored/scored_$SLURM_ARRAY_TASK_ID.csv
