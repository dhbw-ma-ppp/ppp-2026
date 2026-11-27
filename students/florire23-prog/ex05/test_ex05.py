from ex05 import (
    EXAMPLE_PATH,
    EXAMPLE_TEXT,
    lowest_risk,
    lowest_risk_any_direction,
    neighbours,
    parse_grid,
    path_risk,
)

# ---------------------------------------------------------------- Part 1


def test_parse_grid():
    assert parse_grid("12\n34\n") == [[1, 2], [3, 4]]


def test_parse_grid_blank_lines_and_spaces():
    assert parse_grid("\n  12 \n34\n\n") == [[1, 2], [3, 4]]


def test_parse_grid_example():
    grid = parse_grid(EXAMPLE_TEXT)
    assert len(grid) == 5
    assert grid[1] == [1, 9, 1, 1, 1]


def test_path_risk_start_only():
    assert path_risk([[5]], [(0, 0)]) == 0


def test_path_risk_example_path():
    assert path_risk(parse_grid(EXAMPLE_TEXT), EXAMPLE_PATH) == 12


def test_lowest_risk_one_position():
    assert lowest_risk([[5]]) == 0


def test_lowest_risk_two_by_two():
    assert lowest_risk([[1, 2], [3, 4]]) == 6
    assert lowest_risk([[1, 9], [1, 1]]) == 2


def test_lowest_risk_three_by_three():
    assert lowest_risk([[1, 1, 9], [2, 9, 9], [1, 1, 1]]) == 5


def test_lowest_risk_example():
    assert lowest_risk(parse_grid(EXAMPLE_TEXT)) == 16


def test_lowest_risk_from_the_middle():
    grid = parse_grid(EXAMPLE_TEXT)
    assert lowest_risk(grid, 3, 2) == 11
    assert lowest_risk(grid, 4, 0) == 28


def test_lowest_risk_does_not_change_grid():
    grid = parse_grid(EXAMPLE_TEXT)
    before = parse_grid(EXAMPLE_TEXT)
    lowest_risk(grid)
    assert grid == before


# ---------------------------------------------------------------- Part 2
# Add at least two tests of your own below. One of them must use a grid of your own in which
# moving in any direction is cheaper than moving only right and down.


def test_neighbours_corner():
    grid = parse_grid(EXAMPLE_TEXT)
    assert sorted(neighbours(grid, 0, 0)) == [(0, 1), (1, 0)]


def test_neighbours_middle():
    grid = parse_grid(EXAMPLE_TEXT)
    assert sorted(neighbours(grid, 2, 2)) == [(1, 2), (2, 1), (2, 3), (3, 2)]


def test_lowest_risk_any_direction_example():
    assert lowest_risk_any_direction(parse_grid(EXAMPLE_TEXT)) == 12


def test_lowest_risk_any_direction_small():
    assert lowest_risk_any_direction([[5]]) == 0
    assert lowest_risk_any_direction([[1, 2], [3, 4]]) == 6


# --------------------------Eigene Tests--------------------------#


def test_lowest_risk_any_direction_detour():
    """Umwege nach oben/links lohnen sich: 4 statt 16."""
    grid = [[1, 1, 1, 9], [9, 9, 1, 9], [1, 1, 1, 9], [1, 9, 9, 9], [1, 1, 1, 1]]

    # nur rechts und runter:
    assert lowest_risk(grid) == 15

    # jede Richtung erlaubt (runter, hoch, rechts, links):
    assert lowest_risk_any_direction(grid) == 11


def test_lowest_risk_any_direction_eine_zeile():
    """In einer einzelnen Zeile gibt es nur einen Weg."""
    grid = [[1, 2, 3, 4, 5]]

    # Startfeld zählt nicht: 2 + 3 + 4
    assert lowest_risk_any_direction(grid) == 14


def test_lowest_risk_any_direction_does_not_change_grid():
    """Die Funktion darf das Gitter nicht verändern."""
    grid = parse_grid(EXAMPLE_TEXT)
    vorher = parse_grid(EXAMPLE_TEXT)

    lowest_risk_any_direction(grid)

    assert grid == vorher
