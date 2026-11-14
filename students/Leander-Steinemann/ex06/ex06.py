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

    def __init__(self, program):
        self.program = program.copy()
        self.halted = False
        self.inputs = []
        self.outputs = []
        self.base = 0
        self.next_pos = 0
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """

    def run(self, inputs):
        self.outputs = []
        for input in inputs:
            self.inputs.append(input)
        while self.next_pos is not None and not (
            decode(self.program[self.next_pos])[0] == 3 and not self.inputs
        ):
            self.next_pos, self.base = step(
                self.program, self.next_pos, self.inputs, self.outputs, self.base
            )
        if self.next_pos is None:
            self.halted = True
        return self.outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    count = 0
    for x in range(0, len(outputs), 3):
        if outputs[x + 2] == tile and outputs[x] != -1:
            count += 1
    return count


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).
@dataclass
class Game:
    tiles: dict = field(default_factory=dict)
    score: int = 0
    scores: list = field(default_factory=list)
    ball: tuple = None
    paddle: tuple = None

    def update(self, outputs: list) -> None:
        # self.tiles = {}
        # self.score = 0
        for x in range(0, len(outputs), 3):
            y = x + 1
            tile = x + 2
            if outputs[x] != -1:
                coordinates = (outputs[x], outputs[y])
                self.tiles[coordinates] = outputs[tile]
                if outputs[tile] == PADDLE:
                    self.paddle = (outputs[x], outputs[y])
                elif outputs[tile] == BALL:
                    self.ball = (outputs[x], outputs[y])
            else:
                self.score = outputs[tile]
        self.scores.append(self.score)

    def count(self, tile: int) -> int:
        count = 0
        for value_of_tile in self.tiles.values():
            if value_of_tile == tile:
                count += 1
        return count


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    rows = [[]]
    row = 0
    for (x, y), tile in game.tiles.items():
        if row != y:
            rows.append([])
            row = y
        rows[y].append(tile)
    return rows


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    screen_tile_icons = []
    for i, row in enumerate(screen_rows(game)):
        row_icons = ""
        for tile in row:
            match tile:
                case 0:
                    row_icons += " "
                case 1:
                    row_icons += "#"
                case 2:
                    row_icons += "="
                case 3:
                    row_icons += "-"
                case 4:
                    row_icons += "o"
        screen_tile_icons.append(row_icons)
    return "\n".join(screen_tile_icons)


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
        if game.ball[0] > game.paddle[0]:
            return 1
        elif game.ball[0] < game.paddle[0]:
            return -1
        else:
            return 0


def play(program: list[int], controller: Controller) -> Game:
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    comp = Computer(program)
    game = Game()
    game.update(comp.run([]))
    while comp.halted is not True:
        next_input = []
        next_input.append(controller.choose(game))
        game.update(comp.run(next_input))
    return game


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", count_tiles(Computer(program).run([]), BLOCK))

    # Part 2: uncomment once you get there.
    print("Part 2")
    start = Game()
    start.update(Computer(program).run([]))
    print(draw(start))
    lost = play(program, Stay())
    print("2:", lost.score)
    won = play(program, Autopilot())
    print("3:", won.score, "after", len(won.scores) - 1, "frames")
    print(draw(won))
