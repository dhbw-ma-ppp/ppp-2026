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
        self.programCopy = program.copy()
        self.halted = False
        self.inputs = []
        self.index = 0
        self.relative_base = 0

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        self.inputs = inputs.copy()

        outputs = []

        while self.index is not None:
            opcode = decode(self.programCopy[self.index])[0]
            if opcode == 99:
                self.halted = True
                break
            if self.inputs == [] and opcode == 3:
                break
            self.index, self.relative_base = step(
                self.programCopy, self.index, self.inputs, outputs, self.relative_base
            )

        return outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    counter = 0

    for i in range(0, len(outputs), 3):
        if outputs[i] == -1:
            continue
        if outputs[i + 2] == tile:
            counter += 1
    return counter


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).
@dataclass
class Game:
    tiles: dict[tuple[int, int], int] = field(default_factory=dict)
    score: int = 0
    scores: list[int] = field(default_factory=list)
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None

    def update(self, outputs: list[int]) -> None:
        """Apply the computer's outputs to the game."""
        for i in range(0, len(outputs), 3):
            x, y, value = outputs[i : i + 3]

            if (x, y) == (-1, 0):
                self.score = value
            else:
                self.tiles[(x, y)] = value

                if value == 4:
                    self.ball = (x, y)
                elif value == 3:
                    self.paddle = (x, y)

        self.scores.append(self.score)

    def count(self, tile: int) -> int:
        """Count how many positions contain a particular tile."""
        return sum(1 for value in self.tiles.values() if value == tile)


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    if not game.tiles:
        return []

    width = max(x for x, y in game.tiles) + 1
    height = max(y for x, y in game.tiles) + 1

    rows = [[0 for _ in range(width)] for _ in range(height)]

    for (x, y), tile in game.tiles.items():
        rows[y][x] = tile

    return rows


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    return "\n".join("".join(SYMBOLS[tile] for tile in row) for row in screen_rows(game))


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
        if game.ball is None or game.paddle is None:
            return 0

        ball_x = game.ball[0]
        paddle_x = game.paddle[0]

        if ball_x < paddle_x:
            return -1
        elif ball_x > paddle_x:
            return 1
        else:
            return 0


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    computer = Computer(program)
    game = Game()

    outputs = computer.run([])

    while True:
        game.update(outputs)

        if computer.halted:
            break

        joystick = controller.choose(game)
        outputs = computer.run([joystick])

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
