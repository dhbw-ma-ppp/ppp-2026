# Exercise 02. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import PROGRAM, TARGET

# ---------------------------------------------------------------- Part 1 (in class)


def step(memory, position):
    """Execute the instruction that starts at `position` in memory.

    Opcode 1 adds, opcode 2 multiplies, opcode 99 halts (see README.md).
    Return the position of the next instruction, or None if the opcode is 99.

    If a value other than 1, 2 or 99 is being read the program should throw an error to ensure only
    executable code is trying to be executed.
    """

    if memory[position] == 99:
        return None
    elif memory[position] == 1:
        memory[memory[position + 3]] = memory[memory[position + 1]] + memory[memory[position + 2]]
    elif memory[position] == 2:
        memory[memory[position + 3]] = memory[memory[position + 1]] * memory[memory[position + 2]]
    else:
        raise ValueError("The opcode only allows 1, 2 or 99.")

    return position + 4


def run(memory):
    """Execute instructions, starting at position 0, until the program halts.

    Return the value at position 0 after the program has halted.
    """
    index = 0

    copied_memory = memory.copy()

    while index is not None:
        index = step(copied_memory, index)
    return copied_memory[0]


# ---------------------------------------------------------------- Part 2 (at home)


def run_with(program, noun, verb):
    """Return the result of program with noun at position 1 and verb at position 2."""
    if noun < 0 or verb < 0:
        raise ValueError(
            "Noun and Verb must be greater or equal to 0. Negative indeces are not allowed."
        )

    program[1] = noun
    program[2] = verb
    return run(program)


def find_noun_verb(program, target):
    """Return (noun, verb), each from 0 to 99, for which run_with gives target.

    Return None if there is no such pair.
    """
    for first_index in range(100):
        for second_index in range(first_index, 100):
            if target == run_with(program, first_index, second_index):
                return first_index, second_index
            elif target == run_with(program, second_index, first_index):
                return second_index, first_index

    return None


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print("Part 1")
    print("1:", run([2, 9, 10, 9, 1, 9, 11, 0, 99, 6, 7, 3]))
    print("2:", run(list(PROGRAM)))

    print("Part 2")
    print("3:", run_with(list(PROGRAM), 0, 0))
    print("4:", find_noun_verb(list(PROGRAM), TARGET))
