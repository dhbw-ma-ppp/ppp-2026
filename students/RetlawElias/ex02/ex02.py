# Exercise 02. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import PROGRAM, TARGET

# ---------------------------------------------------------------- Part 1 (in class)


def step(memory, position):
    try:
        match memory[position]:
            case 99:
                return None
            case 1:
                memory[memory[position + 3]] = (
                    memory[memory[position + 1]] + memory[memory[position + 2]]
                )
            case 2:
                memory[memory[position + 3]] = (
                    memory[memory[position + 1]] * memory[memory[position + 2]]
                )
            case _:
                raise ValueError("Invalid Operation! Only 1, 2 and 99 Operations are allowed!")

        return position + 4
    except IndexError:
        return 0


def run(memory):
    """Execute instructions, starting at position 0, until the program halts.

    Return the value at position 0 after the program has halted.
    """
    position = 0

    while True:
        position = step(memory, position)
        if position == None:
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
    for i in range(100):
        for j in range(100):
            if run_with(program, i, j) == target:
                return (i, j)

    return None


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print("Part 1")
    print("1:", run([2, 9, 10, 9, 1, 9, 11, 0, 99, 6, 7, 3]))
    print("2:", run(list(PROGRAM)))

    print("Part 2")
    print("3:", run_with(list(PROGRAM), 0, 0))
    print("4:", find_noun_verb(list(PROGRAM), TARGET))
