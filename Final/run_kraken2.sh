#!/usr/bin/bash
#SBATCH --nodes 5
#SBATCH --job-name James_kraken_assignment
#SBATCH --output results.txt

mpiexec -n 5 /homes/jgray/miniconda3/envs/bioinfspark/bin/python run_kraken.py