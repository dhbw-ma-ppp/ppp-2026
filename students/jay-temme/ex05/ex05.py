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
    for item in text.split():
        if not item.isdigit():
            raise ValueError("text must only contain whitespace and integers")

    grid = list()

    for line in text.split("\n"):
        if line.strip() == "":
            continue
        elif line.split()[0] is not line.strip():
            raise ValueError("text contains spaces inbetween values")
        else:
            grid_line = list()

            for position in line.strip():
                grid_line.append(int(position))

            grid.append(grid_line)

    return grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """

    def raise_grid_TypeError():
        raise TypeError("grid must be of type list and only contain lists of integers")

    if type(grid) is not list:
        raise_grid_TypeError()

    for row in grid:
        if type(row) is not list:
            raise_grid_TypeError()

        for item in row:
            if type(item) is not int:
                raise_grid_TypeError()

    def raise_path_TypeError():
        raise TypeError("path must be of type list and only contain tuples of integers")

    if type(path) is not list:
        raise_path_TypeError()

    for position in path:
        if type(position) is not tuple:
            raise_path_TypeError()

        if len(position) != 2:
            raise ValueError("path must only contain tuples of length 2")

        for coordinate in position:
            if type(coordinate) is not int:
                raise_path_TypeError()

    try:
        risks = [grid[position[0]][position[1]] for position in path]
    except IndexError:
        raise ValueError("path must only contain valid positions in grid")

    return sum(risks)


def lowest_risk(grid, row=0, col=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """

    def raise_grid_TypeError():
        raise TypeError("grid must be of type list and only contain lists of integers")

    if type(grid) is not list:
        raise_grid_TypeError()

    for grid_row in grid:
        if type(grid_row) is not list:
            raise_grid_TypeError()

        for item in grid_row:
            if type(item) is not int:
                raise_grid_TypeError()

    grid_h = [[None] * len(grid_row) for grid_row in grid]

    def lowest_risk_h(row_h, col_h):
        risk_down = None
        risk_right = None

        if row_h + 1 == len(grid) and col_h + 1 == len(grid[-1]):
            return 0

        if row_h + 1 < len(grid) and col_h < len(grid[row_h + 1]):
            if grid_h[row_h + 1][col_h] is None:
                lowest_risk_down = lowest_risk_h(row_h + 1, col_h)
                if type(lowest_risk_down) is int:
                    grid_h[row_h + 1][col_h] = lowest_risk_down + grid[row_h + 1][col_h]

            risk_down = grid_h[row_h + 1][col_h]

        if col_h + 1 < len(grid_h[row_h]):
            if grid_h[row_h][col_h + 1] is None:
                lowest_risk_right = lowest_risk_h(row_h, col_h + 1)
                if type(lowest_risk_right) is int:
                    grid_h[row_h][col_h + 1] = lowest_risk_right + grid[row_h][col_h + 1]

            risk_right = grid_h[row_h][col_h + 1]

        if risk_down is None:
            risk_down = risk_right

        if risk_right is None:
            risk_right = risk_down

        if risk_down is None:
            return None

        return min(risk_down, risk_right)

    lowest_risk_int = lowest_risk_h(row, col)

    if lowest_risk_int is None:
        raise ValueError("grid must not have any empty rows")

    return lowest_risk_int


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""

    def raise_grid_TypeError():
        raise TypeError("grid must be of type list and only contain lists of integers")

    if type(grid) is not list:
        raise_grid_TypeError()

    for grid_row in grid:
        if type(grid_row) is not list:
            raise_grid_TypeError()

        for item in grid_row:
            if type(item) is not int:
                raise_grid_TypeError()

    def raise_row_col_ValueError():
        raise ValueError("(row, col) must be a valid position in grid")

    if row < 0 or len(grid) <= row:
        raise_row_col_ValueError()

    for grid_row in grid:
        if col < 0 or len(grid_row) <= col:
            raise_row_col_ValueError()

    neighbours_list = []


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
