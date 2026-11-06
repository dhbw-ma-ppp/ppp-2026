# Exercise 04. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path

# The program file sits next to this file, wherever you run Python from (see README.md).
PROGRAM_FILE = Path(__file__).parent / "diagnostic.txt"

# Reads two numbers and outputs the larger one (see README.md, Part 2).
MAX_OF_TWO = [3, 20, 3, 21, 7, 20, 21, 22, 1005, 22, 14, 4, 20, 99, 4, 21, 99, 0, 0, 0, 0, 0, 0]

# ---------------------------------------------------------------- Part 1 (in class)


def parse_program(text):
    """Return the numbers in `text` as a list of ints.

    Numbers are separated by commas and/or line breaks. A `#` starts a comment that runs to
    the end of its line. Spaces and blank lines don't matter.
    """
    result = []
    for line in text.splitlines():
        program = line.split("#")[0].strip()

        if program == "":
            continue

        for number in program.split(","):
            result.append(int(number.strip()))

    return result


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    with open(PROGRAM_FILE, "r") as file:
        text = file.read()
        path = parse_program(text)
    return path


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    opcode = instruction % 100
    instruction = instruction // 100
    mode = []
    for i in range(3):
        mode.append(instruction % 10)
        instruction = instruction // 10
    return opcode, mode


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    _, modes = decode(memory[position])
    mode = modes[n - 1]
    value = memory[position + n]

    if mode == 0:
        return memory[value]  # memory[memory[position + n]]
    elif mode == 1:
        return value  # memory[position + n]
    else:
        raise ValueError("Invalid opcode {}".format(mode))


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    """
    opcode, _ = decode(memory[position])

    if opcode == 99:
        return None
    if opcode == 1:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        memory[memory[position + 3]] = a + b
        return position + 4

    elif opcode == 2:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        memory[memory[position + 3]] = a * b
        return position + 4

    elif opcode == 3:
        memory[memory[position + 1]] = inputs.pop(0)
        return position + 2

    elif opcode == 4:
        outputs.append(parameter(memory, position, 1))
        return position + 2

    elif opcode == 5:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        if a != 0:
            return b
        else:
            return position + 3

    elif opcode == 6:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        if a == 0:
            return b
        else:
            return position + 3

    elif opcode == 7:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        memory[memory[position + 3]] = int(a < b)
        return position + 4

    elif opcode == 8:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        memory[memory[position + 3]] = int(a == b)
        return position + 4

    else:
        raise ValueError("Invalid opcode {}".format(opcode))


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    start = 0
    inputs = inputs.copy()
    outputs = []
    while start is not None:
        start = step(memory, start, inputs, outputs)
    return outputs


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", run([3, 0, 4, 0, 99], [42]))
    print("2:", run(program.copy(), [1]))

    print("Part 2")
    print("3:", run(MAX_OF_TWO.copy(), [17, 4]))
    print("4:", run(program.copy(), [5]))
