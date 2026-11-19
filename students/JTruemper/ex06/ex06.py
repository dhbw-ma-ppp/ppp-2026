from dataclasses import dataclass, field
from pathlib import Path

from intcode import decode, load_program, step
import time


PROGRAM_FILE = Path(__file__).parent / "breakout.txt"

EMPTY, WALL, BLOCK, PADDLE, BALL = 0, 1, 2, 3, 4

SYMBOLS = {
    EMPTY: " ",
    WALL: "#",
    BLOCK: "=",
    PADDLE: "-",
    BALL: "o",
}


RUNNING_TOTAL = [3, 13, 1, 12, 13, 12, 4, 12, 1105, 1, 0, 0, 0, 0]

TINY_GAME = [
    104, 0, 104, 0, 104, 3,
    104, 5, 104, 0, 104, 4,
    104, -1, 104, 0, 104, 0,
    3, 40, 1, 41, 40, 41, 104, -1, 104, 0, 4, 41,
    1001, 42, -1, 42, 1005, 42, 18, 99,
    0, 0, 0, 0, 3,
]


# ----------------------------------------------------------------
# Part 1


class Computer:
    """An IntCode computer that can pause when it needs input."""

    def __init__(self, program: list[int]) -> None:
        self.memory: list[int] = program.copy()
        self.position: int = 0
        self.base: int = 0
        self.inputs: list[int] = []
        self.halted: bool = False

    def run(self, inputs: list[int]) -> list[int]:
        """Run until the program halts or needs more input."""

        self.inputs.extend(inputs)
        outputs: list[int] = []

        while not self.halted:
            try:
                self.position, self.base = step(
                    self.memory,
                    self.position,
                    self.inputs,
                    outputs,
                    self.base,
                )

                if self.position is None:
                    self.halted = True

            except ValueError as error:
                if "no input left" in str(error):
                    break
                raise

        return outputs


def count_tiles(outputs: list[int], tile: int) -> int:
    """Count how many output triples contain the given tile."""

    return sum(
        1
        for i in range(0, len(outputs), 3)
        if outputs[i] != -1 and outputs[i + 2] == tile
    )


# ----------------------------------------------------------------
# Part 2


@dataclass
class Game:
    """Stores the current state of the Breakout game."""

    tiles: dict[tuple[int, int], int] = field(default_factory=dict)
    score: int = 0
    scores: list[int] = field(default_factory=list)
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None

    def update(self, outputs: list[int]) -> None:
        """Update the game using IntCode output."""

        for i in range(0, len(outputs), 3):
            x, y, value = outputs[i:i + 3]

            if x == -1 and y == 0:
                self.score = value

            else:
                self.tiles[(x, y)] = value

                if value == BALL:
                    self.ball = (x, y)

                elif value == PADDLE:
                    self.paddle = (x, y)

        self.scores.append(self.score)

    def count(self, tile: int) -> int:
        """Count how many positions contain the given tile."""

        return sum(
            value == tile
            for value in self.tiles.values()
        )


def screen_rows(game: Game) -> list[list[int]]:
    """Return the screen as a list of rows."""

    if not game.tiles:
        return []

    width = max(x for x, y in game.tiles) + 1
    height = max(y for x, y in game.tiles) + 1

    return [
        [game.tiles.get((x, y), EMPTY) for x in range(width)]
        for y in range(height)
    ]


def draw(game: Game) -> str:
    """Draw the screen as text."""

    return "\n".join(
        "".join(SYMBOLS[tile] for tile in row)
        for row in screen_rows(game)
    )


# ----------------------------------------------------------------
# Controllers


class Controller:
    """Base class for joystick controllers."""

    def choose(self, game: Game) -> int:
        raise NotImplementedError


class Stay(Controller):
    """Never moves the paddle."""

    def choose(self, game: Game) -> int:
        return 0


class Autopilot(Controller):
    """Moves the paddle towards the ball."""

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


# ----------------------------------------------------------------
# Play the game


def play(
    program: list[int],
    controller: Controller,
    display: bool = False,
) -> Game:
    """Play the game using the given controller."""

    computer = Computer(program)
    game = Game()

    # Run until the first input is needed.
    outputs = computer.run([])
    game.update(outputs)

    while not computer.halted:

        if display:
            print("\033[H\033[J", end="")
            print(draw(game))
            print("Score:", game.score)

        # Ask the controller for the next joystick input.
        joystick = controller.choose(game)

        # Continue the computer with that input.
        outputs = computer.run([joystick])

        # Update the game with the new output.
        game.update(outputs)

    return game



# ----------------------------------------------------------------
# Answers


if __name__ == "__main__":
    program = load_program(PROGRAM_FILE)

    print("Part 1")
    print("1:", count_tiles(Computer(program).run([]), BLOCK))

    print("\nPart 2")

    start = Game()
    start.update(Computer(program).run([]))

    print(draw(start))

    lost = play(program, Stay())
    print("2:", lost.score)

    won = play(program, Autopilot(), display=True)


    print("3:", won.score, "after", len(won.scores) - 1, "frames")
    print(draw(won))