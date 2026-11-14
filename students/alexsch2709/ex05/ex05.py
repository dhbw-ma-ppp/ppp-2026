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
    lines = text.strip().splitlines()
    for line in lines:
        line = line.strip()
        row = []
        for char in line:
            row.append(int(char))
        grid.append(row)
    return grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    total_risk = 0

    # Erstes Feld zählt nicht
    for position in path[1:]:
        row = position[0]
        col = position[1]
        total_risk += grid[row][col]
    return total_risk


def lowest_risk(grid, row=0, col=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    rows = len(grid)
    cols = len(grid[0])
    memo = {}

    def solve(r, c):
        if (r, c) in memo:
            return memo[(r, c)]

        # Ziel erreicht
        if r == rows - 1 and c == cols - 1:
            return 0
        risks = []
        # nach unten
        if r + 1 < rows:
            risk_down = grid[r + 1][c] + solve(r + 1, c)
            risks.append(risk_down)
        # nach rechts
        if c + 1 < cols:
            risk_right = grid[r][c + 1] + solve(r, c + 1)
            risks.append(risk_right)
        result = min(risks)
        memo[(r, c)] = result
        return result

    return solve(row, col)


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    result = []
    rows = len(grid)
    cols = len(grid[0])

    # oben
    if row > 0:
        result.append((row - 1, col))
    # unten
    if row < rows - 1:
        result.append((row + 1, col))
    # links
    if col > 0:
        result.append((row, col - 1))
    # rechts
    if col < cols - 1:
        result.append((row, col + 1))
    return result


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    rows = len(grid)
    cols = len(grid[0])

    ziel = (rows - 1, cols - 1)

    # Speichert das bisher beste Risiko für jede Position
    risks = {}
    risks[(0, 0)] = 0

    # Positionen, die noch untersucht werden müssen
    open_list = [(0, 0)]

    while len(open_list) > 0:
        # Position mit dem niedrigsten Risiko suchen
        current = open_list[0]

        for pos in open_list:
            if risks[pos] < risks[current]:
                current = pos

        open_list.remove(current)

        row, col = current

        if current == ziel:
            return risks[current]

        for n_row, n_col in neighbours(grid, row, col):
            new_risk = risks[current] + grid[n_row][n_col]

            if (n_row, n_col) not in risks:
                risks[(n_row, n_col)] = new_risk
                open_list.append((n_row, n_col))

            elif new_risk < risks[(n_row, n_col)]:
                risks[(n_row, n_col)] = new_risk

                if (n_row, n_col) not in open_list:
                    open_list.append((n_row, n_col))


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
