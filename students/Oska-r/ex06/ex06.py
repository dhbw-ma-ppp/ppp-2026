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

        self.index = 0
        self.relative_base = [0]

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        self.inputs.extend(inputs)
        outputs = []

        while self.index is not None:
            opcode = decode(self.program[self.index])[0]
            if opcode == 99:
                self.halted = True
                break
            if self.inputs == [] and opcode == 3:
                break
            self.index = step(self.program, self.index, self.inputs, outputs, self.relative_base)

        return outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    counter = 0
    for index in range(2, len(outputs), 3):
        if outputs[index - 2] == -1:
            continue

        if outputs[index] == tile:
            counter += 1

    return counter


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).


@dataclass
class Game:
    tiles: dict[tuple[int, int], int] = field(default_factory=dict)
    score: int = 0
    scores: list[int] = field(default_factory=list)
    ball: tuple[int, int] = None
    paddle: tuple[int, int] = None

    def update(self, outputs: list[int]) -> None:
        score_updated = False
        paddle_found = False
        for tile_index in range(2, len(outputs), 3):
            tile = outputs[tile_index]
            position = (outputs[tile_index - 2], outputs[tile_index - 1])

            if position[0] == -1:
                self.scores.append(tile)
                self.score = tile
                score_updated = True
                continue

            self.tiles[position] = tile
            match tile:
                case 3:
                    if not paddle_found:
                        self.paddle = position
                        paddle_found = True
                    else:
                        raise ValueError("Only 1 paddle is allowed, 2 were found.")
                case 4:
                    self.ball = position
                case _:
                    pass
        if not score_updated:
            self.scores.append(0)

    def count(self, tile: int) -> None:
        counter = 0
        for current_tile in self.tiles.values():
            if current_tile == tile:
                counter += 1
        return counter


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    max_x = 0
    max_y = 0

    for position in game.tiles:
        if position[0] > max_x:
            max_x = position[0]
        if position[1] > max_y:
            max_y = position[1]

    cols = [0] * (max_x + 1)
    screen = []
    for i in range(0, max_y + 1):
        screen.append(cols.copy())

    for position in game.tiles:
        screen[position[1]][position[0]] = game.tiles[position]
    return screen


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    text = ""
    game_array = screen_rows(game)
    for index, row in enumerate(game_array):
        for tile in row:
            text += SYMBOLS[tile]
        if index != len(game_array) - 1:
            text += "\n"
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

    def choose(self, game) -> int:
        if game.ball[0] < game.paddle[0]:
            return -1
        elif game.ball[0] > game.paddle[0]:
            return 1
        else:
            return 0


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    computer = Computer(program)
    game = Game()

    game.update(computer.run([]))

    while not computer.halted:
        game.update(computer.run([controller.choose(game)]))
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
