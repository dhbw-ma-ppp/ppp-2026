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
    numbers = []  # only relevant content (number as integer)

    for line in text.splitlines():
        code = line.split("#", 1)[0]  # Step 1, delete everything after first comment

        for number in code.replace(
            ",", " "
        ).split():  # replacing commas and splitting the different numbers
            numbers.append(int(number))  # casting to integer, appending to list
    return numbers


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    with open(path) as file:
        text = file.read()
        return parse_program(text)  # Function parse_program is being reused


def decode(instruction):
    instruction = str(instruction).zfill(5)  # conversion to a string and filling in zeros

    opcode = int(instruction[-2:])

    modes = [int(instruction[-3]), int(instruction[-4]), int(instruction[-5])]

    return opcode, modes


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    _, modes = decode(memory[position])

    mode = modes[
        n - 1
    ]  # selects the mode on the correct position in the list "modes", depeding on n

    value = memory[
        position + n
    ]  # make the n-th parameter (starting from the current position) our value

    if mode == 0:
        return memory[value]

    if mode == 1:
        return value

    raise ValueError(
        f"Unknown parameter mode {mode} at position {position}"
    )  # ValueError for all other modes


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.

    When "Inputs" is empty, a value error will be raised.
    """
    opcode, _ = decode(memory[position])

    if opcode == 99:
        return None

    if opcode in (1, 2, 7, 8):  # Looking for one of the four opcodes with two inputs
        first = parameter(memory, position, 1)
        second = parameter(memory, position, 2)
        destination = memory[position + 3]

        if opcode == 1:
            memory[destination] = first + second
        elif opcode == 2:
            memory[destination] = first * second
        elif opcode == 7:
            memory[destination] = int(
                first < second
            )  # int gives a "1" if condition is true, otherwise "0"
        else:
            memory[destination] = int(first == second)

        return position + 4

    if opcode == 3:
        if not inputs:
            raise ValueError(f"No input available for opcode 3 at position {position}")

        destination = memory[position + 1]
        memory[destination] = inputs.pop(0)  # assign the input as a memory value and delete it
        return position + 2

    if opcode == 4:
        outputs.append(
            parameter(memory, position, 1)
        )  # uses parameter() to find the value and appends to the list "outputs"
        return position + 2

    if opcode in (5, 6):  # category of "jump opcodes"
        condition = parameter(memory, position, 1)
        target = parameter(memory, position, 2)  # target is needed when the condition is true

        if opcode == 5:
            should_jump = condition != 0
        else:
            should_jump = condition == 0

        return target if should_jump else position + 3  # checks if shoud_jump is true/1 or false/0

    raise ValueError(
        f"Unknown opcode {opcode} at position {position}"
    )  # ValueError for all other opcodes


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    inputs_copy = inputs.copy()  # run() must not change the input
    outputs = []
    position = 0

    while position is not None:  # if None is returned, the program ends
        position = step(memory, position, inputs_copy, outputs)

    return outputs


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print(parse_program("1,0,0,0,99"))
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", run([3, 0, 4, 0, 99], [42]))
    print("2:", run(program.copy(), [1]))

    print("Part 2")
    print("3:", run(MAX_OF_TWO.copy(), [17, 4]))
    print("4:", run(program.copy(), [5]))
