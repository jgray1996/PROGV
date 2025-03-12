#!/usr/bin/bash
#SBATCH --nodes 1
#SBATCH --job-name James_time_assignment
time /homes/jgray/miniconda3/envs/progiv/bin/python -m cProfile -s time ~/Documents/Master/Periode\ 5/PROGV/Assignment\ 5/main.py > logs.txt
