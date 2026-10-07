# Exercise 01. See README.md for the full task.
# Each function below has its first line written for you. The text in triple quotes says
# what the function should do. Replace the `pass` line with your code, ending with `return`.

from puzzle_input import INSTRUCTIONS

# ---------------------------------------------------------------- Part 1 (in class)


def quotient_and_remainder(a, b):
    if b == 0:  # undefined zero division
        pass
    if type(a) is not int or type(b) is not int:  # idiv and especially mod requires whole numbers!
        pass
    return a // b, a % b


def celsius_to_fahrenheit(celsius):
    return (celsius * 9) / 5 + 32


def first_three(text):
    return text[:3]


def last_four(text):
    return text[len(text) - 4 :]


def backwards(text):
    return text[::-1]


def science_to_analytics(text):
    return text.replace("Science", "Analytics")


def floor(instructions):
    """Return the floor Santa ends up on, starting on floor 0: "(" is one up, ")" one down."""
    return instructions.count("(") - instructions.count(")")


# ---------------------------------------------------------------- Part 2 (at home)


def floor_after(instructions, steps):
    return floor(instructions[:steps])


def mirrored(instructions):
    #dont ask why (im a c dev)
    x = ~0                                  #a bitield where 1s are assumed ")", so only we need to flip them incase of "("
    index_counter = 0
    for instruction in instructions:
        if instruction == "(":
            x = x & ~(1 << index_counter)   #sets the bit at position index_counter of bitfield x to 0.
        index_counter += 1
    x = ~x                                  # unnecessary if you think about it but for understanding of algorithm :))
    solution = ""                           #for reconstruction of new instructions
    for i in range(0, index_counter):
        if x & (1 << i):                    #bit set at position i of bitfield x
            solution += ")"
        else:
            solution += "("
    return solution


def common_elements(first, second):
    return set(first).intersection(set(second))


def count_letter(words, letter):
    total_occurrences = 0
    for word in words:
        total_occurrences += word.count(letter)
    return total_occurrences


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
