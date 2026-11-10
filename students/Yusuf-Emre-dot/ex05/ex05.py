# Exercise 05. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import CAVE
from time import time
import heapq
import sys

sys.setrecursionlimit(10**6)
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
a = {"counter": 0}


def parse_grid(text):
    """Return the grid in `text` as a list of rows, each a list of ints.

    `text` has one row per line and one digit per position. Blank lines and spaces at the
    start or end of a line don't matter.
    """
    L = []
    for i in text.splitlines():
        i = i.strip(" ")
        if len(i) != 0:
            L.append([int(a) for a in i])
    return L


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    risk = 0
    for i in path[1:]:
        risk += grid[i[0]][i[1]]
    return risk


def lowest_risk(grid, row=0, col=0, Lookup_tabelle=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    rowmax = len(grid) - 1
    colmax = len(grid[0]) - 1
    # erste iteration macht erste Zeile und spalte und initialisiert den lookup
    if Lookup_tabelle == 0:
        Lookup_tabelle = [[0 for _ in range(rowmax + 1)] for _ in range(colmax + 1)]
        for i in range(row + 1, rowmax + 1):
            Lookup_tabelle[i][col] = grid[i][col] + Lookup_tabelle[i - 1][col]
        for i in range(col + 1, colmax + 1):
            Lookup_tabelle[row][i] = grid[row][i] + Lookup_tabelle[row][i - 1]
        row += 1
        col += 1

    for i in range(row, rowmax + 1):
        Lookup_tabelle[i][col] = grid[i][col] + min(
            Lookup_tabelle[i - 1][col], Lookup_tabelle[i][col - 1]
        )
    if col >= colmax:
        return Lookup_tabelle[rowmax][colmax]
    return lowest_risk(grid, row, col + 1, Lookup_tabelle)


# ---------------------------------------------------------------- Part 2 (at home)


def complex(lenght, f):
    a["counter"] = 0
    # macht ein grid n X n
    grid = [[1 for _ in range(lenght)] for _ in range(lenght)]
    f(grid)
    return a["counter"]


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1
    L = []
    if row < max_row:
        L.append((row + 1, col))
    if col < max_col:
        L.append((row, col + 1))
    if col > 0:
        L.append((row, col - 1))
    if row > 0:
        L.append((row - 1, col))

    return L


def lowest_risk_any_direction(grid, row=0, col=0, minimalrisk=0, prio=0, already_looked=0):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    rowmax = len(grid) - 1
    colmax = len(grid[0]) - 1
    # Bei der ertsen Iteration erzeugt es die riskliste und priority queue
    if minimalrisk == 0:
        prio = []
        heapq.heapify(prio)  # macht aus der Liste ein heap
        minimalrisk = [[float("inf") for _ in range(rowmax + 1)] for _ in range(colmax + 1)]
        minimalrisk[row][col] = 0
        already_looked = {}

    # ende der rekursion Ziel erfüllt
    if row >= rowmax and col >= colmax:
        return minimalrisk[row][col]

    # iteriert durch die Nachbarn und fügt ihren minimalenwert in minimalrisk ein. minimalrisk und prio werden aktualisiert falls es besser ist
    neighbour = neighbours(grid, row, col)
    for i in neighbour:
        value = minimalrisk[i[0]][i[1]]
        nrow, ncol = i[0], i[1]
        newvalue = grid[nrow][ncol] + minimalrisk[row][col]
        minimalrisk[nrow][ncol] = min(value, newvalue)
        if (
            newvalue < value and (nrow, ncol) not in already_looked
        ):  # macht prio kleiner da nicht unnötigt befüllt wird
            heapq.heappush(prio, (minimalrisk[nrow][ncol], i))

    already_looked[(row, col)] = True
    # Um wiederholungen zu vermeinden wird untersucht ob die Position schon bearbeitet wurde
    for i in range(len(prio)):
        next = heapq.heappop(prio)
        next_row, next_col = next[1]
        if (next_row, next_col) not in already_looked:
            a["counter"] += 1
            return lowest_risk_any_direction(
                grid, next_row, next_col, minimalrisk, prio, already_looked
            )


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    example = parse_grid(EXAMPLE_TEXT)
    cave = parse_grid(CAVE)

    print("Part 1")
    print("1:", lowest_risk(example))
    print("2:", path_risk(example, EXAMPLE_PATH))
    print("Part 2")
    print("3:", lowest_risk(cave))
    print("-----------------------------------------------------------------")
    print("4:", lowest_risk_any_direction(example))
    zeit = time()
    print("5:", lowest_risk_any_direction(cave))
    print("Cave abgeschlossen in", time() - zeit, "sek")
