# Exercise 02. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import PROGRAM, TARGET

# ---------------------------------------------------------------- Part 1 (in class)


def step(memory, position):
    """Execute the instruction that starts at `position` in memory.

    Opcode 1 adds, opcode 2 multiplies, opcode 99 halts (see README.md).
    Return the position of the next instruction, or None if the opcode is 99.
    If one or more instruction(s) is/are unknown, -1 is returned.
    step() supposes that the only opcode with no parameters is 99.
    """

    if memory[position] == 99:
        return None

    first = memory[memory[position + 1]]
    second = memory[memory[position + 2]]

    if memory[position] == 1:  # addition
        memory[memory[position + 3]] = first + second
    elif memory[position] == 2:  # multi
        memory[memory[position + 3]] = first * second
    else:
        return -1

    return position + 4


def run(memory):
    """Execute instructions, starting at position 0, until the program halts.

    Return the value at position 0 after the program has halted.
    """
    program = memory.copy()  # else programm is modified! bad for brute forcing last exercise e.g.
    IP = 0
    while IP is not None:
        IP = step(program, IP)
    return program[0]


# ---------------------------------------------------------------- Part 2 (at home)


def run_with(program, noun, verb):
    """Return the result of program with noun at position 1 and verb at position 2."""
    program[1] = noun
    program[2] = verb
    return run(program)


def find_noun_verb(program, target):
    """Return (noun, verb), each from 0 to 99, for which run_with gives target.

    Return None if there is no such pair.
    """
    for n in range(0, 100):
        for v in range(0, 100):
            if run_with(program, n, v) == target:
                return n, v
    return None


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print("Part 1")
    print("1:", run([2, 9, 10, 9, 1, 9, 11, 0, 99, 6, 7, 3]))
    print("2:", run(list(PROGRAM)))

    print("Part 2")
    print("3:", run_with(list(PROGRAM), 0, 0))
    print("4:", find_noun_verb(list(PROGRAM), TARGET))
