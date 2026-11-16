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
    program = []

    for line in text.splitlines():
        command_line = line.split("#")[0]

        for number in command_line.split(","):
            try:
                program.append(int(number))
            except ValueError:
                continue

    return program


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    with open(path) as program:
        return parse_program(program.read())


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    reversed_string_opcode = str(instruction)[::-1]

    instruction_list = []

    for index in range(2, len(reversed_string_opcode)):
        instruction_list.append(int(reversed_string_opcode[index]))

    while len(instruction_list) < 3:
        instruction_list.append(0)

    opcode_decoded = (int(reversed_string_opcode[:2:][::-1]), instruction_list)

    return opcode_decoded


def parameter(memory, position, n, relative_base=0):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Mode 2 (relative mode)
    Any other mode raises a ValueError.
    """
    if position < 0:
        raise IndexError(f"Can't access negative index {n} at position {position}.")
    modes_of_parameters = decode(read(memory, position))[1]

    argument = read(memory, position + n)

    match modes_of_parameters[n - 1]:
        case 0:
            return read(memory, argument)
        case 1:
            return argument
        case 2:
            return read(memory, relative_base + argument)
        case _:
            raise ValueError(
                f"{modes_of_parameters[n - 1]} is not a valid parameter. Only 0, 1 and 2 are valid."
            )


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.

    Trying to read from empty inputs or trying to jump to a negative index results in an IndexError.
    """
    opcode = decode(read(memory, position))[0]

    if opcode == 99:
        return None

    # opcodes with no additional parameters

    if opcode == 3:
        if inputs == []:
            raise IndexError(
                f"Can't read from inputs at position {position + 1} as inputs are emtpy."
            )
        target = read(memory, position + 1)
        write(memory, target, inputs.pop(0))
        return position + 2

    first_parameter = parameter(memory, position, 1)

    if opcode == 4:
        outputs.append(first_parameter)
        return position + 2

    if opcode == 6:
        if first_parameter == 0:
            target = parameter(memory, position, 2)
            if target < 0:
                raise IndexError(f"Can't access negative index {target} at position {position}.")
            return target
        return position + 3

    second_parameter = parameter(memory, position, 2)

    # opcodes with 2 parameters

    if opcode == 1:
        target = read(memory, position + 3)
        write(memory, target, first_parameter + second_parameter)
        return position + 4

    if opcode == 2:
        target = read(memory, position + 3)
        write(memory, target, first_parameter * second_parameter)
        return position + 4

    if opcode == 5:
        if first_parameter != 0:
            target = parameter(memory, position, 2)
            if target < 0:
                raise IndexError(f"Can't access negative index {target} at position {position}.")
            return target
        return position + 3

    if opcode == 7:
        if first_parameter < second_parameter:
            write(memory, read(memory, position + 3), 1)
        else:
            write(memory, read(memory, position + 3), 0)
        return position + 4

    if opcode == 8:
        if first_parameter == second_parameter:
            write(memory, read(memory, position + 3), 1)
        else:
            write(memory, read(memory, position + 3), 0)
        return position + 4

    raise ValueError(f"Opcode {opcode} at position {position} is not valid.")


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    index = 0

    working_inputs = inputs.copy()
    outputs = []

    while index is not None:
        index = step(memory, index, working_inputs, outputs)

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


# ---------------------------------------------------------------- Bonus
def run_bonus(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    index = 0

    # relative_base_list is mutable and can therefore be globally changed, unlike an integer
    relative_base = [0]

    working_inputs = inputs.copy()
    outputs = []

    while index is not None:
        index = step_bonus(memory, index, working_inputs, outputs, relative_base)

    return outputs


def write(memory, index, value):
    if index < 0:
        raise IndexError(f"Can't acces negative index {index}")

    missing = index - len(memory) + 1

    if missing > 0:
        memory.extend([0] * missing)

    memory[index] = value


def read(memory, index):
    if index < 0:
        raise IndexError(f"Can't acces negative index {index}")

    if index >= len(memory):
        return 0

    return memory[index]


def step_bonus(memory, position, inputs, outputs, relative_base):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.

    Trying to read from empty inputs or trying to jump to a negative index results in an IndexError.
    """
    opcode, modes = decode(read(memory, position))

    match opcode:
        case 99:
            return None
        case 1:
            first_parameter = parameter(memory, position, 1, relative_base[0])
            second_parameter = parameter(memory, position, 2, relative_base[0])
            target = read(memory, position + 3)
            if modes[2] == 2:
                target += relative_base[0]
            write(memory, target, first_parameter + second_parameter)
            return position + 4
        case 2:
            first_parameter = parameter(memory, position, 1, relative_base[0])
            second_parameter = parameter(memory, position, 2, relative_base[0])
            target = read(memory, position + 3)
            if modes[2] == 2:
                target += relative_base[0]
            write(memory, target, first_parameter * second_parameter)
            return position + 4
        case 3:
            if inputs == []:
                raise IndexError(
                    f"Can't read from inputs at position {position + 1} as inputs are empty."
                )
            target = read(memory, position + 1)
            if modes[0] == 2:
                target += relative_base[0]
            write(memory, target, inputs.pop(0))
            return position + 2
        case 4:
            outputs.append(parameter(memory, position, 1, relative_base[0]))
            return position + 2
        case 5:
            first_parameter = parameter(memory, position, 1, relative_base[0])
            if first_parameter != 0:
                target = parameter(memory, position, 2, relative_base[0])
                if target < 0:
                    raise IndexError(
                        f"Can't access negative index {target} at position {position}."
                    )
                return target
            return position + 3
        case 6:
            first_parameter = parameter(memory, position, 1, relative_base[0])
            if first_parameter == 0:
                target = parameter(memory, position, 2, relative_base[0])
                if target < 0:
                    raise IndexError(
                        f"Can't access negative index {target} at position {position}."
                    )
                return target
            return position + 3
        case 7:
            first_parameter = parameter(memory, position, 1, relative_base[0])
            second_parameter = parameter(memory, position, 2, relative_base[0])
            target = read(memory, position + 3)
            if modes[2] == 2:
                target += relative_base[0]
            write(memory, target, 1 if first_parameter < second_parameter else 0)
            return position + 4
        case 8:
            first_parameter = parameter(memory, position, 1, relative_base[0])
            second_parameter = parameter(memory, position, 2, relative_base[0])
            target = read(memory, position + 3)
            if modes[2] == 2:
                target += relative_base[0]
            write(memory, target, 1 if first_parameter == second_parameter else 0)
            return position + 4
        case 9:
            first_parameter = parameter(memory, position, 1, relative_base[0])
            relative_base[0] += first_parameter
            return position + 2
        case _:
            raise ValueError(f"Opcode {opcode} at position {position} is not valid.")
