#!/bin/bash
#SBATCH --account=def-jeromew
#SBATCH --array 1-10
#SBATCH --time=24:00:00
#SBATCH --job-name=v_screen
#SBATCH --output=%x_$SLURM_ARRAY_TASK_ID.out
echo 'start testing vina on drd3'
python3 main_dock_smi.py -t drd3 -df mol_batch_$SLURM_ARRAY_TASK_ID
