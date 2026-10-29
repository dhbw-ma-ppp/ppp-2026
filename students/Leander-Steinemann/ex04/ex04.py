# Exercise 04. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path


# The program file sits next to this file, wherever you run Python from (see README.md).
PROGRAM_FILE = Path(__file__).parent / "diagnostic.txt"

# Reads two numbers and outputs the larger one (see README.md, Part 2).
MAX_OF_TWO = [3, 20, 3, 21, 7, 20, 21, 22, 1005, 22, 14, 4, 20, 99, 4, 21, 99, 0, 0, 0, 0, 0, 0]


# ---------------------------------------------------------------- Part 1 (in class)
def first_is_number(to_test):
    try:
        int(to_test.lstrip()[0])
        return True
    except ValueError:
        return False
    except IndexError:
        return False


def parse_program(text):
    """Return the numbers in `text` as a list of ints.

    Numbers are separated by commas and/or line breaks. A `#` starts a comment that runs to
    the end of its line. Spaces and blank lines don't matter.
    """
    numbers = []

    for line in text.splitlines():
        if first_is_number(line):
            line_without_comment = line.split("#")[0]
            number_strings = line_without_comment.strip().split(",")

            for number in number_strings:
                numbers.append(int(number.strip()))

    return numbers


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
    instruction_string = str(instruction)
    opcode = int(instruction_string[-2:])

    parameter_modes = list(instruction_string[:-2][::-1])

    for index in range(len(parameter_modes)):
        parameter_modes[index] = int(parameter_modes[index])

    while len(parameter_modes) < 3:
        parameter_modes.append(0)

    return opcode, parameter_modes


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    opcode, parameter_modes = decode(memory[position])
    mode = parameter_modes[n - 1]

    if mode == 1:
        return memory[position + n]
    elif mode == 0:
        return memory[memory[position + n]]
    else:
        raise ValueError(f"Unknown parameter mode {mode}")


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    Opcode 3 raises a ValueError if no input is available.
    """
    opcode, parameter_modes = decode(memory[position])

    next_position_1_or_2 = position + 4
    next_position_3_or_4 = position + 2
    next_position_5_or_6 = position + 3

    match opcode:
        case 99:
            return None

        case 1:
            result = parameter(memory, position, 1) + parameter(memory, position, 2)
            memory[memory[position + 3]] = result
            return next_position_1_or_2

        case 2:
            result = parameter(memory, position, 1) * parameter(memory, position, 2)
            memory[memory[position + 3]] = result
            return next_position_1_or_2

        case 3:
            if not inputs:
                raise ValueError("Opcode 3 requires an input, but inputs is empty")

            input_value = inputs.pop(0)

            if parameter_modes[0] == 0:
                memory[memory[position + 1]] = input_value
            else:
                memory[position + 1] = input_value

            return next_position_3_or_4

        case 4:
            outputs.append(parameter(memory, position, 1))
            return next_position_3_or_4

        case 5:
            if parameter(memory, position, 1) != 0:
                return parameter(memory, position, 2)

            return next_position_5_or_6

        case 6:
            if parameter(memory, position, 1) == 0:
                return parameter(memory, position, 2)

            return next_position_5_or_6

        case 7:
            if parameter(memory, position, 1) < parameter(memory, position, 2):
                memory[memory[position + 3]] = 1
            else:
                memory[memory[position + 3]] = 0

            return next_position_1_or_2

        case 8:
            if parameter(memory, position, 1) == parameter(memory, position, 2):
                memory[memory[position + 3]] = 1
            else:
                memory[memory[position + 3]] = 0

            return next_position_1_or_2

        case _:
            raise ValueError(f"Unknown opcode {opcode} at position {position}")


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    remaining_inputs = inputs.copy()
    position = 0
    outputs = []

    while position is not None:
        position = step(memory, position, remaining_inputs, outputs)

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
