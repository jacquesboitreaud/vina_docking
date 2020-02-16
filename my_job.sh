#!/bin/bash
#SBATCH --account=def-jeromew
#SBATCH --time=00:15:00
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=256M
#SBATCH --job-name=test
#SBATCH --output=%x.out
echo 'start testing vina on drd3'
python3 main_dock_smi.py -t drd3 -df drd3_dude
