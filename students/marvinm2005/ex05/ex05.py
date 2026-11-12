# Exercise 05. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import CAVE
from functools import lru_cache  # for function lowest_risk - improves recursion through caching
import heapq  # for function lowest_risk_any_direction() - allows to make priority queue for Dijkstra algorithm


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

    for line in text.splitlines():  # split the text in lines
        line = line.strip()
        if line:  # skips non-existent lines
            row = [
                int(char) for char in line
            ]  # list comprehension (for every single char in the line)
            grid.append(row)

    return grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    risk = 0

    for row, col in path[1:]:  # first position is skipped
        risk += grid[row][
            col
        ]  # selects the right row --> selects the right position within the row

    return risk


def lowest_risk(grid, row=0, col=0):  # recursion needed, best path is not clear
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    rows = len(grid)
    cols = len(grid[0])

    @lru_cache(
        maxsize=None
    )  # caching makes the recursion faster: remaining paths don't need to be calculated multiple times
    def solve(r, c):
        # print("Currently:", r, c)
        if r == rows - 1 and c == cols - 1:  # goal is reached
            return 0

        risks = []  # every risk stored here

        # Option 1 - go down
        if r + 1 < rows:
            down = grid[r + 1][c] + solve(
                r + 1, c
            )  # add the risk and solve for the other paths using recursion
            risks.append(down)

        # Option 2 - go right (same implementation, just with columns)
        if c + 1 < cols:
            right = grid[r][c + 1] + solve(r, c + 1)
            risks.append(right)
        # print(r, c)
        # print(risks)
        return min(risks)  # best option

    return solve(row, col)


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    result = []

    directions = [
        (-1, 0),  # up
        (1, 0),  # down
        (0, -1),  # left
        (0, 1),  # right
    ]

    for dr, dc in directions:  # for row and column changes
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):  # check if positions are valid
            result.append((new_row, new_col))  # append new (row, col) pair for one direction

    return result


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """

    # Here, the Dijkstra algorithm can be used since the grid can treated like graph with weights (risks)
    # Recursion could be problematic since you can also go backwards now --> infinite loops

    rows = len(grid)
    cols = len(grid[0])

    heap = [(0, 0, 0)]  # start of the priority queue: risk 0, row 0, column 0

    best = {(0, 0): 0}  # dict with best risk we know so far

    while True:
        risk, row, col = heapq.heappop(heap)  # entry with smallest value gets deleted

        if risk > best[(row, col)]:
            continue

        if row == rows - 1 and col == cols - 1:  # goal is reached
            return risk

        for new_row, new_col in neighbours(grid, row, col):  # reuse of function neighbours()
            new_risk = risk + grid[new_row][new_col]

            if new_risk < best.get(
                (new_row, new_col), float("inf")
            ):  # compares the risk with the one in the dict (new positions have infinite risk)
                best[(new_row, new_col)] = new_risk  # new dictionary entry or update to better risk

                heapq.heappush(heap, (new_risk, new_row, new_col))


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    example = parse_grid(EXAMPLE_TEXT)
    cave = parse_grid(CAVE)

    print("Part 1")
    print("1:", lowest_risk(example))
    print("2:", path_risk(example, EXAMPLE_PATH))

    print("Part 2")
    # print("3:", lowest_risk(cave))
    print("4:", lowest_risk_any_direction(example))
    print("5:", lowest_risk_any_direction(cave))
