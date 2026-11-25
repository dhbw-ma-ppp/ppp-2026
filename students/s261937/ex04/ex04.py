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
    numbers = []

    for line in text.splitlines():
        line = line.split("#", 1)[0]

        for item in line.replace(",", " ").split():
            numbers.append(int(item))

    return numbers


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    text = Path(path).read_text(encoding="utf-8")
    return parse_program(text)


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    opcode = instruction % 100
    modes_number = instruction // 100

    modes = []

    for _ in range(3):
        modes.append(modes_number % 10)
        modes_number //= 10

    return opcode, modes


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    instruction = memory[position]
    _, modes = decode(instruction)

    mode = modes[n - 1]
    value = memory[position + n]

    if mode == 0:
        return memory[value]

    if mode == 1:
        return value

    raise ValueError(f"Unknown parameter mode: {mode}")


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    """
    instruction = memory[position]
    opcode, _ = decode(instruction)

    if opcode == 99:
        return None

    if opcode == 1:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        destination = memory[position + 3]

        memory[destination] = a + b
        return position + 4

    if opcode == 2:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        destination = memory[position + 3]

        memory[destination] = a * b
        return position + 4

    if opcode == 3:
        if not inputs:
            raise ValueError("Input requested, but no inputs are available")

        destination = memory[position + 1]
        memory[destination] = inputs.pop(0)

        return position + 2

    if opcode == 4:
        value = parameter(memory, position, 1)
        outputs.append(value)

        return position + 2

    if opcode == 5:
        condition = parameter(memory, position, 1)
        target = parameter(memory, position, 2)

        if condition != 0:
            return target

        return position + 3

    # Part 2: jump-if-false
    if opcode == 6:
        condition = parameter(memory, position, 1)
        target = parameter(memory, position, 2)

        if condition == 0:
            return target

        return position + 3

    # Part 2: less than
    if opcode == 7:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        destination = memory[position + 3]

        memory[destination] = int(a < b)

        return position + 4

    # Part 2: equals
    if opcode == 8:
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        destination = memory[position + 3]

        memory[destination] = int(a == b)

        return position + 4

    raise ValueError(f"Unknown opcode {opcode} at position {position}")


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    inputs = inputs.copy()
    outputs = []
    position = 0

    while position is not None:
        position = step(memory, position, inputs, outputs)

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
