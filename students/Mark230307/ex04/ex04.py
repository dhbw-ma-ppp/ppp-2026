# Exercise 04. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path

# The program file sits next to this file, wherever you run Python from (see README.md).
PROGRAM_FILE = Path(__file__).parent / "diagnostic.txt"

# Reads two numbers and outputs the larger one (see README.md, Part 2).
MAX_OF_TWO = [3, 20, 3, 21, 7, 20, 21, 22, 1005, 22, 14, 4, 20, 99, 4, 21, 99, 0, 0, 0, 0, 0, 0]

# ---------------------------------------------------------------- Part 1 (in class)


def is_None(value_to_prove):
    if value_to_prove is None:
        raise ValueError(value_to_prove + "has no value/is none")


def parse_program(text):
    """Return the numbers in `text` as a list of ints.

    Numbers are separated by commas and/or line breaks. A `#` starts a comment that runs to
    the end of its line. Spaces and blank lines don't matter.
    """
    numbers = []
    is_None(text)
    for line in text.splitlines():
        line = line.split("#")[0]
        elements = line.split(",")
        for number in elements:
            number = number.strip()
            if number:
                numbers.append(int(number))
    return numbers


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    is_None(path)
    with open(path, "r") as file:
        part_of_file = file.read()
    return parse_program(part_of_file)


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    is_None(instruction)
    opcode = instruction % 100
    modes = instruction // 100

    first_mode = modes % 10
    second_mode = (modes // 10) % 10
    third_mode = (modes // 100) % 10

    return opcode, [first_mode, second_mode, third_mode]


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    is_None(memory)
    is_None(position)
    is_None(n)

    instruction = memory[position]

    opcode, modes = decode(instruction)

    mode = modes[n - 1]
    value = memory[position + n]

    if mode == 0:
        result = memory[value]
    elif mode == 1:
        result = value
    else:
        raise ValueError("Unknown mode. mode has to be 0 or 1!")

    return result


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.

    If Opcode 3 can't get a number from input, because it is empty or none, it will
    raise an IndexError for Opcode 3 operations
    """
    is_None(memory)
    is_None(position)

    instruction = memory[position]
    opcode, modes = decode(instruction)

    if opcode == 1:  # Addition
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        target = memory[position + 3]

        memory[target] = a + b
        return position + 4

    elif opcode == 2:  # Multiplication
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        target = memory[position + 3]

        memory[target] = a * b
        return position + 4

    elif opcode == 3:  # Input, dabei braucht input als Übergabeparameter Ganzzahl Werte
        if input is None or input == []:
            raise IndexError("opcode 3 needs a value from input, input can't be empty or None!")
        target = memory[position + 1]
        memory[target] = inputs.pop(0)

        return position + 2

    elif opcode == 4:  # Output
        value = parameter(memory, position, 1)
        outputs.append(value)

        return position + 2

    elif opcode == 5:  # Jump-if-true
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)

        if a != 0:
            return b
        else:
            return position + 3

    elif opcode == 6:  # Jump-if-false
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)

        if a == 0:
            return b
        else:
            return position + 3

    elif opcode == 7:  # Less than
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        target = memory[position + 3]

        if a < b:
            memory[target] = 1
        else:
            memory[target] = 0

        return position + 4

    elif opcode == 8:  # Equals
        a = parameter(memory, position, 1)
        b = parameter(memory, position, 2)
        target = memory[position + 3]

        if a == b:
            memory[target] = 1
        else:
            memory[target] = 0

        return position + 4

    elif opcode == 99:  # stop program
        return None

    else:  # opcode that doesn't exist
        raise ValueError(f"Unknown opcode: {opcode}")


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    position = 0
    outputs = []
    copy_of_input = inputs.copy()

    while position is not None:
        position = step(memory, position, copy_of_input, outputs)

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
