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

    own_program = []
    input_list = []
    position = 0
    relative_base = 0
    halted = False
    needs_input = False

    def __init__(self, program):
        self.own_program = program.copy()
        pass

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        if len(inputs) != 0 and self.needs_input:
            self.needs_input = False
        self.input_list.extend(inputs)
        output = []
        while not self.halted and not self.needs_input:
            try:
                pos, rel = step(
                    self.own_program, self.position, self.input_list, output, self.relative_base
                )
            except ValueError:
                self.needs_input = True
            else:
                self.relative_base = rel
                if pos is not None:
                    self.position = pos
                else:  # finished
                    self.halted = True
        return output


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    counter = 0
    for i in range(len(outputs) // 3):
        cur_tuple = i * 3
        if outputs[cur_tuple + 2] == tile and outputs[cur_tuple] != -1:
            counter += 1
    return counter


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).
class Game:
    tiles = dict()
    score = 0
    scores = []
    ball = None
    paddle = None

    def __init__(self):
        self.tiles = dict()
        self.score = 0
        self.scores = []
        self.ball = None
        self.paddle = None

    def update(self, outputs):
        for i in range(len(outputs) // 3):
            x, y, tile_type = outputs[i * 3], outputs[i * 3 + 1], outputs[i * 3 + 2]

            if x == -1:
                self.score = outputs[3 * i + 2]
            elif tile_type == 3:  # paddle
                self.paddle = (x, y)
            elif tile_type == 4:  # ball
                self.ball = (x, y)

            if x != -1:
                self.tiles[(x, y)] = tile_type

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
    tiles = game.tiles
    width = 0
    height = 0
    for k, _ in tiles.items():
        if k[0] > width:
            width = k[0]
    for k, _ in tiles.items():
        if k[1] > height:
            height = k[1]
    width += 1
    height += 1

    map = []
    for y in range(height):
        map.append([tiles[(x, y)] for x in range(width)])
    return map


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    rows = screen_rows(game)
    full_str = ""
    for row in rows:
        for tile in row:
            match tile:
                case 0:
                    full_str += " "
                case 1:
                    full_str += "#"
                case 2:
                    full_str += "="
                case 3:
                    full_str += "-"
                case 4:
                    full_str += "o"
        full_str += "\n"
    return full_str[:-1]


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
        paddle = game.paddle
        ball = game.ball
        if ball[0] > paddle[0]:  # ball is right of paddle
            return 1
        elif ball[0] < paddle[0]:  # ball is left of paddle
            return -1
        else:
            return 0


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    game = Game()
    com = Computer(program)

    outputs = com.run([])  # init run
    game.update(outputs)

    while not com.halted:
        move = controller.choose(game)
        outputs = com.run([move])
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
