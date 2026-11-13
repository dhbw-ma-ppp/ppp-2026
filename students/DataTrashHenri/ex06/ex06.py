# Exercise 06. See README.md for the full task.
# Replace each `pass` line with your code.

from dataclasses import dataclass, field  # noqa: F401  (you'll need `field` in Part 2)
from pathlib import Path

from intcode import decode, load_program, step  # noqa: F401

PROGRAM_FILE = Path(__file__).parent / "breakout.txt"

EMPTY, WALL, BLOCK, PADDLE, BALL = 0, 1, 2, 3, 4

# How draw() shows each tile.
SYMBOLS = {EMPTY: " ", WALL: "#", BLOCK: "=", PADDLE: "-", BALL: "o"}

# Reads a number, adds it to a running total, outputs the total; forever.
RUNNING_TOTAL = [3, 13, 1, 12, 13, 12, 4, 12, 1105, 1, 0, 0, 0, 0]

# A tiny "game" for testing play(): a paddle at (0, 0), a ball at (5, 0), then three frames.
# Each frame reads the joystick and adds it to the score.
TINY_GAME = [
    104, 0, 104, 0, 104, 3,
    104, 5, 104, 0, 104, 4,
    104, -1, 104, 0, 104, 0,
    3, 40, 1, 41, 40, 41, 104, -1, 104, 0, 4, 41, 1001, 42, -1, 42, 1005, 42, 18, 99,
    0, 0, 0, 0, 3,
]  # fmt: skip

# ---------------------------------------------------------------- Part 1 (in class)


class Computer:
    """An IntCode computer that can pause when it needs input, and carry on later."""

    own_program = []
    input_list = []
    position = 0
    relative_base = 0
    halted = False
    needs_input = False

    def __init__(self, program):
        self.own_program = program.copy()
        print(self.own_program)
        pass  # replace this line with your code

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        if len(inputs) != 0 and self.needs_input:
            self.needs_input = False
        self.input_list.extend(inputs)
        output = []
        while not self.halted and not self.needs_input:
            try:
                pos, rel = step(
                    self.own_program, self.position, self.input_list, output, self.relative_base
                )
                print(pos, rel)
            except ValueError:
                # input needed
                print("value Error")
                self.needs_input = True
            else:
                # input sufficient
                self.relative_base = rel
                if pos is not None:
                    self.position = pos
                else:  # finished
                    self.halted = True
                print(self.position, self.relative_base)
        return output


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    counter = 0
    for i in range(len(outputs) // 3):
        cur_tuple = i * 3
        if outputs[cur_tuple + 2] == tile and outputs[cur_tuple] != -1:
            counter += 1
    return counter


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    pass  # replace this line with your code


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    pass  # replace this line with your code


class Controller:
    """Chooses the joystick input: -1 left, 0 stay, 1 right."""

    def choose(self, game) -> int:
        raise NotImplementedError


class Stay(Controller):
    """Never moves the paddle."""

    def choose(self, game) -> int:
        return 0


class Autopilot(Controller):
    """Plays the game: keeps the ball in play until every block is gone."""

    def choose(self, game) -> int:
        pass  # replace this line with your code


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    pass  # replace this line with your code


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", count_tiles(Computer(program).run([]), BLOCK))

    # Part 2: uncomment once you get there.
    # print("Part 2")
    # start = Game()
    # start.update(Computer(program).run([]))
    # print(draw(start))
    # lost = play(program, Stay())
    # print("2:", lost.score)
    # won = play(program, Autopilot())
    # print("3:", won.score, "after", len(won.scores) - 1, "frames")
    # print(draw(won))
