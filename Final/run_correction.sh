#!/usr/bin/bash
#SBATCH --nodes 5
#SBATCH --job-name James_correction_assignment
#SBATCH --output results.correction.txt

mpiexec -n 5 /homes/jgray/miniconda3/envs/bioinfspark/bin/python correct_records.py