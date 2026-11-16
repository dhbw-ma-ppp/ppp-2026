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

    list_with_line = text.splitlines()
    grid = []

    for line in list_with_line:
        line = line.strip()
        if line:
            grid.append([int(x) for x in line])

    return grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    risk = 0
    for step in path[1:]:
        risk += grid[step[0]][step[1]]
    return risk


def lowest_risk(grid, row=0, col=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    import sys

    sys.setrecursionlimit(50000)
    rows = len(grid)
    cols = len(grid[0])
    memo = {}

    def find_min(row, col):
        # Ziel erreicht
        if row == rows - 1 and col == cols - 1:
            return 0

        # Ergebnis wurde schon berechnet
        if (row, col) in memo:
            return memo[(row, col)]

        down = float("inf")
        right = float("inf")

        # Nach unten
        if row + 1 < rows:
            down = grid[row + 1][col] + find_min(row + 1, col)

        # Nach rechts
        if col + 1 < cols:
            right = grid[row][col + 1] + find_min(row, col + 1)

        memo[(row, col)] = min(down, right)
        return memo[(row, col)]

    return find_min(row, col)


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    possible_positions = []
    if row - 1 >= 0:  # Prüft, ob oben Platz ist.
        possible_positions.append((row - 1, col))
    if row + 1 <= len(grid) - 1:  # Prüft, ob unten Platz ist.
        possible_positions.append((row + 1, col))
    if col - 1 >= 0:  # Prüft, ob links Platz ist.
        possible_positions.append((row, col - 1))
    if col + 1 <= len(grid[0]) - 1:  # Prüft, ob rechts Platz ist.
        possible_positions.append((row, col + 1))
    return possible_positions


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """

    def lowest_risk(pos, already_visited_positions, cost, lowest_cost):
        if pos == (len(grid) - 1, len(grid[-1]) - 1):
            if cost < lowest_cost:
                lowest_cost = cost
            return lowest_cost
        possible_ways = neighbours(grid, pos[0], pos[1])
        possible_ways.sort(
            key=lambda step: grid[step[0]][step[1]]
        )  # Es werden zuerst die Nachbarn mit dem kleinsten Weg untersucht
        for step in possible_ways:
            new_cost = cost + grid[step[0]][step[1]]
            if new_cost >= lowest_cost:
                continue
            if step in already_visited_positions:
                if already_visited_positions[step] <= new_cost:
                    continue
                else:
                    already_visited_positions[step] = new_cost
            else:
                already_visited_positions[step] = new_cost
            lowest_cost = lowest_risk(step, already_visited_positions, new_cost, lowest_cost)
        return lowest_cost

    end_lowest_risk = lowest_risk((0, 0), {(0, 0): 0}, 0, float("inf"))
    if end_lowest_risk == float("inf"):
        return 0
    else:
        return end_lowest_risk


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
