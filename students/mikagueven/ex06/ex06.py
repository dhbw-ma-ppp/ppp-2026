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
        self.input_list = []
        self.position = 0
        self.relative_base = 0
        self.halted = False

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        for i in inputs:
            self.input_list.append(i)

        output = []
        while not self.halted:
            try:
                pos, rel = step(
                    self.program, self.position, self.input_list, output, self.relative_base
                )
            except ValueError:
                break
            self.relative_base = rel
            if pos is None:
                self.halted = True
            else:
                self.position = pos
        return output


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
    score: int = 0
    scores: list[int] = field(default_factory=list)
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None

    def update(self, outputs: list[int]) -> None:
        for i in range(0, len(outputs), 3):
            x = outputs[i]
            y = outputs[i + 1]
            t = outputs[i + 2]
            if x == -1 and y == 0:
                self.score = t
            else:
                self.tiles[(x, y)] = t
                if t == 3:
                    self.paddle = (x, y)
                elif t == 4:
                    self.ball = (x, y)
        self.scores.append(self.score)

    def count(self, tile: int) -> int:
        count = 0
        for value in self.tiles.values():
            if value == tile:
                count += 1
        return count


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    max_x = max(x for x, y in game.tiles)
    max_y = max(y for x, y in game.tiles)
    rows = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            row.append(0)
        rows.append(row)
    for (x, y), tile in game.tiles.items():
        rows[y][x] = tile
    return rows


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    rows = screen_rows(game)
    lines = []
    for row in rows:
        line = ""
        for tile in row:
            line += SYMBOLS[tile]
        lines.append(line)
    return "\n".join(lines)


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
