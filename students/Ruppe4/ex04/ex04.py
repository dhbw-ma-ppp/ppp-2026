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
    numbers = []
    for line in text.splitlines():
        line = line.split("#", 1)[0]
        for part in line.split(","):
            part = part.strip()
            if part:
                numbers.append(int(part))
    return numbers

def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    return parse_program(Path(path).read_text())


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    opcode = instruction % 100
    modes = [(instruction // 100) % 10,
             (instruction // 1000) % 10,
             (instruction // 10000) % 10]
    return opcode, modes


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    _, modes = decode(memory[position])
    mode = modes[n - 1]
    raw = memory[position + n]
    if mode == 0:
        return memory[raw]
    if mode == 1:
        return raw
    raise ValueError(f"Unknown parameter mode: {mode}")


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    """
    opcode, _ = decode(memory[position])
 
    if opcode == 1:  
        memory[memory[position + 3]] = (parameter(memory, position, 1)
                                        + parameter(memory, position, 2))
        return position + 4
    if opcode == 2:  
        memory[memory[position + 3]] = (parameter(memory, position, 1)
                                        * parameter(memory, position, 2))
        return position + 4
    if opcode == 3:  
        memory[memory[position + 1]] = inputs.pop(0)
        return position + 2
    if opcode == 4:  
        outputs.append(parameter(memory, position, 1))
        return position + 2
    if opcode == 5:  
        if parameter(memory, position, 1) != 0:
            return parameter(memory, position, 2)
        return position + 3
    if opcode == 6:  
        if parameter(memory, position, 1) == 0:
            return parameter(memory, position, 2)
        return position + 3
    if opcode == 7:  
        memory[memory[position + 3]] = int(parameter(memory, position, 1)
                                           < parameter(memory, position, 2))
        return position + 4
    if opcode == 8:  
        memory[memory[position + 3]] = int(parameter(memory, position, 1)
                                           == parameter(memory, position, 2))
        return position + 4
    if opcode == 99:  
        return None
    raise ValueError(f"Unknown opcode: {opcode}")


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    remaining = list(inputs)  
    outputs = []
    position = 0
    while position is not None:
        position = step(memory, position, remaining, outputs)
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
