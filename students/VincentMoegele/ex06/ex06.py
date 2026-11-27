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
        self.class_program = program.copy()
        self.halted = False
        self.position = 0
        self.base = 0

        self.inputs = []

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        outputs = []
        self.inputs.extend(inputs)

        while not self.halted:
            opcode, _ = decode(self.class_program[self.position])
            if opcode == 3 and len(self.inputs) == 0:
                break
            next_position, self.base = step(
                self.class_program, self.position, self.inputs, outputs, self.base
            )
            if next_position is None:
                self.halted = True
            else:
                self.position = next_position

        return outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    count = len(outputs)
    count_tile = 0
    for i in range(0, count, 3):
        x = outputs[i]
        tile_intern = outputs[i + 2]
        if x == -1:
            continue
        if tile == tile_intern:
            count_tile += 1

    return count_tile


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).


@dataclass
class Game:
    tiles: dict = field(default_factory=dict)
    score: int = 0
    scores: list[int] = field(default_factory=list[int])
    ball: tuple[int, int] = None
    paddle: tuple[int, int] = None

    def update(self, outputs: list[int]):
        count = len(outputs)
        for i in range(0, count, 3):
            x = outputs[i]
            y = outputs[i + 1]
            tile_intern = outputs[i + 2]

            if x == -1:
                self.score = tile_intern
                continue

            self.tiles[(x, y)] = tile_intern

            if tile_intern == BALL:
                self.ball = (x, y)

            if tile_intern == PADDLE:
                self.paddle = (x, y)

        self.scores.append(self.score)

    def count(self, tile: int):
        tile_counter = 0
        for key in self.tiles:
            if tile == self.tiles[key]:
                tile_counter += 1

        return tile_counter


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""

    screen_width = max([x for x, _ in game.tiles]) + 1
    screen_height = max([y for _, y in game.tiles]) + 1

    screen = []
    for y in range(0, screen_height):
        row = []
        for x in range(0, screen_width):
            row.append(EMPTY)
        screen.append(row)

    for x, y in game.tiles:
        screen[y][x] = game.tiles[(x, y)]

    return screen


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""

    screen = screen_rows(game)
    screen_text = ""
    rows = []
    for row in screen:
        row_value = ""
        for value in row:
            if value == EMPTY:
                row_value = row_value + SYMBOLS[EMPTY]
            elif value == WALL:
                row_value = row_value + SYMBOLS[WALL]
            elif value == BLOCK:
                row_value = row_value + SYMBOLS[BLOCK]
            elif value == PADDLE:
                row_value = row_value + SYMBOLS[PADDLE]
            elif value == BALL:
                row_value = row_value + SYMBOLS[BALL]

        rows.append(row_value)

    screen_text = "\n".join(rows)

    return screen_text


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
        if game.paddle is None or game.ball is None:
            return 0

        if game.paddle[0] < game.ball[0]:
            return 1
        elif game.paddle[0] > game.ball[0]:
            return -1

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
