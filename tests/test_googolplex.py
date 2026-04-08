"""Tests for the googolplex module."""

import pytest

from math_experiments.googolplex import build_power_of_ten, power_of_ten_size_bytes


class TestBuildPowerOfTen:
    def test_zero(self) -> None:
        assert build_power_of_ten(0) == 1

    def test_one(self) -> None:
        assert build_power_of_ten(1) == 10

    def test_three(self) -> None:
        assert build_power_of_ten(3) == 1000

    def test_googol(self) -> None:
        result = build_power_of_ten(100)
        assert result == 10**100
        assert len(str(result)) == 101

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            build_power_of_ten(-1)


class TestPowerOfTenSizeBytes:
    def test_returns_positive(self) -> None:
        assert power_of_ten_size_bytes(100) > 0

    def test_larger_exponent_larger_size(self) -> None:
        assert power_of_ten_size_bytes(1000) > power_of_ten_size_bytes(100)
