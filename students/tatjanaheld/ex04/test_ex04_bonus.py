# Tests for the bonus (see BONUS.md). If you copied the ex04 folder before this file
# existed, copy just this file into your students/<login>/ex04 folder.
#
# They are skipped until your ex04.py has a function `run_bonus`, so they don't turn CI red
# if you don't do the bonus.

import pytest

import ex04

pytestmark = pytest.mark.skipif(
    not hasattr(ex04, "run_bonus"), reason="bonus not attempted: ex04.py has no run_bonus"
)

# Reads n and outputs n!, computed recursively (see BONUS.md).
# fmt: off
FACTORIAL = [
    3, 50, 109, 51, 21101, 15, 0, 0, 21001, 50, 0, 1, 1105, 1, 18, 204, 2, 99, 1205, 1, 28,
    21101, 1, 0, 2, 2105, 1, 0, 21101, 41, 0, 3, 21201, 1, -1, 4, 109, 3, 1105, 1, 18, 109, -3,
    22202, 1, 5, 2, 2105, 1, 0, 0,
]
# fmt: on


def test_relative_mode_read():
    assert ex04.run_bonus([109, 5, 204, 2, 99, 0, 0, 42], []) == [42]


def test_relative_base_adds_up():
    assert ex04.run_bonus([109, 20, 109, -15, 204, 2, 99, 77], []) == [77]


def test_opcode_9_in_position_mode():
    assert ex04.run_bonus([9, 6, 204, 1, 99, 0, 5], []) == [5]


def test_relative_mode_jump():
    assert ex04.run_bonus([109, 2, 1205, 1, 7, 99, 99, 104, 42, 99], []) == [42]


def test_read_beyond_the_program():
    assert ex04.run_bonus([4, 1000, 99], []) == [0]


def test_write_beyond_the_program():
    assert ex04.run_bonus([1101, 2, 3, 500, 4, 500, 99], []) == [5]


def test_relative_mode_write():
    assert ex04.run_bonus([109, 3, 21101, 4, 5, 10, 204, 10, 99], []) == [9]
    assert ex04.run_bonus([109, 10, 203, 0, 204, 0, 99], [7]) == [7]


def test_factorial():
    assert ex04.run_bonus(FACTORIAL.copy(), [0]) == [1]
    assert ex04.run_bonus(FACTORIAL.copy(), [5]) == [120]
    assert ex04.run_bonus(FACTORIAL.copy(), [20]) == [2432902008176640000]
