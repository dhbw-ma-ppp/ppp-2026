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
        self.program = list(program)
        self.pos = 0
        self.base = 0
        self.inputs = []
        self.halted = False

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        self.inputs.extend(inputs)
        outputs = []

        while self.pos is not None:
            opcode, _ = decode(self.program[self.pos])
            if opcode == 3 and not self.inputs:
                break
            self.pos, self.base = step(self.program, self.pos, self.inputs, outputs, self.base)

        self.halted = self.pos is None
        return outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    count = 0

    for i in range(0, len(outputs), 3):
        if outputs[i + 2] == tile and outputs[i] != -1:
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

    def update(self, outputs: list):
        for x in range(0, len(outputs), 3):
            y = x + 1
            tile = x + 2
            ot = outputs[tile]
            ox = outputs[x]
            oy = outputs[y]
            if ox != -1:
                coordinates = (ox, oy)
                self.tiles[coordinates] = ot
                if ot == PADDLE:
                    self.paddle = (ox, oy)
                elif ot == BALL:
                    self.ball = (ox, oy)
            else:
                self.score = ot
        self.scores.append(self.score)

    def count(self, tile: int):
        count = 0
        for tile_type in self.tiles.values():
            if tile_type == tile:
                count = count + 1

        return count


def screen_rows(game) -> list[list[int]]:
    if not game.tiles:
        return []
    width = max(x for x, y in game.tiles) + 1
    height = max(y for x, y in game.tiles) + 1
    rows = [[] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            rows[y].append(game.tiles.get((x, y)))

    return rows


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    returnList = []
    for row in screen_rows(game):
        for tile in row:
            returnList.append(SYMBOLS[tile])

        returnList.append("\n")

    returnList.pop()

    return "".join(returnList)


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
        ball_pos = game.ball[0]
        paddle_pos = game.paddle[0]

        if ball_pos > paddle_pos:
            return 1
        elif ball_pos < paddle_pos:
            return -1
        else:
            return 0


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    comp = Computer(program)
    game = Game()
    out = comp.run([])
    game.update(out)

    while not comp.halted:
        choice = controller.choose(game)
        out = comp.run([choice])
        game.update(out)

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
