#!/usr/bin/bash
#SBATCH --nodes 1
#SBATCH --job-name James_sql_assignment
time /homes/jgray/miniconda3/envs/progiv/bin/python -m cProfile -s time ~/Documents/Master/Periode\ 5/PROGV/Assignment\ 3/main.py > logs.txt
