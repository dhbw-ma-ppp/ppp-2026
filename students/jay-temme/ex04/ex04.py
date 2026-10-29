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
    # initializes the program list
    program = list()

    # iterates over each line in text
    for line in text.split("\n"):
        # removes any potential comments from the line
        line_no_comment = line.split("#")[0]

        # splits the line into individual numbers
        line_no_comment_list = line_no_comment.split(",")

        # iterates over each number
        for number_string in line_no_comment_list:
            if number_string == "":
                continue
            try:
                # adds the number to program
                program.append(int(number_string))

            # if there is any invalid characters in text they'll be caught here
            except ValueError:
                raise ValueError("text contains invalid characters")

    return program


def load_program(path):
    """Read the file at `path` and return the program in it as a list of ints."""
    # opens the file at path
    with open(path) as file:
        # parses the file into program
        program = parse_program(file.read())

    return program


def decode(instruction):
    """Split an instruction into its opcode and the modes of its three parameters.

    decode(1002) == (2, [0, 1, 0]): opcode 2; first parameter in position mode, second in
    immediate mode, third in position mode.
    """
    # determine the opcode
    opcode = instruction % 100

    # determine the modes of the parameters
    mode_1 = (instruction // 100) % 10
    mode_2 = (instruction // 1000) % 10
    mode_3 = (instruction // 10000) % 10

    return (opcode, [mode_1, mode_2, mode_3])


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    # check if position is an integer
    if type(position) is not int:
        raise TypeError("position must be of type integer")

    # check if memory is a list
    if type(memory) is not list:
        raise TypeError("memory must be of type list")

    # check if memory is empty
    if len(memory) == 0:
        raise ValueError("memory must be of at least length 1")

    # check if position is in bounds of memory
    if position < 0 or len(memory) <= position:
        raise ValueError("position is out of bounds of memory")

    # check if n is an integer
    if type(n) is not int:
        raise TypeError("n must be of type integer")

    # check if the instruction at position has parameters
    match memory[position] % 100:
        # addition
        case 1:
            # raise an Error if n is not 1, 2, or 3
            if n not in range(1, 4):
                raise ValueError("n is not a parameter of the instruction at position")

        # multiplication
        case 2:
            # raise an Error if n is not 1, 2, or 3
            if n not in range(1, 4):
                raise ValueError("n is not a parameter of the instruction at position")

        # read from input
        case 3:
            # raise an Error if n is not 1
            if n not in range(1, 2):
                raise ValueError("n is not a parameter of the instruction at position")

        # write to output
        case 4:
            # raise an Error if n is not 1
            if n not in range(1, 2):
                raise ValueError("n is not a parameter of the instruction at position")

        # halt
        case 99:
            # has no parameters, so raise an Error
            raise ValueError("instruction at position does not have any parameters")

        # unknown opcode
        case _:
            raise ValueError("instruction at position is an unknown opcode")

    # check if position + n is in bounds of memory
    if len(memory) <= position + n:
        raise ValueError(
            "the n-th parameter of the instruction at position is out of bounds of memory"
        )

    # check which mode the n-th parameter is in
    match (memory[position] // pow(10, 1 + n)) % 10:
        # position mode
        case 0:
            # return the value at the address that the n-th parameter of the instruction at position holds
            index = memory[position + n]
            value = memory[index]
            return value

        # immediate mode
        case 1:
            # return the value of the n-th parameter of the instruction at position
            value = memory[position + n]
            return value

        # raise an Error if the mode is unknown
        case _:
            raise ValueError(
                "the n-th parameter of the instruction at position is in an invalid mode"
            )


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs`; opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.
    Trying to read from inputs when inputs is empty raises a ValueError.
    """
    # check if position is an integer
    if type(position) is not int:
        raise TypeError("position must be of type integer")

    # check if memory is a list
    if type(memory) is not list:
        raise TypeError("memory must be of type list")

    # check if memory only contains integers
    for i in memory:
        if type(i) is not int:
            raise TypeError("memory must only contain integers")

    # check if memory is empty
    if len(memory) == 0:
        raise ValueError("memory must be of at least length 1")

    # check if position is in bounds of memory
    if position < 0 or len(memory) <= position:
        raise ValueError("position is out of bounds of memory")

    # check if memory is a list
    if type(inputs) is not list:
        raise TypeError("inputs must be of type list")

    # check if memory only contains integers
    for i in inputs:
        if type(i) is not int:
            raise TypeError("inputs must only contain integers")

    # helper function to determine the indecies used by instructions
    def helper_determine_indecies(instruction, output_indecies=[]):
        """determines the inputs of the instruction in memory that starts at position."""
        # check if there are too many modes for the number of parameters
        if instruction[0] // pow(10, 1 + len(instruction)) != 0:
            raise ValueError("instruction specifies too many modes")

        # list to hold the indecies used by the instruction
        instruction_indecies = list()

        # iterate over each parameter of the instruction
        for i in range(1, len(instruction)):
            # determine the mode of the parameter
            mode = instruction[0] // pow(10, 1 + i) % 10

            # check if the parameter is in an invalid mode
            if i in output_indecies and mode not in [0]:
                raise ValueError("instruction has invalid mode for one of its parameters")

            # determine the index in memory of the value to use
            match mode:
                # position mode
                case 0:
                    # index in memory is stored in position + i
                    index = memory[position + i]
                    instruction_indecies.append(index)

                    # check if index is in bounds of memory
                    if index < 0 or len(memory) <= index:
                        raise ValueError(
                            "parameter points to an index that is out of bounds of memory"
                        )

                # immediate mode
                case 1:
                    # index in memory is position + i
                    index = position + i
                    instruction_indecies.append(index)

                # unknown mode
                case _:
                    raise ValueError("instruction contains unknown mode")

        return instruction_indecies

    # easily expandable opcode listing
    match memory[position] % 100:
        # opcode 1: addition
        case 1:
            # check if enough following indecies exist
            if len(memory) < position + 4:
                raise IndexError("memory is not large enough or contains wrong opcode")

            # determine the indecies used by the operation
            indecies = helper_determine_indecies(memory[position : position + 4], [3])

            # execute the operation
            memory[indecies[2]] = memory[indecies[0]] + memory[indecies[1]]

            # return position of next opcode
            return position + 4

        # opcode 2: multiplication
        case 2:
            # check if enough following indecies exist
            if len(memory) < position + 4:
                raise IndexError("memory is not large enough or contains wrong opcode")

            # determine the indecies used by the operation
            indecies = helper_determine_indecies(memory[position : position + 4], [3])

            # execute the operation
            memory[indecies[2]] = memory[indecies[0]] * memory[indecies[1]]

            # return position of next opcode
            return position + 4

        # opcode 3: read from inputs
        case 3:
            # check if enough following indecies exist
            if len(memory) < position + 2:
                raise IndexError("memory is not large enough or contains wrong opcode")

            if len(inputs) == 0:
                raise ValueError("inputs is empty, no more inputs can be read")

            # determine the indecies used by the operation
            indecies = helper_determine_indecies(memory[position : position + 2], [1])

            # execute the operation
            memory[indecies[0]] = inputs[0]

            # remove the number used in the operation from inputs
            inputs.remove(inputs[0])

            # return position of next opcode
            return position + 2

        # opcode 4: write into outputs
        case 4:
            # check if enough following indecies exist
            if len(memory) < position + 2:
                raise IndexError("memory is not large enough or contains wrong opcode")

            # determine the indecies used by the operation
            indecies = helper_determine_indecies(memory[position : position + 2])

            # execute the operation
            outputs.append(memory[indecies[0]])

            # return position of next opcode
            return position + 2

        # opcode 5: jump-if-true
        case 5:
            # check if enough following indecies exist
            if len(memory) < position + 3:
                raise IndexError("memory is not large enough or contains wrong opcode")

            # determine the indecies used by the operation
            indecies = helper_determine_indecies(memory[position : position + 3])

            # check if the first parameter is 0
            if memory[indecies[0]] == 0:
                # return the position of the next instruction
                return position + 3
            else:
                # jump to the instruction specified by the second parameter
                return memory[indecies[1]]

        # opcode 6: jump-if-false
        case 6:
            # check if enough following indecies exist
            if len(memory) < position + 3:
                raise IndexError("memory is not large enough or contains wrong opcode")

            # determine the indecies used by the operation
            indecies = helper_determine_indecies(memory[position : position + 3])

            # check if the first parameter is 0
            if memory[indecies[0]] == 0:
                # jump to the instruction specified by the second parameter
                return memory[indecies[1]]
            else:
                # return the position of the next instruction
                return position + 3

        # opcode 7: less than
        case 7:
            # check if enough following indecies exist
            if len(memory) < position + 4:
                raise IndexError("memory is not large enough or contains wrong opcode")

            # determine the indecies used by the operation
            indecies = helper_determine_indecies(memory[position : position + 4], [3])

            # execute the operation
            if memory[indecies[0]] < memory[indecies[1]]:
                memory[indecies[2]] = 1
            else:
                memory[indecies[2]] = 0

            # return position of next opcode
            return position + 4

        # opcode 8: equals
        case 8:
            # check if enough following indecies exist
            if len(memory) < position + 4:
                raise IndexError("memory is not large enough or contains wrong opcode")

            # determine the indecies used by the operation
            indecies = helper_determine_indecies(memory[position : position + 4], [3])

            # execute the operation
            if memory[indecies[0]] == memory[indecies[1]]:
                memory[indecies[2]] = 1
            else:
                memory[indecies[2]] = 0

            # return position of next opcode
            return position + 4

        # opcode 99: halts
        case 99:
            # check for invalid modes
            helper_determine_indecies(memory[position : position + 1])

            # return None to halt the program
            return None

        # unknown opcode
        case _:
            raise ValueError(
                f"input contained unknown opcode {memory[position] % 100} at position {position}"
            )


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    # check if memory is a list
    if type(memory) is not list:
        raise TypeError("memory must be of type list")

    # check if memory is not empty
    if len(memory) == 0:
        raise ValueError("memory must be of at least length 1")

    # check if memory only contains integers
    for i in memory:
        if type(i) is not int:
            raise TypeError("memory must only contain integers")

    # check if memory is a list
    if type(inputs) is not list:
        raise TypeError("inputs must be of type list")

    # check if memory only contains integers
    for i in inputs:
        if type(i) is not int:
            raise TypeError("inputs must only contain integers")

    # use a copy of inputs to avoid changing the original\
    inputs_copy = inputs.copy()

    # list to hold all the outputs of the program
    outputs = list()

    # starting position is 0
    position = 0

    # iterates through memory
    # as long as the program doesn't receive the halt opcode
    while position is not None:
        # since step returns the position of the next opcode, set position to that value
        # executes instruction at position position in memory
        position = step(memory, position, inputs_copy, outputs)

    # returns the list of outputs
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
