# Exercise 05. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import CAVE
import heapq

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
    maze_string = text.split("\n")
    for row_string in maze_string:
        row = []
        if row_string != "":
            row_int = int(row_string)
        else:
            continue
        i = 0
        while i < len(row_string):
            i += 1
            if row_int % 10 == 0:
                continue
            row.insert(0, row_int % 10)
            row_int = row_int // 10

        grid.append(row)

    return grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    risk = 0
    for step in path[1:]:
        row = grid[step[0]]
        col = step[1]
        risk += row[col]
    return risk


def lowest_risk(grid, row=0, col=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    first_call = not getattr(lowest_risk, "running", False)
    if first_call:
        lowest_risk.cache = {}
        lowest_risk.running = True
    try:
        if row == len(grid) - 1 and col == len(grid[0]) - 1:
            return 0
        right = float("inf")
        down = float("inf")
        if (row, col) in lowest_risk.cache:
            return lowest_risk.cache[(row, col)]
        if col < len(grid[0]) - 1:
            right = lowest_risk(grid, row, col + 1) + grid[row][col + 1]

        if row < len(grid) - 1:
            down = lowest_risk(grid, row + 1, col) + grid[row + 1][col]
        lowest_risk.cache[(row, col)] = min(right, down)
        return min(right, down)
    finally:
        if first_call:
            lowest_risk.running = False


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    neighbour_positions = []
    if row - 1 >= 0:
        neighbour_positions.append((row - 1, col))
    if row + 1 < len(grid):
        neighbour_positions.append((row + 1, col))
    if col - 1 >= 0:
        neighbour_positions.append((row, col - 1))
    if col + 1 < len(grid[0]):
        neighbour_positions.append((row, col + 1))
    return neighbour_positions


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """

    queue = [(0, (0, 0))]
    risks = {(0, 0): 0}
    optimal = []
    while len(queue) > 0:
        risk, (row, col) = heapq.heappop(queue)
        if (row, col) in optimal:
            continue
        optimal.append((row, col))
        field_neighbours = neighbours(grid, row, col)
        for neighbour in field_neighbours:
            neighbour_risk = grid[neighbour[0]][neighbour[1]]
            if not isinstance(neighbour_risk, int) or neighbour_risk < 0:
                raise ValueError(f"invalid risk at {neighbour}: {neighbour_risk}")
            if neighbour not in risks or risks[(row, col)] + neighbour_risk < risks[neighbour]:
                risks[neighbour] = risks[(row, col)] + neighbour_risk
                heapq.heappush(queue, (risks[neighbour], neighbour))
    return risks[(len(grid) - 1, len(grid[0]) - 1)]


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
