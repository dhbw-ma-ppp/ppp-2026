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
        self.memory = list(program)  # Kopie des Originals welches unverändert bleibt
        self.position = 0  # Wo bin ich grade
        self.base = 0  # Basis für Modus 2
        self.halted = False  # True, sobald Opcode 99 /
        self.inputs = []
        self.outputs = []  # Ausgaben des aktuellen Aufrufs

    def run(self, inputs):
        """Add `inputs`, then run until the program halts or needs an input it doesn't have.

        Return the numbers output during this call.
        """
        # Neue Eingaben hinten anfügen – alte, noch unbenutzte bleiben erhalten.
        self.inputs.extend(inputs)

        # Für diesen Aufruf mit einer leeren Ausgabeliste starten.
        self.outputs = []

        # Solange laufen, bis das Programm hält.
        while not self.halted:
            try:
                # step() führt genau EINE Anweisung aus und sagt uns,
                # wo es danach weitergeht (None = Opcode 99).
                next_position, self.base = step(
                    self.memory, self.position, self.inputs, self.outputs, self.base
                )
            except ValueError:
                # Opcode 3 wollte eine Eingabe, aber es war keine mehr da.
                # Wir pausieren: self.position bleibt stehen, damit der
                # nächste run()-Aufruf genau hier weitermacht.
                return self.outputs

            if next_position is None:
                # Opcode 99: das Programm ist zu Ende.
                self.halted = True  # erst setzen
                return self.outputs  # dann zurückgeben

            # Sonst: zur nächsten Anweisung springen.
            self.position = next_position

        return self.outputs


def count_tiles(outputs, tile):
    """How many (x, y, tile) triples in `outputs` have this tile. Score triples don't count."""
    anzahl = 0

    # Immer in Dreierschritten durch die Liste gehen.
    for i in range(0, len(outputs) - 2, 3):
        x = outputs[i]
        y = outputs[i + 1]
        kachel = outputs[i + 2]

        # Score-Tripel überspringen.
        if x == -1 and y == 0:
            continue

        # Zählen, wenn es die gesuchte Kachel ist.
        if kachel == tile:
            anzahl += 1

    return anzahl


if __name__ == "__main__":
    # Programm aus der Datei laden.
    program = load_program("students/florire23-prog/ex06/breakout.txt")

    # Computer bauen und starten. run([]) läuft so lange,
    # bis das Spiel zum ersten Mal eine Eingabe verlangt.
    game = Computer(program)
    outputs = game.run([])

    # Kleine Kontrolle: 3 Zahlen pro Kachel, also muss die Länge aufgehen.
    print("gehalten:", game.halted)
    print("Ausgaben in diesem Aufruf:", len(outputs))
    print("Tripel:", len(outputs) // 3, " Rest:", len(outputs) % 3)

    # Blöcke haben die Kachel-ID 2.
    print("BLÖCKE ZU BEGINN:", count_tiles(outputs, 2))


# ---------------------------------------------------------------- Part 2 (at home)


# 1. Write the dataclass `Game` here (see README.md).


@dataclass
class Game:
    """Der Spielstand: welche Kachel wo liegt, plus Punkte und Positionen."""

    tiles: dict = field(default_factory=dict)  # (x, y) -> Kachel-ID
    score: int = 0
    scores: list = field(default_factory=list)
    ball: tuple | None = None
    paddle: tuple | None = None

    def update(self, outputs: list[int]) -> None:
        """Die Tripel aus outputs einarbeiten."""
        for i in range(0, len(outputs) - 2, 3):
            x = outputs[i]
            y = outputs[i + 1]
            tile_id = outputs[i + 2]

            if x == -1 and y == 0:
                self.score = tile_id  # Score setzen, nicht addieren
                continue

            self.tiles[(x, y)] = tile_id

            if tile_id == BALL:
                self.ball = (x, y)
            elif tile_id == PADDLE:
                self.paddle = (x, y)

        self.scores.append(self.score)  # aktueller Stand nach diesem update

    def count(self, tile):
        """Wie viele Kacheln dieser Art liegen auf dem Bildschirm?"""
        return sum(1 for t in self.tiles.values() if t == tile)


def screen_rows(game) -> list[list[int]]:
    """The screen as a list of rows: screen_rows(game)[y][x] is the tile at (x, y)."""

    if not game.tiles:
        return []

    max_x = max(x for x, _ in game.tiles)
    max_y = max(y for _, y in game.tiles)

    return [[game.tiles.get((x, y), 0) for x in range(max_x + 1)] for y in range(max_y + 1)]


def draw(game) -> str:
    """The screen as text: one line per row, one character per tile (see SYMBOLS)."""
    # Bildschirm als Liste von Zeilen
    rows = screen_rows(game)

    # Leerer Bildschirm: einfach der leere Text
    if not rows:
        return ""

    # Jede Zeile: Kachel-IDs in Zeichen umwandeln und aneinanderhängen.
    lines = []
    for row in rows:
        line = ""
        for tile in row:
            line += SYMBOLS[tile]
        lines.append(line)

    # Die Zeilen mit Zeilenumbrüchen verbinden.
    return "\n".join(lines)


# ------------------------nichts gemacht------------------------#
class Controller:
    """Chooses the joystick input: -1 left, 0 stay, 1 right."""

    def choose(self, game) -> int:
        raise NotImplementedError


class Stay(Controller):
    """Never moves the paddle."""

    def choose(self, game) -> int:
        return 0


# --------------------------------------------------------------#


class Autopilot(Controller):
    """Plays the game: keeps the ball in play until every block is gone."""

    def choose(self, game) -> int:
        if game.ball is None or game.paddle is None:
            return 0
        if game.ball[0] < game.paddle[0]:
            return -1
        if game.ball[0] > game.paddle[0]:
            return 1
        return 0


def play(program, controller):
    game = Game()
    computer = Computer(program)

    # Startbildschirm aufbauen: noch KEIN Score-Eintrag.
    game.update(computer.run([]))

    while True:
        game.update(computer.run([controller.choose(game)]))

        if computer.halted:
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
