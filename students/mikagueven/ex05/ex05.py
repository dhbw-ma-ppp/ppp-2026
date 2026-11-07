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
calls = 0


def parse_grid(text):
    """Return the grid in `text` as a list of rows, each a list of ints.

    `text` has one row per line and one digit per position. Blank lines and spaces at the
    start or end of a line don't matter.
    """
    rows = text.replace(" ", "").split()  # clean up string and split lines to list rows[]
    grid = []
    for i in rows:
        grid.append([int(n) for n in i])
    return grid


"""(constant) EXAMPLE_PATH: list[tuple[int, int]] = [
 (0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 3), (1, 4),
 (2, 4), ..."""


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    total_risk = 0
    for instruction in path:
        if instruction[0] == 0 and instruction[1] == 0 and len(path) == 1:
            return 0
        elif instruction[0] == 0 and instruction[1] == 0:
            continue
        else:
            total_risk += grid[instruction[0]][instruction[1]]
    return total_risk


def lowest_risk(grid, row=0, col=0, cache=None):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    # counter
    global calls
    calls += 1
    # Cache (Memoization)
    if cache is None:
        cache = {}

    if (row, col) in cache:
        return cache[(row, col)]

    # at goal (bottom right of grid)
    if row == len(grid) - 1 and col == len(grid[0]) - 1:
        return 0

    # last row
    elif row == len(grid) - 1:
        result = grid[row][col + 1] + lowest_risk(grid, row, col + 1, cache)
        cache[(row, col)] = result
        return result

    # last col
    elif col == len(grid[0]) - 1:
        result = grid[row + 1][col] + lowest_risk(grid, row + 1, col, cache)
        cache[(row, col)] = result
        return result

    # normal (in between grid)
    else:
        cost_right = grid[row][col + 1] + lowest_risk(grid, row, col + 1, cache)

        cost_down = grid[row + 1][col] + lowest_risk(grid, row + 1, col, cache)

        result = min(cost_right, cost_down)
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
    if col < len(grid[0]) - 1:
        neighbours.append((row, col + 1))
    if col > 0:
        neighbours.append((row, col - 1))
    return neighbours


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    best = {(0, 0): 0}
    todo = [(0, 0)]

    while todo:
        # take any position (here: starting at 0,0)
        row, col = todo.pop()

        # look at all neighbours
        for nr, nc in neighbours(grid, row, col):
            # risk at current point
            current_risk = best[(row, col)]

            # risk of the neighbour
            neighbour_risk = grid[nr][nc]

            # risk if we move there
            new_risk = current_risk + neighbour_risk

            # never saw the neighbour
            if (nr, nc) not in best:
                best[(nr, nc)] = new_risk
                todo.append((nr, nc))

            # found a better way (less risk)
            elif new_risk < best[(nr, nc)]:
                best[(nr, nc)] = new_risk
                todo.append((nr, nc))

    return best[(len(grid) - 1, len(grid[0]) - 1)]


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    example = parse_grid(EXAMPLE_TEXT)
    cave = parse_grid(CAVE)

    print("Part 1")
    print("1:", lowest_risk(example))
    print("2:", path_risk(example, EXAMPLE_PATH))

    # Tests
    for size in [2, 3, 10]:
        grid = [[1] * size for _ in range(size)]
        calls = 0
        lowest_risk(grid)
        print(f"{size}x{size}: {calls}")

    print("Part 2")
    print("3:", lowest_risk(cave))
    print("4:", lowest_risk_any_direction(example))
    print("5:", lowest_risk_any_direction(cave))
