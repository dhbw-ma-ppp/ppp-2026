# Exercise 04. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path

from IPython.terminal.shortcuts import next_history_or_next_completion

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
    textlines = text.split("\n")
    input = []
    for line in textlines:
        line_without_comments = line.split("#")[0]
        inputs_strings = line_without_comments.split(",")
        for string in inputs_strings:
            if len(string.split()) > 0:
                 #if string.split()[0].isdigit() is True or int(string.split()[0]) is True:
                try:
                    input.append(int(string.split()[0]))
                except ValueError:
                    continue
                    input.append(int(string.split()[0]))


    return input
print(parse_program(" 1101, 100, -1, 4, 0 "))
    # with open("students\maxwotschke\ex04\diagnostic.txt") as input_file:
    #     inputs_raw = (input_file.read())
    #
    # inputs_without_comments = inputs_raw.split("#")[0]
    # inputs = inputs_without_comments.split()
    # return inputs
    # pos = 0
    # commands = inputs[pos]
    #
    # if len(commands) == 1:
    #     opcode = "0" + commands
    #
    # elif len(commands) > 1:
    #     opcode = commands[-2:]
    #
    # else:
    #     raise ValueError
    #
    # while opcode != "99":
    #     return inputs
    #
    # attribute_1 = inputs[pos + 1]
    #
    # if opcode == "01" or opcode == "02":
    #     attribute_2 = inputs[pos + 2]
    #     attribute_3 = inputs[pos + 3]
    #
    #     if opcode == "01":








def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    with open(path) as input_file:
        inputs= (input_file.read())

       # inputs.append(parse_program(line))

    return parse_program(inputs)




def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """

    parameters = []

    if (instruction % 100 == 99 or instruction % 100 == 1 or instruction % 100 == 2 or instruction % 100 == 3 or instruction % 100 == 4):

        opcode = instruction % 100
        instruction = instruction // 100
        parameter1 = instruction % 10
        instruction_copied = instruction // 10
        parameter2 = instruction_copied % 10
        instruction_copied = instruction_copied //10
        parameter3 = instruction_copied % 10
        return (opcode, [parameter1, parameter2, parameter3])







        # if len(str(instruction))  <= 2:
        #     parameters = [0, 0, 0]
        # elif len(str(instruction)) == 3:
        #     parameters = [1, 0, 0]
        # elif len(str(instruction)) == 4:
        #     parameters = [instruction[-3], 1, 0]
        # elif len(str(instruction)) == 5:
        #     parameters = [instruction[-3], instruction[-4], 1]
        #
        # return instruction % 100, parameters

    # elif instruction % 100 == 3 or instruction % 100 == 4:
    #     if len(str(instruction)) <= 2:
    #         parameters = [0]
    #     elif len(str(instruction)) == 4:
    #         parameters = [1]
    #     return instruction % 100, parameters





    # def describe(command):
    #     match command:
    #         case "start":
    #             return "starting"
    #         case "stop" | "halt":
    #             return "stopping"
    #         case _:
    #             return "unknown command: " + command


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """

    decoded_memory = decode(memory[position])
    parameters = decoded_memory[1]
    #return parameters,parameters[n-1]
    if parameters[n-1] == 1:
        return memory[position+n]
    elif parameters[n-1] == 0:
        return memory[memory[position+n]]
    else:
        raise ValueError


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    """
    memory_copied = memory.copy()
    opcode = decode(memory)[0]

    if opcode == 2:
        memory_copied[parameter(memory_copied, position, 3)] = parameter(memory_copied, position, 1) * parameter(memory_copied, position, 2)
    elif opcode == 1:
        memory_copied[parameter(memory_copied, position, 3)] = parameter(memory_copied, position, 1) + parameter(memory_copied, position, 2)
    elif opcode == 4:
        outputs.append(parameter(memory_copied, position, 1))
    elif opcode == 3:
        memory_copied[parameter(memory_copied, position, 1)] = inputs[0]
        if len(inputs) >= 1:
            inputs = inputs[1:]
    return memory_copied



def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    pass  # replace this line with your code


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", run([3, 0, 4, 0, 99], [42]))
    print("2:", run(program.copy(), [1]))

    print("Part 2")
    print("3:", run(MAX_OF_TWO.copy(), [17, 4]))
    print("4:", run(program.copy(), [5]))
