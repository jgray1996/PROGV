#!/usr/bin/bash
#SBATCH --nodes 1
#SBATCH --job-name James_mpi_assignment
#SBATCH --output results.csv
start=1
stop=32

for num_processes in $(seq $start $stop);
do
    time mpiexec -np $num_processes /homes/jgray/miniconda3/envs/prog5/bin/python Assignment\ 2/assignment2.py -a -3 -b 3 -n 40
done
