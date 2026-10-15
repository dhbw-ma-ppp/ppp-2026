# Exercise 02. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import PROGRAM, TARGET

# ---------------------------------------------------------------- Part 1 (in class)


def step(memory, position):
    """Execute the instruction that starts at `position` in memory.

    Opcode 1 adds, opcode 2 multiplies, opcode 99 halts (see README.md).
    Return the position of the next instruction, or None if the opcode is 99.
    If the opcode is neither of the three mentioned it will return -1, which stands for an error
    """
    u = position
    if memory[u] == 1:
        sum = memory[u + 3]
        summand1 = memory[u + 1]
        summand2 = memory[u + 2]
        memory[sum] = memory[summand1] + memory[summand2]
        return position + 4
    elif memory[u] == 2:
        product = memory[u + 3]
        mult1 = memory[u + 1]
        mult2 = memory[u + 2]
        memory[product] = memory[mult1] * memory[mult2]
        return position + 4
    elif memory[u] == 99:
        return None
    else:
        return -1


def run(memory):
    """Execute instructions, starting at position 0, until the program halts.

    Return the value at position 0 after the program has halted.
    """
    memory1 = memory.copy()
    for u in range(0, len(memory1), 4):
        if memory1[u] == 1:
            sum = memory1[u + 3]
            summand1 = memory1[u + 1]
            summand2 = memory1[u + 2]
            memory1[sum] = memory1[summand1] + memory1[summand2]
        elif memory1[u] == 2:
            product = memory1[u + 3]
            mult1 = memory1[u + 1]
            mult2 = memory1[u + 2]
            memory1[product] = memory1[mult1] * memory1[mult2]
        elif memory1[u] == 99:
            break
        else:
            return -1
    return memory1[0]


# ---------------------------------------------------------------- Part 2 (at home)


def run_with(program, noun, verb):
    """Return the result of program with noun at position 1 and verb at position 2."""
    if noun % 2 != 1 and noun % 2 != 0:
        return -1
    if verb % 2 != 1 and verb % 2 != 0:
        return -1
    memory = program.copy()

    memory[1] = noun
    memory[2] = verb
    return run(memory)


def find_noun_verb(program, target):
    """Return (noun, verb), each from 0 to 99, for which run_with gives target.

    Return None if there is no such pair.
    """
    for noun in range(100):
        for verb in range(100):
            if run_with(program, noun, verb) == target:
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
