#!/usr/bin/python3
import argparse

"""
Module for calculating the integral of a function using the trapezoid rule.
"""

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

def trapezoid_rule(func, lower_bound, upper_bound, num_steps):
    """
    Approximate the integral of function `func` from `lower_bound` to `upper_bound` 
    using the trapezoid rule with `num_steps` steps.

    :param func: Function to integrate.
    :param lower_bound: Lower bound of integration.
    :param upper_bound: Upper bound of integration.
    :param num_steps: Number of steps.
    :return: Approximate integral value.
    """
    if num_steps <= 0:
        raise ValueError("Number of steps must be greater than 0.")
    step_size = (upper_bound - lower_bound) / num_steps
    integral = (func(lower_bound) + func(upper_bound)) / 2
    for i in range(1, num_steps):
        x = lower_bound + i * step_size
        integral += func(x)
    integral *= step_size
    return integral

def main(args):
    """
    Main function to parse arguments, compute the integral, and display the result.
    """
    def function_to_integrate(x):
        """
        Function to be integrated: x squared.

        :param x: Input value.
        :return: x squared.
        """
        return x ** 2

    integral_value = trapezoid_rule(
        function_to_integrate,
        args.a,
        args.b,
        args.n
    )

    # Example with known result (integration of x^2 from 1 to 4)
    expected_value = 21
    error = abs(integral_value - expected_value)

    print(f"Calculated integral: {integral_value}")
    print(f"Expected value: {expected_value}")
    print(f"Error: {error}")

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
