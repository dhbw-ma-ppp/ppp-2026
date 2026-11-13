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
    Result = []
    Helper = []

    for char in text:
        if char == "\n":
            if Helper != []:
                Result.append(Helper)
                Helper = []
        elif char != " ":
            Helper.append(int(char))
    return Result


def print_grid(text):
    for Row in parse_grid(text):
        print("".join(Row))


def path_risk(grid, path):
    risk = 0
    for row, col in path:
        risk += grid[row][col]
    risk -= grid[0][0]
    return risk


def lowest_risk(grid, row=0, col=0, memo=None):
    if memo is None:
        memo = {}

    rows = len(grid)
    cols = len(grid[0])

    if row == rows - 1 and col == cols - 1:
        return 0

    if (row, col) in memo:
        return memo[(row, col)]

    right = float("inf")
    down = float("inf")

    if col + 1 < cols:
        right = grid[row][col + 1] + lowest_risk(grid, row, col + 1, memo)

    if row + 1 < rows:
        down = grid[row + 1][col] + lowest_risk(grid, row + 1, col, memo)

    memo[(row, col)] = min(right, down)

    return memo[(row, col)]


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    Result = []

    rows = len(grid)
    cols = len(grid[0])
    if row - 1 >= 0:
        Result.append((row - 1, col))
    if row + 1 < rows:
        Result.append((row + 1, col))
    if col - 1 >= 0:
        Result.append((row, col - 1))
    if col + 1 < cols:
        Result.append((row, col + 1))
    return Result


def lowest_risk_any_direction(grid):
    rows = len(grid)
    cols = len(grid[0])

    distances = [[float("inf")] * cols for _ in range(rows)]
    distances[0][0] = 0

    queue = [(0, 0, 0)]

    while queue:
        queue.sort()
        risk, row, col = queue.pop(0)

        if row == rows - 1 and col == cols - 1:
            return risk

        if risk > distances[row][col]:
            continue

        for next_row, next_col in neighbours(grid, row, col):
            new_risk = risk + grid[next_row][next_col]

            if new_risk < distances[next_row][next_col]:
                distances[next_row][next_col] = new_risk
                queue.append((new_risk, next_row, next_col))


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
    parse_grid(EXAMPLE_TEXT)
    print(EXAMPLE_PATH[0][0])
