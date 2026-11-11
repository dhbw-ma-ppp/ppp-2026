# Exercise 05. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import CAVE


EXAMPLE_TEXT = """
19999
19111
19191
11191
99991
"""

# A path through EXAMPLE_TEXT's grid (see README.md, answer 2).
# fmt: off
EXAMPLE_PATH = [
    (0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 3), (1, 4),
    (2, 4), (3, 4), (4, 4),
]
# fmt: on

# ---------------------------------------------------------------- Part 1 (in class)


aufrufe = 0


def parse_grid(text):
    """Return the grid in `text` as a list of rows, each a list of ints.

    `text` has one row per line and one digit per position. Blank lines and spaces at the
    start or end of a line don't matter.
    """
    grid = []
    for line in text.splitlines():
        line = line.strip()
        if line != "":
            row = []
            for zeichen in line:
                row.append(int(zeichen))
            grid.append(row)
    return grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    totalrisk = 0
    for row, col in path[1:]:  # Erste Position nicht gewertet da wir schon dort sind
        totalrisk += grid[row][col]
    return totalrisk


def lowest_risk(grid, row=0, col=0, _memo=None):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    global aufrufe

    if _memo is None:
        _memo = {}

    if (row, col) in _memo:
        return _memo[(row, col)]

    aufrufe += 1

    letzte_zeile = len(grid) - 1
    letzte_spalte = len(grid[0]) - 1

    if row == letzte_zeile and col == letzte_spalte:
        ergebnis = 0

    # Nach RECHTS, da es nach unten keine Zeile mehr gibt
    elif row == letzte_zeile:
        ergebnis = grid[row][col + 1] + lowest_risk(grid, row, col + 1, _memo)

    # Nach UNTEN, da es nach rechts keine Spalte mehr gibt
    elif col == letzte_spalte:
        ergebnis = grid[row + 1][col] + lowest_risk(grid, row + 1, col, _memo)

    else:
        # Mitten im Gitter: beide Richtungen sind möglich
        # RECHTS = gleiche Zeile, nächste Spalte
        rechts = grid[row][col + 1] + lowest_risk(grid, row, col + 1, _memo)
        # UNTEN = nächste Zeile, gleiche Spalte
        unten = grid[row + 1][col] + lowest_risk(grid, row + 1, col, _memo)
        # Den günstigeren der beiden Wege nehmen
        ergebnis = min(rechts, unten)

    _memo[(row, col)] = ergebnis
    return ergebnis


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    ergebnis = []
    if row > 0:
        ergebnis.append((row - 1, col))
    if row < len(grid) - 1:
        ergebnis.append((row + 1, col))
    if col > 0:
        ergebnis.append((row, col - 1))
    if col < len(grid[0]) - 1:
        ergebnis.append((row, col + 1))
    return ergebnis


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    ziel = (len(grid) - 1, len(grid[0]) - 1)
    beste = {(0, 0): 0}  # bisher bestes Risiko je Position
    offen = [(0, 0)]  # Positionen, die noch bearbeitet werden muessen

    while len(offen) > 0:
        # Position in `offen` mit dem kleinsten bisherigen Risiko suchen
        aktuelle = offen[0]
        for position in offen:
            if beste[position] < beste[aktuelle]:
                aktuelle = position
        offen.remove(aktuelle)

        if aktuelle == ziel:
            return beste[aktuelle]

        row, col = aktuelle
        for r, c in neighbours(grid, row, col):
            neues_risiko = beste[aktuelle] + grid[r][c]
            if (r, c) not in beste or neues_risiko < beste[(r, c)]:
                beste[(r, c)] = neues_risiko
                if (r, c) not in offen:
                    offen.append((r, c))
    return None


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    example = parse_grid(EXAMPLE_TEXT)
    cave = parse_grid(CAVE)

    print("Part 1")
    print("1:", lowest_risk(example))
    print("2:", path_risk(example, EXAMPLE_PATH))

    print("Part 2")
    print("3:", lowest_risk(cave))
    print("4:", lowest_risk_any_direction(example))
    print("5:", lowest_risk_any_direction(cave))
