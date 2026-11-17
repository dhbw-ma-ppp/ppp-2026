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


def path_risk(gitter, weg):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    totales_risiko = 0
    for reihe, spalte in weg[1:]:  # Erste Position nicht gewertet da wir schon dort sind
        totales_risiko += gitter[reihe][spalte]
    return totales_risiko


def lowest_risk(gitter, reihe=0, spalte=0, _memo=None):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    global aufrufe

    if _memo is None:
        _memo = {}

    if (reihe, spalte) in _memo:
        return _memo[(reihe, spalte)]

    aufrufe += 1

    letzte_zeile = len(gitter) - 1
    letzte_spalte = len(gitter[0]) - 1

    if reihe == letzte_zeile and spalte == letzte_spalte:
        ergebnis = 0

    # Nach RECHTS, da es nach unten keine Zeile mehr gibt
    elif reihe == letzte_zeile:
        ergebnis = gitter[reihe][spalte + 1] + lowest_risk(gitter, reihe, spalte + 1, _memo)

    # Nach UNTEN, da es nach rechts keine Spalte mehr gibt
    elif spalte == letzte_spalte:
        ergebnis = gitter[reihe + 1][spalte] + lowest_risk(gitter, reihe + 1, spalte, _memo)

    else:
        # Mitten im Gitter: beide Richtungen sind möglich
        # RECHTS = gleiche Zeile, nächste Spalte
        rechts = gitter[reihe][spalte + 1] + lowest_risk(gitter, reihe, spalte + 1, _memo)
        # UNTEN = nächste Zeile, gleiche Spalte
        unten = gitter[reihe + 1][spalte] + lowest_risk(gitter, reihe + 1, spalte, _memo)
        # Den günstigeren der beiden Wege nehmen
        ergebnis = min(rechts, unten)

    _memo[(reihe, spalte)] = ergebnis
    return ergebnis


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(gitter, reihe, spalte):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    ergebnis = []
    if reihe > 0:
        ergebnis.append((reihe - 1, spalte))
    if reihe < len(gitter) - 1:
        ergebnis.append((reihe + 1, spalte))
    if spalte > 0:
        ergebnis.append((reihe, spalte - 1))
    if spalte < len(gitter[0]) - 1:
        ergebnis.append((reihe, spalte + 1))
    return ergebnis


def lowest_risk_any_direction(gitter):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    ziel = (len(gitter) - 1, len(gitter[0]) - 1)
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

        reihe, spalte = aktuelle
        for r, s in neighbours(gitter, reihe, spalte):
            neues_risiko = beste[aktuelle] + gitter[r][s]
            if (r, s) not in beste or neues_risiko < beste[(r, s)]:
                beste[(r, s)] = neues_risiko
                if (r, s) not in offen:
                    offen.append((r, s))
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
