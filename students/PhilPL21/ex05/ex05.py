# Exercise 05. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.
# from exercises.ex01.ex01 import count_letter


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
    rows = text.split("\n")
    list_of_result = []

    for row in rows:
        row = row.strip()

        if row == "":
            continue

        list_of_row = []

        for digit in row:
            list_of_row.append(int(digit))

        list_of_result.append(list_of_row)
        # print(list_of_result)
    return list_of_result


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    risk = 0
    if path == [(0, 0)]:
        return risk
    for row, col in path[1:]:
        risk += grid[row][col]
    # print(risk)
    return risk


def lowest_risk(grid, row=0, col=0, start=True, cache=None):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """

    rows = len(grid)
    cols = len(grid[0])

    # return lowest_risk_rec(grid, row, col, rows, cols)
    if cache is None:
        cache = {}

    if (row, col) in cache:
        return cache[(row, col)]

    if row == rows - 1 and col == cols - 1:
        if start:
            return 0
        else:
            return grid[row][col]

    risk = 0 if start else grid[row][col]

    if row == rows - 1:
        return risk + lowest_risk(grid, row, col + 1, False, cache)

    elif col == cols - 1:
        return risk + lowest_risk(grid, row + 1, col, False, cache)
    else:
        move_right = lowest_risk(grid, row, col + 1, False, cache)
        move_down = lowest_risk(grid, row + 1, col, False, cache)

        result = risk + min(move_right, move_down)
    cache[(row, col)] = result
    return result


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    neighbours = []
    if row > 0:
        neighbours.append((row - 1, col))
    if row < len(grid) - 1:
        neighbours.append((row + 1, col))
    if col > 0:
        neighbours.append((row, col - 1))
    if col < len(grid[0]) - 1:
        neighbours.append((row, col + 1))
    return neighbours


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    distances = {(0, 0): 0}
    visited = set()
    queue = [(0, (0, 0))]

    while len(queue) > 0:
        risk, (row, col) = heapq.heappop(queue)
        if (row, col) in visited:
            continue
        visited.add((row, col))

        if (row, col) == (len(grid) - 1, len(grid[0]) - 1):
            return risk

        for neighbour in neighbours(grid, row, col):
            if neighbour in visited:
                continue

            neighbour_risk = grid[neighbour[0]][neighbour[1]]
            new_risk = risk + neighbour_risk
            if neighbour not in distances or new_risk < distances[neighbour]:
                distances[neighbour] = new_risk
                heapq.heappush(queue, (new_risk, neighbour))

    return distances[(len(grid) - 1, len(grid[0]) - 1)]


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
