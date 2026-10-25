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
    res = []
    for line in text.splitlines():
        parsed_line = line.split("#")[0].strip()
        for number in parsed_line.split(","):
            if number != "":
                res.append(int(number))
    return res


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    full_string = ""
    with open(PROGRAM_FILE, "r") as file:
        for line in file:
            full_string += line

    return parse_program(full_string)


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    opcode = instruction % 100
    instruction //= 100

    par_modes = []

    for i in range(3):
        par_modes.append(instruction % 10)
        instruction //= 10
    return opcode, par_modes


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    _, modes = decode(memory[position])  # e.g. MULTIPLY,[IMM,MEM,MEM]
    if modes[n - 1] == 0:
        return memory[memory[position + n]]
    elif modes[n - 1] == 1:
        return memory[position + n]
    raise ValueError("unknown mode" + str(modes[n - 1]))


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    """
    known_ops = [1, 2, 3, 4, 5, 6, 7, 8, 99]
    full_opcode = memory[position]
    opcode = full_opcode % 100

    if opcode not in known_ops:
        raise ValueError("unknown opcode" + str(opcode))
    next_offset = 0
    if opcode == 99:
        return None

    if opcode == 1:  # ADD
        next_offset = 4
        first = parameter(memory, position, 1)
        second = parameter(memory, position, 2)
        memory[memory[position + 3]] = first + second
    elif opcode == 2:  # MUL
        next_offset = 4
        first = parameter(memory, position, 1)
        second = parameter(memory, position, 2)
        memory[memory[position + 3]] = first * second
    elif opcode == 3:
        next_offset = 2
        memory[memory[position + 1]] = inputs.pop(0)
    elif opcode == 4:
        next_offset = 2
        _, mode = decode(full_opcode)
        if mode[0] == 0:
            outputs.append(memory[memory[position + 1]])
        else:
            outputs.append(memory[position + 1])
    elif opcode == 5:
        if parameter(memory, position, 1) != 0:
            position = parameter(memory, position, 2)  # next_offset stays 0, thats fine
        else:
            next_offset = 3
    elif opcode == 6:
        if parameter(memory, position, 1) == 0:
            position = parameter(memory, position, 2)
        else:
            next_offset = 3
    elif opcode == 7:
        next_offset = 4
        first = parameter(memory, position, 1)
        second = parameter(memory, position, 2)
        memory[memory[position + 3]] = int(first < second)
    elif opcode == 8:
        next_offset = 4
        first = parameter(memory, position, 1)
        second = parameter(memory, position, 2)
        memory[memory[position + 3]] = int(first == second)
    else:
        raise ValueError
    return position + next_offset


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    outputs = []
    position = 0
    inputs_cpy = inputs.copy()
    while position is not None:
        position = step(memory, position, inputs_cpy, outputs)
    return outputs


# ======================BONUS=================================================================
def parameter_bonus(memory, position, n,relative):
    _, modes = decode(memory[position])  # e.g. MULTIPLY,[IMM,MEM,MEM]
    if modes[n - 1] == 0:
        index = memory[position + n]
    elif modes[n - 1] == 1:
        index = position + n
    elif modes[n - 1] == 2:
        index = relative+memory[position + n]
    else:
        raise ValueError("unknown mode" + str(modes[n - 1]))

    if index < len(memory):
        return index
    else:
        memory += [0] * (index - len(memory) + 1)
        if modes[n - 1] == 2:
            return index
        if modes[n - 1] == 0:
            return index
        if modes[n - 1] == 1:
            return index
        return index

def step_bonus(memory, position, inputs, outputs, relative_base):
    known_ops = [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]
    full_opcode = memory[position]
    opcode = full_opcode % 100

    if opcode not in known_ops:
        raise ValueError("unknown opcode" + str(opcode))
    next_offset = 0
    if opcode == 99:
        return None,None

    if opcode == 1:  # ADD
        next_offset = 4
        first = memory[parameter_bonus(memory, position, 1,relative_base)]
        second = memory[parameter_bonus(memory, position, 2,relative_base)]
        index = parameter_bonus(memory, position, 3,relative_base)
        print("ADD", first, second, index)
        memory[index] = first + second

    elif opcode == 2:  # MUL
        next_offset = 4
        first = memory[parameter_bonus(memory, position, 1,relative_base)]
        second = memory[parameter_bonus(memory, position, 2,relative_base)]
        index = parameter_bonus(memory, position, 3,relative_base)
        memory[index] = first * second
    elif opcode == 3: #input
        next_offset = 2
        memory[parameter_bonus(memory, position, 1,relative_base)] = inputs.pop(0)
    elif opcode == 4: #out
        next_offset = 2
        outputs.append(memory[parameter_bonus(memory, position, 1,relative_base)])
    elif opcode == 5:#if
        if memory[parameter_bonus(memory, position, 1,relative_base)] != 0:
            position = memory[parameter_bonus(memory, position, 2,relative_base)]  # next_offset stays 0, thats fine
        else:
            next_offset = 3
    elif opcode == 6:#if
        if memory[parameter_bonus(memory, position, 1,relative_base)] == 0:
            position = memory[parameter_bonus(memory, position, 2,relative_base)]
        else:
            next_offset = 3
    elif opcode == 7:#less
        next_offset = 4
        first = memory[parameter_bonus(memory, position, 1,relative_base)]
        second = memory[parameter_bonus(memory, position, 2,relative_base)]
        memory[parameter_bonus(memory, position, 3,relative_base)] = int(first < second)
    elif opcode == 8:#equal
        next_offset = 4
        first = memory[parameter_bonus(memory, position, 1,relative_base)]
        second = memory[parameter_bonus(memory, position, 2,relative_base)]
        memory[parameter_bonus(memory, position, 3,relative_base)] = int(first == second)
    elif opcode == 9:
        next_offset = 2
        relative_base += memory[parameter_bonus(memory, position, 1,relative_base)]
    else:
        raise ValueError
    return position + next_offset,relative_base


def run_bonus(memory, inputs):
    outputs = []
    position = 0
    relative_base = 0
    inputs_cpy = inputs.copy()
    while position is not None:
        position,relative_base = step_bonus(memory, position, inputs_cpy, outputs, relative_base)
    return outputs


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    # print("Part 1")
    # print("1:", run([3, 0, 4, 0, 99], [42]))
    # print("2:", run(program.copy(), [1]))
    #
    # print("Part 2")
    # print("3:", run(MAX_OF_TWO.copy(), [17, 4]))
    # print("4:", run(program.copy(), [5]))
    print(run_bonus([4, 1000, 99], []))