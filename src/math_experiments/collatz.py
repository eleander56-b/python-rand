"""Collatz conjecture (3x+1 problem) explorer.

Generates random starting numbers and counts how many steps each takes
to reach 1 under the Collatz sequence. Optionally sends email alerts
when a number requires an unusually high number of steps.
"""

from __future__ import annotations

import argparse
import logging
import random
import re
import subprocess
import sys
import time
from collections.abc import Iterator

from math_experiments.notifications import send_alert

logger = logging.getLogger(__name__)

DEFAULT_UPPER_BOUND: int = 10**150
STEP_THRESHOLD: int = 5000
STATS_INTERVAL: int = 10_000
TEMP_LIMIT_CELSIUS: int = 70
COOLDOWN_SECONDS: int = 30


def collatz_steps(n: int) -> int:
    """Return the number of steps for n to reach 1 under the Collatz sequence.

    The Collatz sequence: if n is even, divide by 2; if odd, multiply
    by 3 and add 1. Repeat until reaching 1.

    Args:
        n: A positive integer starting value.

    Returns:
        The number of steps to reach 1.

    Raises:
        ValueError: If n is not a positive integer.
    """
    if n < 1:
        raise ValueError(f"n must be a positive integer, got {n}")
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def random_collatz_trials(
    upper_bound: int = DEFAULT_UPPER_BOUND,
    max_trials: int | None = None,
) -> Iterator[tuple[int, int]]:
    """Yield (starting_number, step_count) for random Collatz trials.

    Args:
        upper_bound: Exclusive upper bound for random starting numbers.
        max_trials: Stop after this many trials, or None for infinite.

    Yields:
        Tuples of (starting_number, steps_to_reach_1).
    """
    trial = 0
    while max_trials is None or trial < max_trials:
        num = random.randrange(1, upper_bound)
        steps = collatz_steps(num)
        yield num, steps
        trial += 1


def get_cpu_temp_linux() -> float | None:
    """Read CPU temperature via lm-sensors on Linux.

    Returns:
        Temperature in Celsius, or None if unavailable.
    """
    if sys.platform != "linux":
        return None
    try:
        result = subprocess.run(
            ["sensors"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        logger.warning("lm-sensors not available")
        return None

    for line in result.stdout.splitlines():
        if "\u00b0C" in line:
            match = re.search(r"[+-]?(\d+\.?\d*)\s*\u00b0C", line)
            if match:
                return float(match.group(1))
    return None


def main() -> None:
    """Run Collatz trials with optional email alerts and temp monitoring."""
    parser = argparse.ArgumentParser(description="Collatz conjecture explorer")
    parser.add_argument(
        "--upper-bound",
        type=int,
        default=DEFAULT_UPPER_BOUND,
        help="Upper bound for random starting numbers",
    )
    parser.add_argument(
        "--max-trials",
        type=int,
        default=None,
        help="Maximum number of trials (default: unlimited)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=STEP_THRESHOLD,
        help="Step count threshold for email alerts (default: 5000)",
    )
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="Disable email notifications",
    )
    args = parser.parse_args()

    total_steps = 0
    for trial_num, (num, steps) in enumerate(
        random_collatz_trials(args.upper_bound, args.max_trials), start=1
    ):
        total_steps += steps
        print(f"{steps} steps for: {num}")

        if steps >= args.threshold and not args.no_email:
            try:
                send_alert(
                    subject=f"Collatz: {num} took {steps} steps",
                    body=f"The number {num} required {steps} steps to reach 1.",
                )
            except Exception:
                logger.exception("Failed to send alert")

        if trial_num % STATS_INTERVAL == 0:
            avg = total_steps / trial_num
            print(f"After {trial_num} trials: average {avg:.1f} steps")

            temp = get_cpu_temp_linux()
            if temp is not None:
                print(f"CPU: {temp}\u00b0C")
                if temp > TEMP_LIMIT_CELSIUS:
                    print(f"Cooling down for {COOLDOWN_SECONDS}s...")
                    time.sleep(COOLDOWN_SECONDS)


if __name__ == "__main__":
    main()
