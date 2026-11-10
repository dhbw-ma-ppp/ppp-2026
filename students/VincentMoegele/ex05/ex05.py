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
    input_rows = text.splitlines()
    grid = []
    for row in input_rows:
        row.strip("")
        if row != "":
            grid.append([int(digit) for digit in row])
    return grid


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    total_risk = 0
    for row, col in path[1:]:
        total_risk = total_risk + grid[col][row]
    return total_risk



def lowest_risk(grid, row=0, col=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """

    max_row_count = len(grid) - 1
    max_col_count = len(grid[0]) - 1
    visited = {}
    def from_here(row, col):

        if (row, col) in visited:
            return visited[(row, col)]
        
        if row == max_row_count and col == max_col_count:
            return 0
        
        values = []
        if row < max_row_count:
            values.append(from_here(row + 1, col) + grid[row + 1][col])

        if col < max_col_count:
            values.append(from_here(row, col + 1) + grid[row][col + 1])

        visited[(row, col)] = min(values)
        return visited[(row, col)]
 


    return from_here(row, col)



# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    neighbour_left = (row, col - 1)
    neighbour_right = (row, col + 1)
    neighbour_above = (row - 1, col)
    neighbour_below = (row + 1, col)
    max_row_count = len(grid) - 1
    max_col_count = len(grid[0]) - 1
    results = []

    if col != 0:
        results.append(neighbour_left)

    if col != max_col_count:
        results.append(neighbour_right)

    if row != 0:
        results.append(neighbour_above)

    if row != max_row_count:
        results.append(neighbour_below)

    return results                       




def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    pass  # replace this line with your code


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    example = parse_grid(EXAMPLE_TEXT)
    cave = parse_grid(CAVE)
    two_two = parse_grid("12\n34")
    three_three = parse_grid("123\n456\n789")
    ten_ten = [[i * 10 + j for j in range(10)] for i in range(10)]
    

    print("Part 1")
    print("1:", lowest_risk(example))
    print("2:", path_risk(example, EXAMPLE_PATH))

    print("Part 2")
    print("3a")
    print(lowest_risk(two_two))
    print("3b")
    print(lowest_risk(three_three))
    print("3c")
    print(lowest_risk(ten_ten))
    print("3:", lowest_risk(cave))
    #print("4:", lowest_risk_any_direction(example))
    #print("5:", lowest_risk_any_direction(cave))
