# Exercise 02. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import PROGRAM, TARGET

# ---------------------------------------------------------------- Part 1 (in class)


def step(memory, position):
    """Execute the instruction that starts at `position` in memory.

    Opcode 1 adds, opcode 2 multiplies, opcode 99 halts (see README.md).
    Return the position of the next instruction, or None if the opcode is 99.
    If opcode isn´t 1 or 2, then we skip the current instruction and go to the next.
    """
    opcode = memory[position]
    if opcode == 1:
        value = memory[memory[position + 1]] + memory[memory[position + 2]]
        memory[memory[position + 3]] = value
    elif opcode == 2:
        value = memory[memory[position + 1]] * memory[memory[position + 2]]
        memory[memory[position + 3]] = value
    elif opcode == 99:
        return None

    return position + 4


def run(memory):
    """Execute instructions, starting at position 0, until the program halts.

    Return the value at position 0 after the program has halted.
    """
    position = 0
    while position is not None:
        position = step(memory, position)
    return memory[0]


# ---------------------------------------------------------------- Part 2 (at home)


def run_with(program, noun, verb):
    """Return the result of program with noun at position 1 and verb at position 2."""
    memory = list(program)
    memory[1] = noun
    memory[2] = verb
    return run(memory)


def find_noun_verb(program, target):
    """Return (noun, verb), each from 0 to 99, for which run_with gives target.

    Return None if there is no such pair.
    """
    for counter1 in range(100):
        for counter2 in range(100):
            if run_with(program, counter1, counter2) == target:
                return counter1, counter2
    return None


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print("Part 1")
    print("1:", run([2, 9, 10, 9, 1, 9, 11, 0, 99, 6, 7, 3]))
    print("2:", run(list(PROGRAM)))

    print("Part 2")
    print("3:", run_with(list(PROGRAM), 0, 0))
    print("4:", find_noun_verb(list(PROGRAM), TARGET))
