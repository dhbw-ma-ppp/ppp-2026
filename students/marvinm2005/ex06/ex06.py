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

    def __init__(
        self, program: list[int]
    ):  # constructor is called automatically when creating a new object
        self.memory = program.copy()  # every computer gets its own memory
        self.position = 0  # position of the next instruction
        self.base = 0  # relative base for memory access
        self.inputs: list[int] = []
        self.halted = False  # if the program ended completely

    def run(self, inputs: list[int]) -> list[int]:
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        self.inputs.extend(inputs)  # inputs is added (--> remaining inputs don't get lost)
        outputs: list[int] = []

        while not self.halted:
            opcode, _ = decode(self.memory[self.position])
            if opcode == 3 and not self.inputs:  # opcode 3 needs an input
                break  # wait, without executing input instruction

            next_position, self.base = (
                step(  # step() gives a new position in the program and relative base
                    self.memory, self.position, self.inputs, outputs, self.base
                )
            )
            if next_position is None:  # None means opcode 99 got executed
                self.halted = True
            else:
                self.position = next_position

        return outputs


def count_tiles(outputs: list[int], tile: int) -> int:
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    count = 0
    for i in range(0, len(outputs), 3):  # goes through the liste in three steps
        x, y, value = outputs[i : i + 3]  # cuts out the values
        if (x, y) != (-1, 0) and value == tile:  # (-1, 0) shows a score, so it doesn't count
            count += 1
    return count


# ---------------------------------------------------------------- Part 2 (at home)


@dataclass  # creates the instructor automatically
class Game:  # should know the current state of the game
    tiles: dict[tuple[int, int], int] = field(
        default_factory=dict
    )  # dict with coordinates as key and tile number as value; every object gets its own
    score: int = 0
    scores: list[int] = field(default_factory=list)  # every object gets its own
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None

    def update(self, outputs: list[int]):
        for i in range(0, len(outputs), 3):
            x, y, tile = outputs[i : i + 3]
            if (x, y) == (-1, 0):  # updating score
                self.score = tile
            else:
                self.tiles[(x, y)] = tile  # update the position on the field
                # We keep the new position in mind
                if tile == BALL:
                    self.ball = (x, y)
                elif tile == PADDLE:
                    self.paddle = (x, y)

        self.scores.append(self.score)  # save current score

    def count(self, tile: int) -> int:
        return sum(
            value == tile for value in self.tiles.values()
        )  # True counts as 1, False counts as 0


def screen_rows(game: Game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    if not game.tiles:
        return []

    width = max(x for x, y in game.tiles) + 1
    height = max(y for x, y in game.tiles) + 1
    rows = [[EMPTY for _ in range(width)] for _ in range(height)]
    for (x, y), tile in game.tiles.items():
        rows[y][x] = tile  # y is row, x is column
    return rows


def draw(game: Game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    rows = screen_rows(game)
    result = []
    for row in rows:
        line = ""
        for tile in row:
            symbol = SYMBOLS[tile]
            line = line + symbol
        result.append(line)
    output = "\n".join(result)

    return output


class Controller:
    """Chooses the joystick input: -1 left, 0 stay, 1 right."""

    def choose(self, game: Game) -> int:
        raise NotImplementedError


class Stay(Controller):
    """Never moves the paddle."""

    def choose(self, game: Game) -> int:
        return 0


class Autopilot(Controller):
    """Plays the game: keeps the ball in play until every block is gone."""

    def choose(self, game: Game) -> int:
        if game.ball is None or game.paddle is None:
            return 0
        ball_x, _ = game.ball
        paddle_x, _ = game.paddle
        if ball_x < paddle_x:  # position of the ball is left to the paddle
            return -1
        if ball_x > paddle_x:  # position of the ball is right to the paddle
            return 1
        return 0


def play(program: list[int], controller: Controller) -> Game:
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    computer = Computer(program)  # create new computer
    game = Game()  # create game
    game.update(computer.run([]))  # initial picture without input
    while not computer.halted:
        joystick = controller.choose(game)
        game.update(computer.run([joystick]))  # update the game with the new outputs

    return game  # return the Game object


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
