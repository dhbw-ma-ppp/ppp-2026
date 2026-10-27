# Exercise 04. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.
# import opcode
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
        leftSide = line.split("#")[0].strip()
        for part in leftSide.split(","):
            if part != "":
                numbers.append(int(part))
    return numbers


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    with open(path) as input_file:
        inputs = input_file.read()
    return parse_program(inputs)


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    digits = []
    modes = []
    opCodeArr = []

    if instruction == 99:
        opCode = 99
    else:
        for digit in str(instruction):
            digits.append(int(digit))
        opCodeArr.extend(digits[-2:])
        if len(opCodeArr) == 1:
            opCode = opCodeArr[0]
        elif opCodeArr[0] == 0:
            opCode = opCodeArr[1]
        else:
            raise ValueError("Opcode invalid.")
        modes.extend(digits[:-2])
    while len(modes) != 3:
        modes.insert(0, 0)
    modes.reverse()
    return opCode, modes


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    opCode_Mode = decode(memory[position])
    # opCode = opCode_Mode[0]
    modes = opCode_Mode[1]
    parameterMode = modes[n - 1]
    if parameterMode == 0:
        if n == 3:
            if n < len(memory):
                value = memory[position + n]
            else:
                value = None
        else:
            address = memory[position + n]
            if address == 99:
                return 99
            if address <= len(memory):
                value = memory[address]
            else:
                value = None
    elif parameterMode == 1:
        value = memory[position + n]
    else:
        raise ValueError("Unknown mode.")
    return value


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError. Empty inputs, invalid starting point raise ValueErrors as well.
    """
    if len(memory) < position:
        raise IndexError("No starting point found.")
    else:
        opCode_Mode = decode(memory[position])
        opCode = opCode_Mode[0]
        if opCode == 99:
            return None
        if opCode == 3:
            newPosition = memory[position + 1]
            if len(inputs) >= 1:
                memory[newPosition] = inputs.pop(0)
            else:
                raise ValueError("No inputs found.")
            return position + 2
        elif opCode == 4:
            newPosition = memory[position + 1]
            if newPosition < len(memory):
                outputs.append(memory[newPosition])
            else:
                outputs.append(newPosition)
            return position + 2

        if len(memory) >= position + 3:
            number1 = parameter(memory, position, 1)
            number2 = parameter(memory, position, 2)
            result = parameter(memory, position, 3)
        else:
            raise IndexError("More information needed.")

        if result is None:
            pass
        if number1 is None or number2 is None:
            raise ValueError("One number is None")
        else:
            if opCode == 1:
                memory[result] = number1 + number2
            elif opCode == 2:
                memory[result] = number1 * number2
            elif opCode == 5:
                if number1 != 0:
                    return number2
                else:
                    return position + 3
            elif opCode == 6:
                if number1 == 0:
                    return number2
                else:
                    return position + 3
            elif opCode == 7:
                if number1 < number2:
                    memory[result] = number1
                else:
                    memory[result] = 0
            elif opCode == 8:
                if number1 == number2:
                    memory[result] = 1
                else:
                    memory[result] = 0

            else:
                raise ValueError
    return position + 4


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    outputList = []
    inputsCopy = inputs.copy()
    startIndex = 0
    while startIndex is not None:
        startIndex = step(memory, startIndex, inputsCopy, outputList)
    return outputList


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", run([3, 0, 4, 0, 99], [42]))
    print("2:", run(program.copy(), [1]))

    print("Part 2")
    print("3:", run(MAX_OF_TWO.copy(), [17, 4]))
    print("4:", run(program.copy(), [5]))
