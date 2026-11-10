from ex03 import (
    EXAMPLE,
    delete_directory,
    directory_sizes,
    directory_to_delete,
    parse_transcript,
    small_directories_total,
)

EXAMPLE_ENTRIES = [
    ("/notes.txt", 100),
    ("/photos/trip.jpg", 4000),
    ("/photos/summer/beach.jpg", 2500),
    ("/photos/summer/sunset.jpg", 1500),
    ("/music/song.mp3", 3000),
]

# ---------------------------------------------------------------- Part 1


def test_parse_transcript_example():
    assert parse_transcript(EXAMPLE) == EXAMPLE_ENTRIES


def test_parse_transcript_cd_root():
    lines = ["$ cd /", "$ cd a", "$ cd b", "$ cd /", "$ cd c", "$ ls", "5 x.txt"]
    assert parse_transcript(lines) == [("/c/x.txt", 5)]


def test_directory_sizes_root():
    sizes = directory_sizes(EXAMPLE_ENTRIES)
    assert sizes["/"] == 11100


def test_directory_sizes_nested():
    sizes = directory_sizes(EXAMPLE_ENTRIES)
    assert sizes["/photos"] == 8000
    assert sizes["/photos/summer"] == 4000


def test_small_directories_total():
    sizes = directory_sizes(EXAMPLE_ENTRIES)
    assert small_directories_total(sizes, limit=5000) == 7000


# ---------------------------------------------------------------- Part 2
# Add at least two tests of your own below, for the Part 2 functions.
# One of them must check that delete_directory does not change `sizes`.


def test_directory_to_delete():
    sizes = directory_sizes(EXAMPLE_ENTRIES)
    assert directory_to_delete(sizes, disk_size=13000, needed_free=5400) == 4000


def test_delete_directory():
    sizes = directory_sizes(EXAMPLE_ENTRIES)
    assert delete_directory(sizes, "/photos/summer") == {
        "/": 7100,
        "/photos": 4000,
        "/music": 3000,
    }


def test_delete_does_not_change_original_sizes():
    """Input: the given dictionary sizes; delete /photos/summer
    expected result: the result contains the updated directory sizes, while the original dictionary remains unchanged
    case covered: correct size calculation and protection of the original dictionary"""
    sizes = {
        "/": 9500,
        "/photos": 6500,
        "/photos/summer": 2500,
        "/music": 3000,
    }

    original = sizes.copy()

    result = delete_directory(sizes, "/photos/summer")

    assert result == {
        "/": 7000,
        "/photos": 4000,
        "/music": 3000,
    }
    assert sizes == original


def test_directory_to_delete_when_enough_space_is_free():
    """input: total disk space is 5000 units, 1000 units are used, and at least 2000 units must be free
    expected result: None, because 4000 units are already free
    case covered: no directory needs to be deleted"""
    sizes = {"/": 1000, "/home": 1000}

    assert (
        directory_to_delete(
            sizes,
            disk_size=5000,
            needed_free=2000,
        )
        is None
    )
