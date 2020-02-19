#!/bin/bash
#SBATCH --account=def-jeromew
#SBATCH --array 1-10
#SBATCH --time=72:00:00
#SBATCH --job-name=virtual_screen
#SBATCH --output=out/%x_${SLURM_ARRAY_JOB_ID}.out
echo "Starting task $SLURM_ARRAY_TASK_ID"
python3 dock_df.py -t drd3 -df data/split/split_batch_${SLURM_ARRAY_TASK_ID}.csv -o data/scored/scored_${SLURM_ARRAY_TASK_ID}.csv -s cedar
