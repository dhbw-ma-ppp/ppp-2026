# Exercise 02. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import PROGRAM, TARGET

# ---------------------------------------------------------------- Part 1 (in class)


def step(memory, position):
    """Execute the instruction that starts at `position` in memory.

    Opcode 1 adds, opcode 2 multiplies, opcode 99 halts (see README.md).
    Return the position of the next instruction, or None if the opcode is 99.
    """
    # easily expandable opcode listing
    match memory[position]:
        # opcode 1: addition
        case 1:
            # find indecies of values to add and write into
            input_1_index = memory[position + 1]
            input_2_index = memory[position + 2]
            output_index = memory[position + 3]

            # add values at previously found indecies and writes sum into memory
            memory[output_index] = memory[input_1_index] + memory[input_2_index]

            # return position of next opcode
            return position + 4
        # opcode 2: multiplication
        case 2:
            # find indecies of values to multiply and write into
            input_1_index = memory[position + 1]
            input_2_index = memory[position + 2]
            output_index = memory[position + 3]

            # multiply values at previously found indecies and writes product into memory
            memory[output_index] = memory[input_1_index] * memory[input_2_index]

            # return position of next opcode
            return position + 4
        # opcode 99: halts
        case 99:
            return None
        # unknown opcode
        case _:
            raise ValueError("input contained unknown opcode")


def run(memory):
    """Execute instructions, starting at position 0, until the program halts.

    Return the value at position 0 after the program has halted.
    """

    # check if memory is a list
    if type(memory) is not list:
        raise TypeError("input parameter should be a list of integers")

    # check if memory is not empty
    if len(memory) == 0:
        raise ValueError("input parameter should contain at least one element")

    # check if memory only contains integers
    for i in memory:
        if type(i) is not int:
            raise TypeError("input parameter should only contain integers")

    # starting position is 0
    position = 0

    # iterates through memory
    # as long as the program doesn't receive the halt opcode
    while position is not None:
        # since step returns the position of the next opcode, set position to that value
        # executes instruction at position position in memory
        position = step(memory, position)

    # returns the value at position 0
    return memory[0]


# ---------------------------------------------------------------- Part 2 (at home)


def run_with(program, noun, verb):
    """Return the result of program with noun at position 1 and verb at position 2."""

    # check if program is a list
    if type(program) is not list:
        raise TypeError("input parameter 1 should be a list")

    # check if program is not empty
    if len(program) == 0:
        raise ValueError("input parameter 1 must be of at least length 1")

    # check if noun and verb are integers
    if type(noun) is not int or type(verb) is not int:
        raise TypeError("input parameters 2 and 3 should be of type integer.")

    # set length of program to 3 if it's less than 3
    if len(program) == 1:
        program.append(None)
    if len(program) == 2:
        program.append(None)

    # insert noun and verb into the indecies 1 and 2 of program
    program[1] = noun
    program[2] = verb

    # check if every input
    for i in program:
        if type(i) is not int:
            raise TypeError("input parameter 1 should contain integers at all indecies")

    # runs the program
    return run(program)


def find_noun_verb(program, target):
    """Return (noun, verb), each from 0 to 99, for which run_with gives target.

    Return None if there is no such pair.
    """

    return None


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print("Part 1")
    print("1:", run([2, 9, 10, 9, 1, 9, 11, 0, 99, 6, 7, 3]))
    print("2:", run(list(PROGRAM)))

    print("Part 2")
    print("3:", run_with(list(PROGRAM), 0, 0))
    print("4:", find_noun_verb(list(PROGRAM), TARGET))
