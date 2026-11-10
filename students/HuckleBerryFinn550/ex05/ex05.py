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


def parse_grid(text):
    """Return the grid in `text` as a list of rows, each a list of ints.

    `text` has one row per line and one digit per position. Blank lines and spaces at the
    start or end of a line don't matter.
    """
    listOfRows = []
    listOfDigits = []
    for line in text.splitlines():
        if line:
            for digit in line.strip().replace("'", " "):
                print(digit)
                listOfDigits.append(int(digit))
            listOfRows.append(listOfDigits.copy())
            listOfDigits.clear()
    return listOfRows


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    #fuer jede position in path die risk, also value an der Koordinate ausgeben
#input sind Koordinaten, also Tupel, in Liste
    #grid ist listOfRows
    risk_sum = 0
    for step in path[1:]:
        x = step[0]
        y = step[1]
        risk = grid[x][y]
        risk_sum+=risk
    return risk_sum




def lowest_risk(grid, row=0, col=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    #entweder ist klar, dass rechts oder nach unten weniger risk ist
    #oder beide Wege sind als Liste im PathPlanning
    #directions = [(0,1), (1,0)]
    # x, y = row, col
    # current = (x, y)
    # #currentRisk = grid[row][col]
    # last_coordinate = grid[len(grid)-1]
    # x_final, y_final = last_coordinate
    # lowest_risk_final = 0
    # path_planning = []
    #
    # while current != last_coordinate:
    #     candidates = []
    #     if y+1 <= y_final:
    #         candidates.append((x, y+1))
    #     if x+1 <= x_final:
    #         candidates.append((x+1, y))
    #     lowestRisk = min(grid[nextX][nextY] for nextX, nextY in candidates)
    #     for c in candidates:
    #         if grid[c[0], c[1]] == lowestRisk:
    #             path_planning.append(c)
    #
    #
    # for path in path_planning:
    #     if isinstance(path, list):
    #
    #         #thoughts:
    #         #falls zwei Kandidaten, doppelt rekursiver Aufruf
    #         #waehrend Aufruf Summe mit risks erhoehen
    #         #rekursiverAufruf mit Kanidaten als neue row, col
    # #zweiter Ansatz
    # while current != last_coordinate:
    #     riskRight = grid[x+1][y]
    #     riskDown = grid[x][y+1]
    #     if x + 1 <= x_final:
    #         lowest_risk(grid, row+1, col)
    #
    #     if y + 1 <= y_final:
    #         lowest_risk(grid, row, col+1)
    #     if riskRight <= riskDown:
    #         #wie speicher ich "ergebnis" des rekursiven Aufrufs?
    if len(grid) == 1:
        return 0
    else:
        x, y = row, col
        current = (x, y)
        x_final = len(grid) - 1  # letzte Zeile
        y_final = len(grid[0]) - 1  # letzte Spalte
        last_coordinate = (x_final, y_final)
        path_planning = []
        path_risks = []
        if current == last_coordinate:
            path_risks.append(path_risk(path_planning))
        else:
            if x + 1 <= x_final:
                path_planning.append(lowest_risk(grid, row + 1, col))
            if y + 1 <= y_final:
                path_planning.append(lowest_risk(grid, row, col + 1))

    return min(path_risks)


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    pass  # replace this line with your code


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    pass  # replace this line with your code


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
