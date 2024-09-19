#!/usr/bin/python3
import argparse

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
    parser.add_argument(
        '-p', type=int, required=True,
        help="Number of OpenMPI workers to start [int > 0]"
    )
    return parser.parse_args()

