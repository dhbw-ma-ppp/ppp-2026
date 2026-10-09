# Exercise 01. See README.md for the full task.
# Each function below has its first line written for you. The text in triple quotes says
# what the function should do. Replace the `pass` line with your code, ending with `return`.

from puzzle_input import INSTRUCTIONS

# ---------------------------------------------------------------- Part 1 (in class)


def quotient_and_remainder(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder


def celsius_to_fahrenheit(celsius):
    fahrenheit = celsius * 9 / 5 + 32
    return fahrenheit


def first_three(text):
    return text[:3]


def last_four(text):
    return text[-4:]


def backwards(text):
    return text[::-1]


def science_to_analytics(text):
    return text.replace("Science", "Analytics")


def floor(instructions):
    """Return the floor Santa ends up on, starting on floor 0: "(" is one up, ")" one down."""
    current_floor = 0

    for zeichen in instructions:
        if zeichen == "(":
            current_floor += 1
        elif zeichen == ")":
            current_floor -= 1

    return current_floor


# ---------------------------------------------------------------- Part 2 (at home)


def floor_after(instructions, steps):
    return floor(instructions[:steps])


def mirrored(instructions):
    """Return the instructions as seen in a mirror: every "(" becomes ")" and vice versa."""
    result = ""

    for zeichen in instructions:
        if zeichen == "(":
            result += ")"
        elif zeichen == ")":
            result += "("

    return result


def common_elements(first, second):
    """Return the set of elements that occur in both lists."""
    return set(first).intersection(set(second))


def count_letter(words, letter):
    """Return how often letter occurs in all the strings of the list words together."""
    count = 0

    for word in words:
        count += word.count(letter)

    return count


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
