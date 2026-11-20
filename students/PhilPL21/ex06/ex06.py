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
        self.own_program = program.copy()
        self.list_inputs = []
        self.position = 0
        self.base = 0
        self.halted = False

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """

        self.list_inputs.extend(inputs)
        outputs = []
        if self.halted:
            return outputs

        while True:
            opcode, _ = decode(self.own_program[self.position])
            if opcode == 3 and len(self.list_inputs) == 0:
                break

            next_position, next_base = step(
                self.own_program, self.position, self.list_inputs, outputs, self.base
            )

            if next_position is None:
                self.halted = True
                break
            self.position = next_position
            self.base = next_base
        return outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    if len(outputs) % 3 != 0:
        raise ValueError("outputs must contain complete triples")

    count = 0
    for i in range(0, len(outputs), 3):
        x = outputs[i]
        y = outputs[i + 1]
        tile_in = outputs[i + 2]
        if x == -1 and y == 0:
            continue
        if tile == tile_in:
            count += 1
    return count


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).
@dataclass
class Game:
    tiles: dict[tuple[int, int], int] = field(default_factory=dict)
    score: int = 0
    scores: list[int] = field(default_factory=list[int])
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None

    def update(self, outputs: list[int]) -> None:
        if len(outputs) % 3 != 0:
            raise ValueError("outputs must contain complete triples")

        for i in range(0, len(outputs), 3):
            x = outputs[i]
            y = outputs[i + 1]
            tile_in = outputs[i + 2]
            if x == -1 and y == 0:
                self.score = tile_in
                continue

            self.tiles[(x, y)] = tile_in
            if tile_in == BALL:
                self.ball = (x, y)
            elif tile_in == PADDLE:
                self.paddle = (x, y)

        self.scores.append(self.score)

    def count(self, tile: int) -> int:
        count = 0

        for tile_in in self.tiles.values():
            if tile_in == tile:
                count += 1
        return count


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    width = 0
    height = 0
    screen_final = []

    for x, y in game.tiles:
        width = max(width, x + 1)
        height = max(height, y + 1)

    for y in range(height):
        screen = []
        for x in range(width):
            screen.append(game.tiles.get((x, y), EMPTY))
        screen_final.append(screen)
    return screen_final


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    rows = screen_rows(game)
    text = ""
    for row in rows:
        for tile in row:
            match tile:
                case 0:
                    text += " "
                case 1:
                    text += "#"
                case 2:
                    text += "="
                case 3:
                    text += "-"
                case 4:
                    text += "o"
        text += "\n"
    return text[:-1]


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
        ball = game.ball
        paddle = game.paddle
        if game.ball is None or game.paddle is None:
            return 0
        if ball[0] < paddle[0]:
            return -1
        elif ball[0] > paddle[0]:
            return 1
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

    while True:
        if computer.halted:
            break
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
