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
        self.inputs = []
        self.position = 0
        self.halted = False
        self.base = 0

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        for i in inputs:
            self.inputs.append(i)
        outputs = []
        while not self.halted:
            opcode = decode(self.program[self.position])[0]
            if opcode == 3 and len(self.inputs) == 0:
                break
            pos, rel = step(self.program, self.position, self.inputs, outputs, self.base)
            if pos is None:
                self.halted = True
            else:
                self.position = pos
                self.base = rel
        return outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    count = 0
    for i in range(0, len(outputs), 3):
        x = outputs[i]
        y = outputs[i + 1]
        t = outputs[i + 2]
        if x == -1 and y == 0:
            continue
        if t == tile:
            count += 1
    return count


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).
@dataclass
class Game:
    tiles: dict[tuple[int, int], int] = field(default_factory=dict)
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None
    score: int = 0
    scores: list[int] = field(default_factory=list)

    def update(self, outputs: list[int]) -> None:
        self.scores.append(0)
        for i in range(0, len(outputs), 3):
            x = outputs[i]
            y = outputs[i + 1]
            t = outputs[i + 2]
            if x == -1 and y == 0:
                self.score = t
                self.scores[-1] += self.score
            else:
                self.tiles[(x, y)] = t
                if t == BALL:
                    self.ball = (x, y)
                elif t == PADDLE:
                    self.paddle = (x, y)

    def count(self, tile):
        count = 0
        for value in self.tiles.values():
            if value == tile:
                count += 1
        return count


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    xMax, yMax = max(x for x, y in game.tiles), max(y for x, y in game.tiles)
    reihen = []
    for y in range(yMax + 1):
        row = []
        for x in range(xMax + 1):
            row.append(0)
        reihen.append(row)
    for (x, y), tile in game.tiles.items():
        reihen[y][x] = tile
    return reihen


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    reihen = screen_rows(game)
    zeilen = ""
    for reihe in reihen:
        for i in reihe:
            zeilen += SYMBOLS[i]
        zeilen += "\n"
    zeilen = zeilen[:-1]
    return zeilen


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

        if game.paddle[0] < game.ball[0]:
            return 1
        elif game.ball[0] < game.paddle[0]:
            return -1
        else:
            return 0


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    game = Game()
    computer = Computer(program)
    outputs = computer.run([])
    game.update(outputs)
    while not computer.halted:
        joystick = controller.choose(game)
        outputs = computer.run([joystick])
        game.update(outputs)
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
