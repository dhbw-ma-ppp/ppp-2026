# A complete IntCode computer, as functions: everything from exercise 4, plus relative mode
# (mode 2), opcode 9 (adjust the relative base) and memory beyond the end of the program (the
# bonus of exercise 4). You don't need to change this file.
#
# Did the exercise 4 bonus? You may use your own functions instead: copy them into this file,
# keeping the names and what they return.


def parse_program(text):
    """Return the numbers in `text` as a list of ints.

    Numbers are separated by commas and/or line breaks; `#` starts a comment.
    """
    numbers = []
    for line in text.splitlines():
        line = line.split("#")[0]
        for part in line.split(","):
            if part.strip() != "":
                numbers.append(int(part))
    return numbers


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    with open(path, encoding="utf-8") as file:
        return parse_program(file.read())


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0])
    """
    opcode = instruction % 100
    modes = [instruction // 100 % 10, instruction // 1000 % 10, instruction // 10000 % 10]
    return opcode, modes


def read(memory, address):
    """The value at `address`; addresses beyond the end of `memory` hold 0."""
    if address < 0:
        raise ValueError(f"negative address {address}")
    if address >= len(memory):
        return 0
    return memory[address]


def write(memory, address, value):
    """Write `value` to `address`, making `memory` longer (with 0s) if needed."""
    if address < 0:
        raise ValueError(f"negative address {address}")
    if address >= len(memory):
        memory.extend([0] * (address + 1 - len(memory)))
    memory[address] = value


def address_of(memory, position, n, base):
    """The address the n-th parameter refers to, in position or relative mode."""
    _, modes = decode(memory[position])
    raw = read(memory, position + n)
    match modes[n - 1]:
        case 0:
            return raw
        case 2:
            return base + raw
        case _:
            raise ValueError(f"mode {modes[n - 1]} has no address, at position {position}")


def value_of(memory, position, n, base):
    """The value of the n-th parameter, in any of the three modes."""
    _, modes = decode(memory[position])
    if modes[n - 1] == 1:
        return read(memory, position + n)
    return read(memory, address_of(memory, position, n, base))


# What opcodes 1, 2, 7 and 8 compute from their two parameters.
OPERATIONS = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    7: lambda a, b: 1 if a < b else 0,
    8: lambda a, b: 1 if a == b else 0,
}


def step(memory, position, inputs, outputs, base):
    """Execute the instruction at `position`. Return (next position, relative base).

    The next position is None if the opcode is 99. Opcode 3 takes the first number out of
    `inputs`, and raises a ValueError if there is none; opcode 4 appends to `outputs`.
    """
    opcode, _ = decode(memory[position])
    # print(f"detected op: {opcode}")
    match opcode:
        case 1 | 2 | 7 | 8:
            a = value_of(memory, position, 1, base)
            b = value_of(memory, position, 2, base)
            write(memory, address_of(memory, position, 3, base), OPERATIONS[opcode](a, b))
            return position + 4, base
        case 3:
            if len(inputs) == 0:
                # print("op 3 and no inputs")
                raise ValueError(f"no input left at position {position}")
            write(memory, address_of(memory, position, 1, base), inputs.pop(0))
            return position + 2, base
        case 4:
            outputs.append(value_of(memory, position, 1, base))
            return position + 2, base
        case 5:
            if value_of(memory, position, 1, base) != 0:
                return value_of(memory, position, 2, base), base
            return position + 3, base
        case 6:
            if value_of(memory, position, 1, base) == 0:
                return value_of(memory, position, 2, base), base
            return position + 3, base
        case 9:
            return position + 2, base + value_of(memory, position, 1, base)
        case 99:
            return None, base
        case _:
            raise ValueError(f"unknown opcode {opcode} at position {position}")
