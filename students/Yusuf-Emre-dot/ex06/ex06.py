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
        self.pos = 0
        self.inputs = []
        self.base = 0

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        outputs = []
        if not self.halted:
            self.inputs += inputs
            while self.pos is not None and not (
                decode(self.program[self.pos])[0] == 3 and len(self.inputs) == 0
            ):
                self.pos, self.base = step(self.program, self.pos, self.inputs, outputs, self.base)
            if self.pos is None:
                self.halted = True
        return outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    c = 0
    for i in range(len(outputs) // 3):
        if outputs[i * 3 + 2] == tile and outputs[i * 3] != -1:
            c += 1

    return c


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).
@dataclass
class Game:
    tiles: dict = field(default_factory=dict)
    score: int = 0
    scores: list = field(default_factory=list)
    ball: tuple = None
    paddle: tuple = None

    def update(self, outputs):
        self.scores += [0]
        for i in range(len(outputs) // 3):
            x, y, tile = outputs[i * 3], outputs[i * 3 + 1], outputs[i * 3 + 2]
            # tile ist dann der score
            if x == -1:
                self.score = tile
                self.scores[-1] += tile

            else:
                self.tiles[(x, y)] = tile
                if tile == BALL:
                    self.ball = (x, y)
                elif tile == PADDLE:
                    self.paddle = (x, y)

    def count(self, tile):
        c = 0
        for i in self.tiles.values():
            if i == tile:
                c += 1
        return c


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    x, y = max(game.tiles.keys())[0], max(game.tiles.keys(), key=lambda value: value[1])[1]
    a = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
    for i in game.tiles.keys():
        a[i[1]][i[0]] = game.tiles[i]
    return a


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    start = ""
    L = screen_rows(game)
    for row in L:
        for item in row:
            start += SYMBOLS[item]
        start += "\n"
    start = start[:-1]
    return start


class Controller:
    """Chooses the joystick input: -1 left, 0 stay, 1 right."""

    def choose(self, game) -> int:
        raise NotImplementedError


class Stay(Controller):
    """Never moves the paddle."""

    def choose(self, game) -> int:
        return 0


class Joystick(Controller):  # Habs gemacht aus Spaß
    def choose(self, game) -> int:
        """Invalid Inputs werden wie in einem echten Game ignoriert statt einen Crash zu machen"""
        zahl = -2
        while zahl not in (-1, 0, 1):
            try:
                zahl = int(input("Chooses the joystick input: -1 left, 0 stay, 1 right :"))
            except ValueError:
                pass
        return zahl


class Autopilot(Controller):
    """Plays the game: keeps the ball in play until every block is gone."""

    def choose(self, game) -> int:
        ballpos, paddlepos = game.ball[0], game.paddle[0]
        if ballpos > paddlepos:
            return 1
        elif ballpos < paddlepos:
            return -1
        else:
            return 0


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    game = Game()
    computer = Computer(program)
    input = []
    # outputs werden generiert, gamestand wird aktualisiert und angezeigt bis das game zuende ist
    while not computer.halted:
        output = computer.run(input)
        game.update(output)
        if (
            controller.__class__.__name__ == "Controller"
        ):  # nur beim selber spielen soll es was zeichnen sonst net
            print(draw(game))
        input = [controller.choose(game)]
    return game


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", count_tiles(Computer(program).run([]), BLOCK))

    print("Part 2")
    start = Game()
    start.update(Computer(program).run([]))
    print(draw(start))
    lost = play(program, Stay())
    print("2:", lost.score)
    won = play(program, Autopilot())
    print("3:", won.score, "after", len(won.scores) - 1, "frames")
    print(draw(won))
