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
    instructions_added = 0

    for index in range(2, len(reversed_string_opcode)):
        instruction_list.append(int(reversed_string_opcode[index]))
        instructions_added += 1

    while instructions_added < 3:
        instruction_list.append(0)
        instructions_added += 1

    opcode_decoded = (int(reversed_string_opcode[:2:][::-1]), instruction_list)

    return opcode_decoded


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    if position < 0:
        raise IndexError(f"Can't access negative index {n} at position {position}.")
    opcode, modes_of_parameters = decode(memory[position])

    argument = memory[position + n]

    match modes_of_parameters[n - 1]:
        case 0:
            return memory[argument]
        case 1:
            return argument
        case _:
            raise ValueError(
                f"{modes_of_parameters[n - 1]} is not a valid parameter. Only 0 and 1 are valid."
            )


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.

    Trying to read from empty inputs or trying to jump to a negative index results in an IndexError.
    """
    opcode, modes = decode(memory[position])

    match opcode:
        case 99:
            return None
        case 1:
            first_parameter = parameter(memory, position, 1)
            second_parameter = parameter(memory, position, 2)
            target = memory[position + 3]
            memory[target] = first_parameter + second_parameter
            return position + 4
        case 2:
            first_parameter = parameter(memory, position, 1)
            second_parameter = parameter(memory, position, 2)
            target = memory[position + 3]
            memory[target] = first_parameter * second_parameter
            return position + 4
        case 3:
            if inputs == []:
                raise IndexError(
                    f"Can't read from inputs at position {position + 1} as inputs are emtpy."
                )
            target = memory[position + 1]
            memory[target] = inputs.pop(0)
            return position + 2
        case 4:
            outputs.append(parameter(memory, position, 1))
            return position + 2
        case 5:
            first_parameter = parameter(memory, position, 1)
            if first_parameter != 0:
                target = parameter(memory, position, 2)
                if target < 0:
                    raise IndexError(
                        f"Can't access negative index {target} at position {position}."
                    )
                return target
            return position + 3
        case 6:
            first_parameter = parameter(memory, position, 1)
            if first_parameter == 0:
                target = parameter(memory, position, 2)
                if target < 0:
                    raise IndexError(
                        f"Can't access negative index {target} at position {position}."
                    )
                return target
            return position + 3
        case 7:
            first_parameter = parameter(memory, position, 1)
            second_parameter = parameter(memory, position, 2)
            if first_parameter < second_parameter:
                memory[memory[position + 3]] = 1
            else:
                memory[memory[position + 3]] = 0
            return position + 4
        case 8:
            first_parameter = parameter(memory, position, 1)
            second_parameter = parameter(memory, position, 2)
            if first_parameter == second_parameter:
                memory[memory[position + 3]] = 1
            else:
                memory[memory[position + 3]] = 0
            return position + 4
        case _:
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
