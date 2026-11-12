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
    final_grid = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        row = []
        for digit_at_position in line:
            row.append(int(digit_at_position))
        final_grid.append(row)
    return final_grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    total_risk = 0
    entered_positions = path[1:]
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (row, col) in entered_positions:
                total_risk += grid[row][col]
    return total_risk


def lowest_risk(grid, row=0, col=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    last_row = len(grid) - 1
    last_col = len(grid[0]) - 1
    memory = {(last_row, last_col): 0}

    def risk_from(row, col):
        current_position = (row, col)
        if current_position in memory:
            return memory[current_position]
        possible_risk = []
        if col < last_col:
            right_risk = grid[row][col + 1] + risk_from(row, col + 1)
            possible_risk.append(right_risk)
        if row < last_row:
            down_risk = grid[row + 1][col] + risk_from(row + 1, col)
            possible_risk.append(down_risk)
        memory[current_position] = min(possible_risk)
        return memory[current_position]

    return risk_from(row, col)


# Explanation for Part 2 Exercise 1
# I tried it with recursion first (for part 1), however this meant, that it would always call lowest_risk exponentially
# which resulted in 100.000s of calls for 10 x 10 grid, which is why I used a different method inside lowest_risk,
# so I don't need to call the entire method, but instead only the necessary parts,
# while also saving these risk values in a dictionary

# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    neighbor_positions = []
    last_row = len(grid) - 1
    last_col = len(grid[0]) - 1
    if row > 0:  # checks if there is a upper neighbor
        neighbor_positions.append((row - 1, col))
    if row < last_row:  # checks if there is lower neighbor
        neighbor_positions.append((row + 1, col))
    if col > 0:  # checks if there is a
        neighbor_positions.append((row, col - 1))
    if col < last_col:
        neighbor_positions.append((row, col + 1))
    return neighbor_positions


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    rows = len(grid)
    cols = len(grid[0])
    best = []
    for row in grid:
        best.append([None] * cols)
    best[0][0] = 0
    changed = True
    while changed:
        changed = False
        for row in range(rows):
            for col in range(cols):
                for next_row, next_col in neighbours(grid, row, col):
                    new_risk = best[row][col] + grid[next_row][next_col]
                    if best[next_row][next_col] is None or new_risk < best[next_row][next_col]:
                        best[next_row][next_col] = new_risk
                        changed = True
    return best[rows - 1][cols - 1]


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
