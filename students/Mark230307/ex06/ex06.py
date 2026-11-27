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
        self.memory = program.copy()
        self.position = 0
        self.relative_base = 0
        self.inputs = []
        self.halted = False

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        self.inputs.extend(inputs)
        outputs = []
        while not self.halted:
            opcode, rest = decode(self.memory[self.position])
            if opcode == 3 and not self.inputs:
                break
            self.position, self.relative_base = step(
                self.memory,
                self.position,
                self.inputs,
                outputs,
                self.relative_base,
            )
            self.halted = self.position is None
        return outputs


def count_tiles(outputs, tile) -> int:
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    count = 0
    for i in range(0, len(outputs), 3):
        x, y, value = outputs[i : i + 3]
        if (x, y) == (-1, 0):
            continue
        if value == tile:
            count += 1
    return count


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).
@dataclass
class Game:
    tiles: dict[tuple[int, int], int] = field(default_factory=dict)
    score: int = 0
    scores: list[int] = field(default_factory=list)
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None

    def update(self, outputs: list[int]):
        for i in range(0, len(outputs), 3):
            x, y, value = outputs[i : i + 3]
            position = (x, y)
            if position == (-1, 0):
                self.score = value
                continue
            self.tiles[position] = value
            if value == 4:
                self.ball = position
            elif value == 3:
                self.paddle = position
        self.scores.append(self.score)

    def count(self, tile: int) -> int:
        count = 0
        for value in self.tiles.values():
            if value == tile:
                count += 1
        return count


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    if not game.tiles:
        return []
    width = max(x for x, y in game.tiles) + 1
    height = max(y for x, y in game.tiles) + 1
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(game.tiles.get((x, y), 0))
        rows.append(row)
    return rows


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    text = ""
    for y, row in enumerate(screen_rows(game)):
        if y > 0:
            text += "\n"
        for tile in row:
            text += SYMBOLS[tile]
    return text


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

    def choose(self, game: Game) -> int:
        if game.ball is None or game.paddle is None:
            return 0
        ball_x = game.ball[0]
        paddle_x = game.paddle[0]
        if ball_x < paddle_x:
            return -1
        if ball_x > paddle_x:
            return 1
        return 0


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    computer = Computer(program)
    game = Game()
    outputs = computer.run([])
    game.update(outputs)
    while not computer.halted:
        move = controller.choose(game)
        outputs = computer.run([move])
        game.update(outputs)
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
