#!/usr/bin/python3
import argparse
from mpi4py import MPI
import trapezoid
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def parse_arguments():
    """
    Parse command-line arguments for integration bounds and number of steps.
    """
    parser = argparse.ArgumentParser(
        description="Calculate the integral of a function using the trapezoid rule."
    )
    parser.add_argument(
        '-a', type=int, required=True,
        help="Lower integration bound [int]"
    )
    parser.add_argument(
        '-b', type=int, required=True,
        help="Upper integration bound [int]"
    )
    parser.add_argument(
        '-n', type=int, required=True,
        help="Number of steps for integration [int > 0]"
    )
    return parser.parse_args()


args = parse_arguments()

lower_boundry = args.a
upper_boundry = args.b

if rank == 0:

    intervals = np.linspace(lower_boundry, upper_boundry,
                                                size+1)
    boundries = [[intervals[i], intervals[i+1]] 
                for i in range(len(intervals)-1)]
    
    comm.scatter(boundries)
    results = comm.gather(None, root=0)
    print(f"Results: {results}")
else:
    data = comm.scatter([],root=0)
    print(data)
    I = trapezoid.trapezoid_rule(func=trapezoid.function_to_integrate,
                       lower_bound=lower_boundry,
                       upper_bound=upper_boundry,
                       num_steps=30)
    I = data
    comm.gather(I, root=0)
