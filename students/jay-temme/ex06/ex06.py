# Exercise 06. See README.md for the full task.
# Replace each `pass` line with your code.

from dataclasses import dataclass, field  # noqa: F401  (you'll need `field` in Part 2)
from pathlib import Path

from intcode import EmptyInputError, decode, load_program, step  # noqa: F401

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

    def __init__(self, program: list):
        self.program = program.copy()
        self.current_position = 0
        self.relative_base = 0
        self.halted = False

    def run(self, inputs: list) -> list:
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        position = self.current_position
        outputs = []

        while position is not None:
            try:
                position, self.relative_base = step(
                    self.program, position, inputs, outputs, self.relative_base
                )

            except EmptyInputError:
                self.current_position = position
                break

        if position is None:
            self.halted = True

        return outputs


def count_tiles(outputs: list, input_tile: int) -> int:
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    number_of_tiles = 0

    for x, y, tile in [
        (outputs[i], outputs[i + 1], outputs[i + 2]) for i in range(0, len(outputs), 3)
    ]:
        if x == -1:
            continue

        if tile == input_tile:
            number_of_tiles += 1

    return number_of_tiles


# ---------------------------------------------------------------- Part 2 (at home)


@dataclass
class Game:
    tiles: dict[tuple[int], int] = field(default_factory=dict)
    score: int = 0
    scores: list[tuple[int]] = field(default_factory=list)
    ball: tuple[int] = None
    paddle: tuple[int] = None

    def update(self, outputs: list):
        for x, y, tile in [
            (outputs[i], outputs[i + 1], outputs[i + 2]) for i in range(0, len(outputs), 3)
        ]:
            if x == -1 and y == 0:
                self.score = tile
                continue

            if tile == BALL:
                self.ball = (x, y)

            if tile == PADDLE:
                self.paddle = (x, y)

            self.tiles[(x, y)] = tile

        self.scores.append(self.score)

    def count(self, input_tile: int) -> int:
        """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
        number_of_tiles = len(
            [(x, tile) for (x, y), tile in self.tiles.items() if tile == input_tile and x != -1]
        )
        return number_of_tiles


def screen_rows(game: Game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""
    screen = []

    for (x, y), tile in game.tiles.items():
        if len(screen) <= y:
            screen.extend([[]] * (y - (len(screen) - 1)))

        if len(screen[y]) <= x:
            screen[y].extend([None] * (x - (len(screen[y]) - 1)))

        screen[y][x] = tile

    return screen


def draw(game: Game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    screen_string = ""

    for screen_row in screen_rows(game):
        for tile in screen_row:
            screen_string += SYMBOLS[tile]

        screen_string += "\n"

    return screen_string[:-1]


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
        if game.paddle[0] < game.ball[0]:
            return 1
        if game.paddle[0] > game.ball[0]:
            return -1
        return 0


class Keyboard(Controller):
    """Reads input from the user to play the game."""

    def draw_game(self, game: Game):
        print("score: ", game.score)
        print(draw(game))

    def get_next_input(self) -> int:
        next_input = input("Enter next input (a: left, d: right, nothing: stay): ")
        while next_input not in ["a", "d", ""]:
            next_input = input("Enter a valid input (a: left, d: right, nothing: stay):")

        if next_input == "a":
            return -1
        if next_input == "d":
            return 1
        return 0

    def choose(self, game: Game) -> int:
        self.draw_game(game)

        return self.get_next_input()


def play(program: list[int], controller: Controller) -> Game:
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

    print("Part 2")
    start = Game()
    start.update(Computer(program).run([]))
    print(draw(start))
    lost = play(program, Stay())
    print("2:", lost.score)
    won = play(program, Autopilot())
    print("3:", won.score, "after", len(won.scores) - 1, "frames")
    print(draw(won))

    print("Bonus")
    # playing = play(program, Keyboard())
    # print("Score: ", playing.score)
    # print(draw(playing))
