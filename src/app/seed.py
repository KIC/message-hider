import secrets
import sys


def generate_secure_random_integer(lower: int = 10000, upper: int = sys.maxsize) -> int:
    """
    Generates a cryptographically secure random integer within a given range [lower, upper].

    :param lower: The minimum value of the range (inclusive).
    :param upper: The maximum value of the range (inclusive).
    :return: A secure random integer.
    """
    if lower > upper:
        raise ValueError("Lower bound must be less than or equal to the upper bound.")

    return secrets.randbelow(upper - lower + 1) + lower


def generate_secure_random_float(lower: float = 14, upper: float = 100000) -> float:
    """
    Generates a cryptographically secure random float within a given range [lower, upper].

    :param lower: The minimum value of the range (inclusive).
    :param upper: The maximum value of the range (inclusive).
    :return: A secure random float.
    """
    if lower > upper:
        raise ValueError("Lower bound must be less than or equal to the upper bound.")

    # Generate a secure random float in the range [0, 1)
    random_fraction = secrets.randbelow(10**8) / 10**8  # High precision random fraction

    # Scale and shift to the desired range
    return lower + (upper - lower) * random_fraction
