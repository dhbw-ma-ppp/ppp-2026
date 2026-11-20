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
    text = text.split("\n")
    result = []
    for row in text:
        row = row.strip()
        if row == "":
            continue

        ResultingRow = []
        for char in row:
            ResultingRow.append(int(char))
        result.append(ResultingRow)

    return result


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    risk = 0
    for actionX, actionY in path:
        if actionX == 0 and actionY == 0:
            continue
        risk += grid[actionX][actionY]

    return risk


def lowest_risk(grid, row=0, col=0, memory=None):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    # Avoid IndexOutOfBounds and reiterating memory and grid errors
    if not grid or not grid[0]:
        raise ValueError("Grid cannot be empty")

    if memory is None:
        memory = {}

    if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
        raise ValueError("Starting position out of bounds")

    if row == len(grid) - 1 and col == len(grid[row]) - 1:
        return 0

    if (row, col) in memory:
        return memory[(row, col)]

    down = float("inf")
    right = float("inf")

    if row < len(grid) - 1:
        down = grid[row + 1][col] + lowest_risk(grid, row + 1, col, memory)

    if col < len(grid[0]) - 1:
        right = grid[row][col + 1] + lowest_risk(grid, row, col + 1, memory)

    memory[(row, col)] = min(down, right)

    return memory[(row, col)]


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    result = []

    possible_moves = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    for rows, cols in possible_moves:
        if 0 <= rows < len(grid) and 0 <= cols < len(grid[0]):
            result.append((rows, cols))

    return result


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    rows = len(grid)
    cols = len(grid[0])

    distances = {(0, 0): 0}
    visited = set()

    while True:
        current = None
        lowest = float("inf")

        for position, risk in distances.items():
            if position not in visited and risk < lowest:
                current = position
                lowest = risk

        if current is None:
            return float("inf")

        row, col = current

        if row == rows - 1 and col == cols - 1:
            return lowest

        visited.add(current)

        for nr, nc in neighbours(grid, row, col):
            if (nr, nc) in visited:
                continue

            new_risk = lowest + grid[nr][nc]

            if new_risk < distances.get((nr, nc), float("inf")):
                distances[(nr, nc)] = new_risk


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    example = parse_grid(EXAMPLE_TEXT)
    cave = parse_grid(CAVE)

    memory = {}

    print("Part 1")
    print("1:", lowest_risk(example))
    print("2:", path_risk(example, EXAMPLE_PATH))

    print("Part 2")
    print("3:", lowest_risk(cave))
    print("4:", lowest_risk_any_direction(example))
    print("5:", lowest_risk_any_direction(cave))
