#!/usr/bin/bash
#SBATCH --nodes 1
#SBATCH --job-name Trapezoid_James
#SBATCH --output results.txt
for i in {20..60}
do
   python trapezoid.py -a 1 -b 4 -n "$i"
done
