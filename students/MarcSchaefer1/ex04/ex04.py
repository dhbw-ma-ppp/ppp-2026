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
    ListCommandLines = text.splitlines()
    WithoutComments = []

    for line in ListCommandLines:
        WithoutComments.append(line.split("#")[0])

    LineWsithoutSpaces = []

    for line in WithoutComments:
        newline = ""
        for char in line:
            if char != " ":
                newline = newline + char
        LineWsithoutSpaces.append(newline)

    newList = []

    for elem in LineWsithoutSpaces:
        if elem != "":
            newList.append(elem)

    numList = []
    for line in newList:
        for elem in line.split(","):
            numList.append(int(elem))

    return numList


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    with open(path) as file:
        text = file.read()

    return parse_program(text)


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """

    last2digits = int(str(instruction)[-2:])

    modes = str(instruction)[:-2][::-1]

    temp_list = []

    for mode in modes:
        temp_list.append(int(mode))

    while len(temp_list) < 3:
        temp_list.append(0)

    return last2digits, temp_list


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """

    instruction = memory[position]  # Instructions an Stelle position, nicht nur 0
    mode = decode(
        instruction
    )[
        1
    ][
        n - 1
    ]  # decodierung der instructions und entnahme des modus aus dem 2. teil des tupels von stelle n-1
    value = memory[position + n]

    if mode == 0:
        return memory[value]
    elif mode == 1:
        return value
    else:
        raise ValueError("Unknown parameter mode")


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.

    if inputs is empty return -1
    """

    opcode = decode(
        memory[position]
    )[
        0
    ]  # Take 1. element of tuple which is the result of decoding the memory at position giving the instructions

    if opcode == 1:
        posToWrite = memory[position + 3]
        param1 = parameter(memory, position, 1)
        param2 = parameter(memory, position, 2)
        memory[posToWrite] = param1 + param2
        return position + 4
    elif opcode == 2:
        posToWrite = memory[position + 3]
        param1 = parameter(memory, position, 1)
        param2 = parameter(memory, position, 2)
        memory[posToWrite] = param1 * param2
        return position + 4
    elif opcode == 3:
        if len(inputs) == 0:
            return -1
        posToWrite = memory[position + 1]  # Überschreibe die oben gesetzte posToWrite
        memory[posToWrite] = inputs.pop(0)
        return position + 2  # Sprunggröße 2 für opcode 3 und 4 es wird
    elif opcode == 4:
        outputs.append(parameter(memory, position, 1))
        return position + 2
    elif opcode == 5:
        if parameter(memory, position, 1) != 0:
            return parameter(memory, position, 2)
        return position + 3
    elif opcode == 6:
        if parameter(memory, position, 1) == 0:
            return parameter(memory, position, 2)
        return position + 3
    elif opcode == 7:
        param1 = parameter(memory, position, 1)
        param2 = parameter(memory, position, 2)
        posToWrite = memory[position + 3]
        memory[posToWrite] = int(param1 < param2)
        return position + 4
    elif opcode == 8:
        param1 = parameter(memory, position, 1)
        param2 = parameter(memory, position, 2)
        posToWrite = memory[position + 3]
        memory[posToWrite] = int(param1 == param2)
        return position + 4
    elif opcode == 99:
        return None
    else:
        raise ValueError("Unknown opcode")


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """

    NextPos = 0
    inputsCopy = inputs[:]
    outputs = []
    while NextPos is not None:
        NextPos = step(memory, NextPos, inputsCopy, outputs)
        if NextPos == -1:
            return -1
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
