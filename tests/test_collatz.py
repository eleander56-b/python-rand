"""Tests for the Collatz module."""

import pytest

from math_experiments.collatz import collatz_steps, random_collatz_trials


class TestCollatzSteps:
    def test_one_returns_zero(self) -> None:
        assert collatz_steps(1) == 0

    def test_two_returns_one(self) -> None:
        assert collatz_steps(2) == 1

    def test_known_sequence_three(self) -> None:
        # 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1 = 7 steps
        assert collatz_steps(3) == 7

    def test_known_sequence_six(self) -> None:
        # 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1 = 8 steps
        assert collatz_steps(6) == 8

    def test_known_sequence_27(self) -> None:
        # 27 is famously long: 111 steps
        assert collatz_steps(27) == 111

    def test_powers_of_two(self) -> None:
        # 2^k takes exactly k steps
        for k in range(1, 20):
            assert collatz_steps(2**k) == k

    def test_large_number(self) -> None:
        result = collatz_steps(1_000_000)
        assert isinstance(result, int)
        assert result > 0

    def test_always_integer_division(self) -> None:
        # Ensure no float contamination for large numbers
        result = collatz_steps(2**64 + 1)
        assert isinstance(result, int)

    def test_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="positive integer"):
            collatz_steps(0)

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="positive integer"):
            collatz_steps(-5)


class TestRandomCollatzTrials:
    def test_finite_trials(self) -> None:
        results = list(random_collatz_trials(upper_bound=1000, max_trials=10))
        assert len(results) == 10
        for num, steps in results:
            assert 1 <= num < 1000
            assert steps >= 0

    def test_zero_trials(self) -> None:
        results = list(random_collatz_trials(max_trials=0))
        assert results == []

    def test_all_reach_one(self) -> None:
        # Every trial should have completed (steps >= 0 means it reached 1)
        for _num, steps in random_collatz_trials(upper_bound=10000, max_trials=50):
            assert steps >= 0
