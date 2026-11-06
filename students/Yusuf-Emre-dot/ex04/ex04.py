# Exercise 04. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

"""debug review wenn hinter den kommentar ein , steckt kann es fehler geben
5 5 zu 55
"""

# tests mit
# print(delete_coms(("#lo,4\n3,3,4#lol"))) print(parse_program("#lo,4\n3,3,4#lol444"))
from pathlib import Path
from functools import partial

# The program file sits next to this file, wherever you run Python from (see README.md).
PROGRAM_FILE = Path(__file__).parent / "diagnostic.txt"
# Reads two numbers and outputs the larger one (see README.md, Part 2).
MAX_OF_TWO = [3, 20, 3, 21, 7, 20, 21, 22, 1005, 22, 14, 4, 20, 99, 4, 21, 99, 0, 0, 0, 0, 0, 0]


# ---------------------------------------------------------------- Part 1 (in class)
def delete_coms(text):
    anzahl = text.count("#")
    for i in range(anzahl):
        a = text.find("#")
        b = text.find("\n", a)
        if b != -1:
            text = text[:a] + text[b:]
        else:
            text = text[:a]
    return text


def parse_program(text):
    L = []
    text = text.replace(" ", "")  # Leerzeichen wegmachen
    text = delete_coms(text)  # macht alle kommentare weg bevor die kommas gewertet werden
    text = text.replace("\n", ",")  # ersetzt es mit , damit sie alle getrennt werden
    text = text.split(",")  # trennt alles
    for i in text:
        try:
            L += [int(i)]
        except ValueError:
            pass
    return L


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
    text = str(instruction)
    # Fügt so viele Nullen wie es net zu 10_000 hat
    text = "0" * (5 - len(text)) + text
    return int(text[-2] + text[-1]), [int(text[i]) for i in range(2, -1, -1)]


def parameter(memory, position, n):
    """Return the value of the n-th parameter (1, 2 or 3) of the instruction at `position`.

    Mode 0 (position mode): the value at the address the parameter holds.
    Mode 1 (immediate mode): the parameter itself.
    Any other mode raises a ValueError.
    """
    mode = decode(memory[position])[1][n - 1]
    # nimmt nur die Liste und der index ist -n weil sie von rechts zu links gelesen wird
    if mode == 1:
        return memory[position + n]
    return memory[memory[position + n]]


def step(memory, position, inputs, outputs):
    """Execute the instruction that starts at `position` in memory.

    Opcode 3 takes the first number out of `inputs` Wenn Input leer ist gibt es IndexError;
    opcode 4 appends a number to `outputs`.
    Return the position of the next instruction, or None if the opcode is 99.
    An unknown opcode raises a ValueError.

    """
    wert = partial(parameter, memory, position)
    # partial ist eine Funktion wo ich eine vorhandene Funktion eingebe und dann bestimmte parameter vordefiniere
    # dann muss ich nicht immer parameter(memory,position,1) schreiebn sondern nur wert(1)
    opcode, mode = decode(memory[position])
    match opcode:
        case 1:
            memory[memory[position + 3]] = wert(1) + wert(2)
            return position + 4
        case 2:
            memory[memory[position + 3]] = wert(1) * wert(2)
            return position + 4
        case 3:
            if inputs == []:
                raise IndexError(
                    f"Du rufst in Position {position} Opcode 3 auf, ohne in Input zu schreiben."
                )
            memory[memory[position + 1]] = inputs[0]
            inputs.pop(0)
            return position + 2
        case 4:
            outputs.append(wert(1))
            return position + 2

        case 5:  # jump if True
            if wert(1) != 0:
                return wert(2)
            return position + 3

        case 6:  # jump if False
            if wert(1) == 0:
                return wert(2)
            return position + 3

        case 7:  # less than
            memory[memory[position + 3]] = int(wert(1) < wert(2))
            # Falls die Bedingung True ist, macht int() es zu 1 sonst 0
            return position + 4
        case 8:
            memory[memory[position + 3]] = int(wert(1) == wert(2))
            # Falls die Bedingung True ist, macht int() es zu 1 sonst 0
            return position + 4
        case 99:
            return None
        case _:
            raise ValueError(f"In Position {position} ist ein nicht definierter Oppcode {opcode}")


def run(memory, inputs):
    """Execute instructions, starting at position 0, until the program halts.

    `inputs` is the list of numbers the program reads, in order. `inputs` itself must not
    change. Return the list of numbers the program output.
    """
    output = []
    inp = inputs.copy()
    position = step(memory, 0, inp, output)
    while position is not None:
        position = step(memory, position, inp, output)
    return output


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print(delete_coms("4#3,4\n\n3 4\n"))
    program = load_program(PROGRAM_FILE)
    print("Part 1")
    print("1:", run([3, 0, 4, 0, 99], [42]))
    print("2:", run(program.copy(), [1]))

    print("Part 2")
    print("3:", run(MAX_OF_TWO.copy(), [17, 4]))
    print("4:", run(program.copy(), [5]))
