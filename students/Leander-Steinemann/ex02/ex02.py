# Exercise 02. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import PROGRAM, TARGET

# ---------------------------------------------------------------- Part 1 (in class)

HUNDRED_NOUN_PLUS_VERB = [1, 0, 0, 3, 2, 1, 13, 13, 1, 13, 2, 0, 99, 100] + [0] * 86


def step(memory, position):
    """Execute the instruction that starts at `position` in memory.

    Opcode 1 adds, opcode 2 multiplies, opcode 99 halts (see README.md).
    Return the position of the next instruction, or None if the opcode is 99.
    When the Opcode isn't 1,2 or 99, then it wouldn't retourn anything. I think it should return -1.
    """
    if memory[position] == 99:
        return None
    elif memory[position] == 1:
        a = memory[memory[position + 1]] + memory[memory[position + 2]]
        memory[memory[position + 3]] = a
        return position + 4
    elif memory[position] == 2:
        b = memory[memory[position + 1]] * memory[memory[position + 2]]
        memory[memory[position + 3]] = b
        return position + 4
    else:
        return -1


def run(memory):
    """Execute instructions, starting at position 0, until the program halts.

    Return the value at position 0 after the program has halted.
    """
    Position = 0
    while Position is not None:
        Position = step(memory, Position)
        if Position == -1:
            return -1
    return memory[0]


# ---------------------------------------------------------------- Part 2 (at home)


def run_with(program, noun, verb):
    """Return the result of program with noun at position 1 and verb at position 2."""
    program[1] = noun
    program[2] = verb
    return run(program.copy())


def find_noun_verb(program, target):
    """Return (noun, verb), each from 0 to 99, for which run_with gives target.

    Return None if there is no such pair.
    """
    """if run(program.copy())==target:
          return (program[1], program[2])
    if:"""
    for noun in range(100):
        for verb in range(100):
            if run_with(program.copy(), noun, verb) == target:
                return (noun, verb)
    return None


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print("Part 1")
    print("1:", run([2, 9, 10, 9, 1, 9, 11, 0, 99, 6, 7, 3]))
    print("2:", run(list(PROGRAM)))

    print("Part 2")
    print("3:", run_with(list(PROGRAM), 0, 0))
    print("4:", find_noun_verb(list(PROGRAM), TARGET))
