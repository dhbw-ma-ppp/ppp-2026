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
    ints_without_comment = []
    lines = text.splitlines()
    for line in lines:
        if first_is_number(line):
            a = line.split("#")
            a = a[0].strip().split(",")
            for number in a:
                ints_without_comment.append(int(number.strip()))
        else:
            continue
    return ints_without_comment


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    with open(path) as file:
        a = file.read()
    return parse_program(a)


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    string_instruction = str(instruction)
    if int(string_instruction[len(string_instruction) - 2 :]) == 99:
        opcode = 99
    else:
        opcode = int(string_instruction[len(string_instruction) - 2 :])
    parameters = list(string_instruction[:-2][::-1])
    for i in range(len(parameters)):
        parameters[i] = int(parameters[i])
    while len(parameters) < 3:
        parameters.append(0)
    return (opcode, parameters)


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    a = decode(memory[position])
    if a[1][n - 1] == 1:
        return memory[position + n]
    elif a[1][n - 1] == 0:
        return memory[memory[position + n]]
    else:
        raise ValueError


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    """
    a = decode(memory[position])
    opCode = a[0]
    next_instruction1and2 = position + 4
    next_instruction3and4 = position + 2
    next_instruction5and6 = position + 3
    match opCode:
        case 99:
            return None
        case 1:
            b = parameter(memory, position, 1) + parameter(memory, position, 2)
            memory[memory[position + 3]] = b
            return next_instruction1and2
        case 2:
            b = parameter(memory, position, 1) * parameter(memory, position, 2)
            memory[memory[position + 3]] = b
            return next_instruction1and2
        case 3:
            insert = inputs[0]
            inputs.pop(0)
            if decode(memory[position])[1][0] == 0:
                memory[memory[position + 1]] = insert
            else:
                memory[position + 1] = insert
            return next_instruction3and4
        case 4:
            outputs.append(parameter(memory, position, 1))
            return next_instruction3and4
        case 5:
            if parameter(memory, position, 1) != 0:
                return parameter(memory, position, 2)
            return next_instruction5and6
        case 6:
            if parameter(memory, position, 1) == 0:
                return parameter(memory, position, 2)
            return next_instruction5and6
        case 7:
            if parameter(memory, position, 1) < parameter(memory, position, 2):
                memory[memory[position + 3]] = 1
            else:
                memory[memory[position + 3]] = 0
            return next_instruction1and2
        case 8:
            if parameter(memory, position, 1) == parameter(memory, position, 2):
                memory[memory[position + 3]] = 1
            else:
                memory[memory[position + 3]] = 0
            return next_instruction1and2
        case _:
            raise ValueError(f"Unknown opcode {opCode} at position {position}")


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    a = inputs.copy()
    pos = 0
    outputs = []
    while pos is not None:
        pos = step(memory, pos, a, outputs)
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
