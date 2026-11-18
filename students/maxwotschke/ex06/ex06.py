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
        self.position = 0
        self.base = 0
        self.inputs = []

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        self.inputs.extend(inputs)
        outputs = []
        while not self.halted:
            if decode(self.program[self.position])[0] == 3 and len(self.inputs) < 1:
                break

            self.position, self.base = step(
                self.program, self.position, self.inputs, outputs, self.base
            )

            if self.position is None:
                self.halted = True
                break

        return outputs


# computer = Computer([104, 7, 104, 8, 99])
# print(computer.run([]))


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    counter = 0
    for i in range(len(outputs) // 3):
        current_triple = i * 3
        if outputs[current_triple + 2] == tile and outputs[current_triple] != -1:
            counter += 1
    return counter


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).
@dataclass
class Game:
    scores: list[int] = field(default_factory=list)
    x: int = 0
    y: int = 0
    tiles: dict[tuple[int, int], int] = field(default_factory=dict)
    score: int = 0
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None

    def update(self, outputs):
        for i in range(len(outputs) // 3):
            current_triple = i * 3
            x, y, tile = (
                outputs[current_triple],
                outputs[current_triple + 1],
                outputs[current_triple + 2],
            )

            if x == -1:
                self.score = tile
            elif tile == 3:
                self.paddle = (x, y)
            elif tile == 4:
                self.ball = (x, y)

            if x != -1:
                if tile in self.tiles.values() and (tile == 3 or tile == 4):
                    for key in self.tiles.copy().keys():
                        if self.tiles[key] == tile:
                            del self.tiles[key]

                self.tiles[(x, y)] = tile
        self.scores.append(self.score)
        pass

    def count(self, tile):
        counter = 0
        for value in self.tiles.values():
            if value == tile:
                counter += 1
        return counter


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    if game.tiles == {}:
        return []
    height = 0
    width = 0
    for tile, _ in game.tiles.items():
        if tile[1] > height:
            height = tile[1]
        if tile[0] > width:
            width = tile[0]

    screen_as_list = []
    for y in range(height + 1):
        screen_as_list.append([game.tiles[(x, y)] for x in range(width + 1)])
    return screen_as_list


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    screen = ""
    for row in screen_rows(game):
        for tile in row:
            match tile:
                case 0:
                    screen += " "
                case 1:
                    screen += "#"
                case 2:
                    screen += "="
                case 3:
                    screen += "-"
                case 4:
                    screen += "o"
        screen += "\n"
    return screen[:-1]


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
        if game.ball is not None and game.paddle is not None:
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
    game.update(computer.run([]))

    while not computer.halted:
        controls = controller.choose(game)
        game.update(computer.run([controls]))

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
