from ex01 import (
    backwards,
    celsius_to_fahrenheit,
    common_elements,
    count_letter,
    first_three,
    floor,
    floor_after,
    last_four,
    mirrored,
    quotient_and_remainder,
    science_to_analytics,
)

# ---------------------------------------------------------------- Part 1


def test_quotient_and_remainder():
    assert quotient_and_remainder(17, 5) == (3, 2)
    try:
        quotient_and_remainder(0.1, 0.01)
    except TypeError:
        pass
    try:
        quotient_and_remainder("test", "t")
    except TypeError:
        pass


def test_quotient_and_remainder_no_remainder():
    assert quotient_and_remainder(10, 5) == (2, 0)


def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(100) == 212
    assert celsius_to_fahrenheit(0) == 32
    try:
        celsius_to_fahrenheit("test")
    except TypeError:
        pass
    try:
        celsius_to_fahrenheit(False)
    except TypeError:
        pass


def test_celsius_to_fahrenheit_same_value():
    # -40 °C is -40 °F
    assert celsius_to_fahrenheit(-40) == -40


def test_first_three():
    assert first_three("Python") == "Pyt"
    try:
        first_three(2)
    except TypeError:
        pass
    try:
        first_three(2)
    except TypeError:
        pass


def test_last_four():
    assert last_four("Python") == "thon"
    try:
        last_four(5)
    except TypeError:
        pass
    try:
        last_four()
    except TypeError:
        pass


def test_backwards():
    assert backwards("Python") == "nohtyP"
    try:
        backwards(5.6)
    except TypeError:
        pass


def test_science_to_analytics():
    assert science_to_analytics("DataScience") == "DataAnalytics"


def test_floor():
    assert floor("(((") == 3
    assert floor("(()") == 1


def test_floor_below_zero():
    assert floor("())))") == -3


def test_floor_up_and_down():
    assert floor("()()") == 0


# ---------------------------------------------------------------- Part 2
# Add at least two tests of your own below, for the Part 2 functions.


def test_floor_after():
    assert floor_after("((())", 3) == 3
    try:
        floor_after("((())", -2)
    except ValueError:
        pass


def test_mirrored():
    assert mirrored("(()") == "))("


def test_common_elements():
    assert common_elements(["a", "b", "c"], ["b", "c", "d"]) == {"b", "c"}


def test_count_letter():
    assert count_letter(["banana", "apple"], "a") == 4
