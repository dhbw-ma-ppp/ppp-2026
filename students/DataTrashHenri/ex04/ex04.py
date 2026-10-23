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
        porgramm = line.split("#")[0].strip()
        for number in porgramm.split(","):
            if number != "":
                res.append(int(number))
    return res
def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    full_string = ""
    with open(PROGRAM_FILE,"r") as file:
        for line in file:
            full_string += line

    return parse_program(full_string)


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    opcode = instruction % 100
    instruction//=100

    par_modes = []

    for i in range(3):
        par_modes.append(instruction%10)
        instruction//=10
    return opcode,par_modes

def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    _,modes = decode(memory[position]) # e.g. MULTIPLY,[IMM,MEM,MEM]
    if modes[n-1] == 0:#TODO EMPTY 0
        return memory[memory[position+n]]
    return memory[position+n]


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    """
    known_ops = [1,2,3,4,99]
    full_opcode = memory[position]
    opcode = full_opcode%100
    print(f"OPCODE {opcode}")
    if opcode not in known_ops:
        raise ValueError
    if opcode == 1:#ADD
        first = parameter(memory, position, 1)
        second = parameter(memory, position, 2)
        memory[parameter(memory, position, 3)] = first + second
    elif opcode == 2:#MUL
        first = parameter(memory, position, 1)
        second = parameter(memory, position, 2)
        print(f"first {first}, second {second}")
        print(f"write to index {parameter(memory, position, 3)}")
        memory[parameter(memory, position, 3)] = first * second

    return position + 4


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    pass  # replace this line with your code


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
    memory = [1002, 4, 3, 4, 33]
    step(memory,0,[],[])
