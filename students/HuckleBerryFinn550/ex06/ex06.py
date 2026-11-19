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
        self.position = 0
        self.halted = False
        self.relative_base = 0
        self.inputs = []

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        outputs = []
        self.inputs.extend(inputs)
        pos = 0
        base = 0

        while not self.halted:
            try:
                pos, base = step(self.program, self.position, self.inputs, outputs, self.relative_base)
                if pos is None:
                    self.halted = True
                else:
                    self.position = pos
                    self.relative_base = base
            except ValueError : #if inputs are empty
                if self.program[self.position] % 100 == 3:  # waiting for input
                    return outputs
                else:
                    raise
        return  outputs

def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    triples_list = []
    counter = 0
    for i in range(0, len(outputs), 3):
        x = outputs[i]
        y = outputs[i + 1]
        tileOutputs = outputs[i + 2]
        triples_list.append((x, y, tileOutputs))

    for t in triples_list:
        if t[0] == -1 and t[1] == 0:
            continue
        elif t[2] == tile:
            counter+=1

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
        """Applies the outputs of one run call to the screen. If output is ball,
        paddle or score, those will be initiated."""
        for i in range(0, len(outputs), 3):
            x = outputs[i]
            y = outputs[i + 1]
            tile_outputs = outputs[i + 2]

            if x == -1 and y == 0:
                self.score = tile_outputs
            else:
                self.tiles[(x, y)] = tile_outputs

            if tile_outputs == 3:
                self.paddle = (x, y)
            if tile_outputs == 4:
                self.ball = (x, y)


        self.scores.append(self.score)

    def count(self, tile: int) -> int:
        """Counts how many positions in the grid show the tile."""
        counter = 0
        for t in self.tiles.values():
            if t == tile:
                counter+=1
        return counter

def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    if not game.tiles:
        return []

    width = max(x for (x, y) in game.tiles) + 1
    height = max(y for (x, y) in game.tiles) + 1
    list_of_rows = [[0] * width for _ in range(height)]

    for (x,y), tile in game.tiles.items():
            list_of_rows[y][x] = tile
    return list_of_rows


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    screen = ""
    symbols = [" ", "#", "=", "-", "o"]
    for row in screen_rows(game):
        for columns in row:
            screen += symbols[columns]
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
        x_ball, _ = game.ball
        x_paddle, _ = game.paddle
        if x_ball > x_paddle: 
            return 1
        elif x_ball < x_paddle:
            return -1
        else:
            return 0


def play(program: list[int], controller: Controller):
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    new_computer = Computer(program)
    new_game = Game()

    #first call without any inputs
    outputs = new_computer.run([])
    new_game.update(outputs)
    while not new_computer.halted:
        inputs_from_controller = controller.choose(new_game)
        outputs = new_computer.run([inputs_from_controller])
        new_game.update(outputs)
    return new_game










# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", count_tiles(Computer(program).run([]), BLOCK))

    #Part 2: uncomment once you get there.
    print("Part 2")
    start = Game()
    start.update(Computer(program).run([]))
    print(draw(start))
    lost = play(program, Stay())
    print("2:", lost.score)
    won = play(program, Autopilot())
    print("3:", won.score, "after", len(won.scores) - 1, "frames")
    print(draw(won))
