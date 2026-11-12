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
    listOfRows = []
    listOfDigits = []
    for line in text.splitlines():
        if line:
            for digit in line.strip().replace("'", " "):
                listOfDigits.append(int(digit))
            listOfRows.append(listOfDigits.copy())
            listOfDigits.clear()
    return listOfRows


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    # fuer jede position in path die risk, also value an der Koordinate ausgeben
    # input sind Koordinaten, also Tupel, in Liste
    # grid ist listOfRows
    risk_sum = 0
    for step in path[1:]:
        x = step[0]
        y = step[1]
        risk = grid[x][y]
        risk_sum += risk
    return risk_sum


counter = 0


def lowest_risk(grid, row=0, col=0):
    """Return the lowest total risk from (row, col) to the bottom-right corner.

    Moves go only right or down. The risk of (row, col) itself doesn't count.
    """
    global counter
    counter = 0
    cache = [[None] * len(grid[0]) for _ in range(len(grid))]
    return lowest_risk_rekursion(grid, row, col, cache)


def lowest_risk_rekursion(grid, row, col, cache):
    global counter
    counter += 1
    lastRow = len(grid) - 1
    lastCol = len(grid[0]) - 1

    if cache[row][col] is not None:
        return cache[row][col]

    if col < lastCol and row < lastRow:
        result = min(
            (grid[row + 1][col] + lowest_risk_rekursion(grid, row + 1, col, cache)),
            (grid[row][col + 1] + lowest_risk_rekursion(grid, row, col + 1, cache)),
        )
    elif col < lastCol:
        result = grid[row][col + 1] + lowest_risk_rekursion(grid, row, col + 1, cache)
    elif row < lastRow:
        result = grid[row + 1][col] + lowest_risk_rekursion(grid, row + 1, col, cache)
    else:
        result = 0

    cache[row][col] = result
    return result


for n in (2, 3, 10):
    grid = [[1] * n for _ in range(n)]
    lowest_risk(grid)
    print(f"n: {n}, counter: {counter}")

# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""
    listOfPairs = []
    lastRow = len(grid)
    lastCol = len(grid[0])
    if (row < 0 or row > lastRow) or (col < 0 or col > lastCol):
        raise IndexError("Row: {row}, or Column: {col} are not valid")
    directions = [(row - 1, col), (row + 1, col), (row, col + 1), (row, col - 1)]
    for r, c in directions:
        if r in range(0, lastRow) and c in range(0, lastCol):
            listOfPairs.append((r, c))
    return listOfPairs


def lowest_risk_any_direction(grid):
    """Return the lowest total risk from the top-left to the bottom-right corner.

    Moves go up, down, left or right. The risk of the top-left position doesn't count.
    """
    if not grid:
        raise IndexError("No input given")
    rows = len(grid)
    cols = len(grid[0])
    goal = (rows - 1, cols - 1)
    minHeap = [(0, 0, 0)]
    distanceTable = [[float("inf")] * cols for _ in range(rows)]
    distanceTable[0][0] = 0

    while minHeap:
        cost, row, col = heapq.heappop(minHeap)
        if cost > distanceTable[row][col]:
            continue
        if row == goal[0] and col == goal[1]:
            return cost
        for r, c in neighbours(grid, row, col):
            new_cost = cost + grid[r][c]
            if new_cost < distanceTable[r][c]:
                distanceTable[r][c] = new_cost
                heapq.heappush(minHeap, (new_cost, r, c))
    return None


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
