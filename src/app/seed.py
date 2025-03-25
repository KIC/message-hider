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


def generate_secure_random_lat_long():
    """
    Generates a random valid latitude and longitude combination using a
    cryptographically secure random generator.

    :return: A tuple containing latitude and longitude.
    """
    # Latitude ranges from -90 to 90
    latitude = -90 + (
        secrets.randbelow(180_000_001) / 1_000_000
    )  # Secure float between -90 and 90

    # Longitude ranges from -180 to 180
    longitude = -180 + (
        secrets.randbelow(360_000_001) / 1_000_000
    )  # Secure float between -180 and 180

    return f"{latitude:.5f}, {longitude:.5f}"
