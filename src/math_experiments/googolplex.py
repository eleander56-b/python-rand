"""Googolplex demonstration.

A googolplex is 10^(10^100). This module provides utilities for working
with large powers of 10 and demonstrates the scale of a googolplex.
"""

from __future__ import annotations

import argparse
import sys
import time

GOOGOL: int = 10**100


def build_power_of_ten(exponent: int) -> int:
    """Compute 10^exponent as a Python integer.

    Uses Python's built-in binary exponentiation (O(log n)),
    far more efficient than string concatenation in a loop.

    Args:
        exponent: The power to raise 10 to. Must be non-negative.

    Returns:
        10 ** exponent as an integer.

    Raises:
        ValueError: If exponent is negative.
    """
    if exponent < 0:
        raise ValueError(f"exponent must be non-negative, got {exponent}")
    result: int = 10**exponent
    return result


def power_of_ten_size_bytes(exponent: int) -> int:
    """Return the memory size in bytes of 10^exponent as a Python int.

    Args:
        exponent: The power of 10. Must be non-negative.

    Returns:
        Size in bytes as reported by sys.getsizeof.
    """
    return sys.getsizeof(build_power_of_ten(exponent))


def main() -> None:
    """Demonstrate large powers of 10 and explain googolplex scale."""
    parser = argparse.ArgumentParser(description="Explore large powers of 10")
    parser.add_argument(
        "--exponent",
        type=int,
        default=1000,
        help="Power of 10 to compute (default: 1000, i.e. 10^1000)",
    )
    args = parser.parse_args()

    print(f"Computing 10^{args.exponent}...")
    start = time.perf_counter()
    result = build_power_of_ten(args.exponent)
    elapsed = round(time.perf_counter() - start, 4)

    size_bytes = sys.getsizeof(result)
    print(f"Computed in {elapsed}s")
    print(f"Number of digits: {len(str(result))}")
    print(f"Memory usage: {size_bytes:,} bytes ({size_bytes / 1024:.2f} KB)")

    print("\nA googol is 10^100 = a number with 101 digits")
    print("A googolplex is 10^(10^100) = a number with 10^100 + 1 digits")
    print("Storing that many digits would require ~10^91 PETABYTES")


if __name__ == "__main__":
    main()
