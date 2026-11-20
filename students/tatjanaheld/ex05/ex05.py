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

    grid = []
    zeilen = text.split("\n")

    for zeile in zeilen:
        zeile = zeile.strip()
        if zeile == "":
            continue

        row = []
        for zeichen in zeile:
            row.append(int(zeichen))
        grid.append(row)

    return grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """

    summe = 0

    for position in path[1:]:
        row, col = position
        summe = summe + grid[row][col]

    return summe


def lowest_risk(grid, row=0, col=0, memo=None):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """

    if memo is None:
        memo = {}

    if (row, col) in memo:
        return memo[row, col]

    last_row = len(grid) - 1
    last_col = len(grid[0]) - 1

    if row == last_row and col == last_col:
        return 0

    options = []

    if col < last_col:
        feld_rechts = grid[row][col + 1]

        rest = lowest_risk(grid, row, col + 1, memo)
        options.append(feld_rechts + rest)

    if row < last_row:
        feld_unten = grid[row + 1][col]

        rest = lowest_risk(grid, row + 1, col, memo)
        options.append(feld_unten + rest)

    result = min(options)
    memo[(row, col)] = result
    return result


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""

    result = []

    if row > 0:
        result.append((row - 1, col))

    if row < len(grid) - 1:
        result.append((row + 1, col))

    if col > 0:
        result.append((row, col - 1))

    if col < len(grid[0]) - 1:
        result.append((row, col + 1))

    return result


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """

    last_row = len(grid) - 1
    last_col = len(grid[0]) - 1

    candidates = [(0, 0, 0)]
    done = set()

    while candidates:
        best = min(candidates)
        candidates.remove(best)
        risk, row, col = best

        if row == last_row and col == last_col:
            return risk

        if (row, col) in done:
            continue

        done.add((row, col))

        for next_row, next_col in neighbours(grid, row, col):
            new_risk = risk + grid[next_row][next_col]
            candidates.append((new_risk, next_row, next_col))


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
