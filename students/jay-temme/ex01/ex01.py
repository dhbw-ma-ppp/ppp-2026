# Exercise 01. See README.md for the full task.
# Each function below has its first line written for you. The text in triple quotes says
# what the function should do. Replace the `pass` line with your code, ending with `return`.

from puzzle_input import INSTRUCTIONS

# ---------------------------------------------------------------- Part 1 (in class)


def quotient_and_remainder(a, b):
    """Return the quotient and remainder of the integer division a // b, e.g. (3, 2) for 17, 5."""

    # check if a and b are integers
    if (type(a) is not int) or (type(b) is not int):
        raise TypeError("input paramenters should be of type integer.")

    # calculate quotient and remainder
    quotient = a // b
    remainder = a % b

    return (quotient, remainder)


def celsius_to_fahrenheit(celsius):
    """Return the temperature celsius (in °C) converted to °F."""

    # check if celcius is an integer or a float
    if (type(celsius) is not int) and (type(celsius) is not float):
        raise TypeError("input paramenter should be of type integer or float.")

    # calculate fahrenheit
    fahrenheit = (celsius * 9 / 5) + 32

    return fahrenheit


def first_three(text):
    """Return the first three characters of text."""

    # check if text is a string
    if type(text) is not str:
        raise TypeError("input paramenter should be of type string.")

    # slice text into the desired substring
    substring = text[:3]

    return substring


def last_four(text):
    """Return the last four characters of text."""

    # check if text is a string
    if type(text) is not str:
        raise TypeError("input paramenter should be of type string.")

    # slice text into the desired stubstring
    substring = text[-4:]

    return substring


def backwards(text):
    """Return text backwards."""

    # check if text is a string
    if type(text) is not str:
        raise TypeError("input paramenter should be of type string.")

    # slice text into the desired string
    reversed_string = text[::-1]

    return reversed_string


def science_to_analytics(text):
    """Return text with every "Science" replaced by "Analytics"."""

    # check if text is a string
    if type(text) is not str:
        raise TypeError("input paramenter should be of type string.")

    # replacing substring
    new_text = text.replace("Science", "Analytics")

    return new_text


def floor(instructions):
    """Return the floor Santa ends up on, starting on floor 0: "(" is one up, ")" one down."""

    # check if instructions is a string
    if type(instructions) is not str:
        raise TypeError("input paramenter should be of type string.")

    # calculate floor
    floors_up = instructions.count("(")
    floors_down = instructions.count(")")
    floor = floors_up - floors_down

    return floor


# ---------------------------------------------------------------- Part 2 (at home)


def floor_after(instructions, steps):
    """Return the floor Santa is on after following only the first `steps` instructions.

    Use your function `floor` from Part 1.
    """

    # check if steps is an integer
    if type(steps) is not int:
        raise TypeError("second input parameter should be of type integer.")

    # check if steps is non-negative
    if steps < 0:
        raise ValueError("second input parameter should be non-negative.")

    # calculate floor
    floor_after_steps = floor(instructions[:steps])

    return floor_after_steps


def mirrored(instructions):
    """Return the instructions as seen in a mirror: every "(" becomes ")" and vice versa."""

    if type(instructions) is not str:
        raise TypeError("input paramenter should be of type string.")

    # mirror input string
    mirrored_instructions = instructions.replace("(", "a").replace(")", "(").replace("a", ")")

    return mirrored_instructions


def common_elements(first, second):
    """Return the set of elements that occur in both lists."""

    # calculate common elements
    common_elements = set(first) & set(second)

    return common_elements


def count_letter(words, letter):
    """Return how often letter occurs in all the strings of the list words together."""

    # check if letter is a string
    if type(letter) is not str:
        raise TypeError("second input parameter should be of type string.")

    # check if letter is not empty
    if letter == "":
        raise ValueError("second input parameter should not be empty.")

    count = 0
    for word in words:
        # check if words only contains strings
        if type(word) is not str:
            raise TypeError("first input paramenter should only contain strings.")

        count += word.count(letter)
    return count


# ---------------------------------------------------------------- Bonus


def first_basement_enter(instructions):

    # check if instructions is a string
    if type(instructions) is not str:
        raise TypeError("input paramenter should be of type string.")

    current_floor = 0

    # iterate through each instruction
    for step, instruction in enumerate(instructions):
        # calculate floor after instruction
        if instruction == "(":
            current_floor += 1
        elif instruction == ")":
            current_floor -= 1

        # check if the basement has been entered
        if current_floor < 0:
            return step + 1

    # return None if the basement was not entered
    return None


# ---------------------------------------------------------------- Answers

# The lines below run when you run this file (`uv run python ex01.py`), but not when the
# tests import it. Leave the `if` line as it is; we'll see what it means later.
if __name__ == "__main__":
    first_list = ["drs", "clt", "iny", "alv", "nvy", "bpt", "gkw", "fkm", "jrz", "hov", "bqu",
                  "bov", "eju", "eiz", "fjm", "bek", "abj", "hov", "coq", "iox", "efs", "krw",
                  "evy", "elw", "gil", "ajq", "cek", "fkm", "mnu", "adf"]  # fmt: skip
    second_list = ["dlz", "akw", "bry", "eyz", "bny", "kst", "elw", "ekl", "djm", "aft", "gkw",
                   "krw", "coq", "evy", "bov", "bkl", "bov", "afs", "hov", "fjq", "cqu", "ahq",
                   "beh", "ijz", "ksy", "ilx", "htu", "epz", "ekl", "ajq"]  # fmt: skip

    print("Part 1")
    print("1:", quotient_and_remainder(2711274328912, 23369245575))
    print("2:", celsius_to_fahrenheit(233))
    print("3:", first_three("DataScience"), last_four("DataScience"))
    print("4:", backwards("DataScience"), science_to_analytics("DataScience"))
    print("5:", floor(INSTRUCTIONS))

    print("Part 2")
    print("6:", floor_after(INSTRUCTIONS, 1000))
    print("7:", floor(mirrored(INSTRUCTIONS)))
    print("8:", len(first_list), len(second_list))
    print("9:", common_elements(first_list, second_list))
    print("10:", count_letter(first_list, "a"), count_letter(second_list, "a"))

    print("Bonus")
    print("11:", first_basement_enter(INSTRUCTIONS))
