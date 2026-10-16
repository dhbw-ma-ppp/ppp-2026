# Exercise 02. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import PROGRAM, TARGET

# ---------------------------------------------------------------- Part 1 (in class)


def step(memory, position):
    """Execute the instruction that starts at `position` in memory.

    Opcode 1 adds, opcode 2 multiplies, opcode 99 halts, anything else passes and the next position is returned (see README.md).
    Return the position of the next instruction, or None if the opcode is 99.
    """
    if len(memory) >= 1:
        op = memory[position]
    else:
        raise IndexError("No opcode detected.")

    if op == 99:
        return None

    if len(memory) >= 4:
        factor1 = memory[position + 1]
        factor2 = memory[position + 2]
        res = memory[position + 3]
    else:
        pass

    if op == 1:
        memory[res] = memory[factor1] + memory[factor2]
        # print(f"res bei add: {memory[res]}")
    elif op == 2:
        memory[res] = memory[factor1] * memory[factor2]
        # print(f"res bei mul: {memory[res]}")
    else:
        pass

    return position + 4


def run(memory):
    """Execute instructions, starting at position 0, until the program halts.

    Return the value at position 0 after the program has halted.
    """
    beg = 0
    memoryCopy = memory.copy()
    while beg is not None:
        beg = step(memoryCopy, beg)
    return memoryCopy[0]


# ---------------------------------------------------------------- Part 2 (at home)


def run_with(program, noun, verb):
    """Return the result of program with noun at position 1 and verb at position 2."""
    if isinstance(noun, int) & isinstance(verb, int):
        program[1] = noun
        program[2] = verb
    else:
        raise TypeError("Input must be an int")
    return run(program)


def find_noun_verb(program, target):
    """Return (noun, verb), each from 0 to 99, for which run_with gives target.

    Return None if there is no such pair.
    """
    for i in range(0, 99):
        for j in range(0, 99):
            output = run_with(program, i, j)
            if output == target:
                return i, j
    return None


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print("Part 1")
    print("1:", run([2, 9, 10, 9, 1, 9, 11, 0, 99, 6, 7, 3]))
    print("2:", run(list(PROGRAM)))

    print("Part 2")
    print("3:", run_with(list(PROGRAM), 0, 0))
    print("4:", find_noun_verb(list(PROGRAM), TARGET))
