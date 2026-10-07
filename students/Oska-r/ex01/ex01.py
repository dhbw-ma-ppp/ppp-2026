# Exercise 01. See README.md for the full task.
# Each function below has its first line written for you. The text in triple quotes says
# what the function should do. Replace the `pass` line with your code, ending with `return`.

from puzzle_input import INSTRUCTIONS

# ---------------------------------------------------------------- Part 1 (in class)


def quotient_and_remainder(a, b):
    """Return the quotient and remainder of the integer division a // b, e.g. (3, 2) for 17, 5."""

    if type(a) is not int:
        raise TypeError("Dividend must be an integer.")
    if type(b) is not int:
        raise TypeError("Divisor must be an integer.")

    if b == 0:
        raise ValueError("Division with 0 is not permitted.")

    return divmod(a, b)


def celsius_to_fahrenheit(celsius):
    """Return the temperature celsius (in °C) converted to °F."""

    if type(celsius) is not int:
        raise TypeError("Temperature in Celsius must be an integer.")

    if celsius < -273:
        raise ValueError("Temperature in celsius must be above -274 degrees.")

    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit


def first_three(text):
    """Return the first three characters of text."""

    if type(text) is not str:
        raise TypeError("Text must be a string.")

    if len(text) < 3:
        raise ValueError("Text must be at least 3 characters long.")

    return text[:3]


def last_four(text):
    """Return the last four characters of text."""

    if type(text) is not str:
        raise TypeError("Text must be a string.")

    if len(text) < 4:
        raise ValueError("Text must be at least 4 characters long.")

    return text[-4:]


def backwards(text):
    """Return text backwards."""

    if type(text) is not str:
        raise TypeError("Text must be a string.")

    return text[::-1]


def science_to_analytics(text):
    """Return text with every "Science" replaced by "Analytics"."""

    if type(text) is not str:
        raise TypeError("Text must be a string.")

    return text.replace("Science", "Analytics")


def floor(instructions):
    """Return the floor Santa ends up on, starting on floor 0: "(" is one up, ")" one down."""

    check_instructions(instructions)

    return instructions.count("(") - instructions.count(")")


# ---------------------------------------------------------------- Part 2 (at home)


def floor_after(instructions, steps):
    """Return the floor Santa is on after following only the first `steps` instructions.

    Use your function `floor` from Part 1.
    """

    if type(steps) is not int:
        raise TypeError("Steps must be an integer.")

    if steps < 0:
        raise ValueError("Steps must be greater or equal to 0.")

    # This type check of instructions happens in floor again and is therefore redundant.
    # However floor_after() needs this check to ensure len(instructions) is accessible and
    # floor() needs this check independently to function as a global function.

    if type(instructions) is not str:
        raise TypeError("Instructions must be a string.")

    if steps > len(instructions):
        raise ValueError("Steps must be smaller or equal to the length of instructions.")

    return floor(instructions[:steps])


def mirrored(instructions):
    """Return the instructions as seen in a mirror: every "(" becomes ")" and vice versa."""

    check_instructions(instructions)

    return instructions.replace("(", "a").replace(")", "(").replace("a", ")")


def common_elements(first, second):
    """Return the set of elements that occur in both lists."""

    if type(first) is not list:
        raise TypeError("The first argument must be a list.")

    if type(second) is not list:
        raise TypeError("The second argument must be a list.")

    return set(first) & set(second)


def count_letter(words, letter):
    """Return how often letter occurs in all the strings of the list words together."""

    if type(words) is not list:
        raise TypeError("Words must be a list.")

    for word in words:
        if type(word) is not str:
            raise ValueError("All Elements of words must be a string.")

    if type(letter) is not str:
        raise ValueError("Letter must be a string.")

    # This allows checking longer strings as letters.
    # If the function specifically requires the letter to be a single character, the line below would change to: if len(letter) != 1:
    if len(letter) < 1:
        raise ValueError("Letter cannot be empty.")

    connected_string = "".join(words)
    return connected_string.count(letter)


def bonus(instructions):

    check_instructions(instructions)

    floor = 0
    for index, char in enumerate(instructions):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1

        if floor == -1:
            return index
    return -1


def check_instructions(instructions):
    if type(instructions) is not str:
        raise TypeError("Instructions must be a string.")

    if instructions.replace("(", "").replace(")", "") != "":
        raise ValueError("Instructions can only contain '(' and ')'.")


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
