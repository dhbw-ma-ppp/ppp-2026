# Exercise 03. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import TRANSCRIPT

EXAMPLE = [
    "$ cd /",
    "$ ls",
    "dir photos",
    "100 notes.txt",
    "dir music",
    "$ cd photos",
    "$ ls",
    "4000 trip.jpg",
    "dir summer",
    "$ cd summer",
    "$ ls",
    "2500 beach.jpg",
    "1500 sunset.jpg",
    "$ cd ..",
    "$ cd ..",
    "$ cd music",
    "$ ls",
    "3000 song.mp3",
]

# ---------------------------------------------------------------- Part 1 (in class)


def parse_transcript(lines):
    """Return a list of (path, size) pairs, one per file listed in the transcript.

    lines is a list of strings like EXAMPLE. Paths are full paths, e.g. "/photos/trip.jpg",
    in the order the files appear in the transcript.
    """
    if lines is None:
        return None

    path_size_pairs = []

    current_path = []

    for line in lines:
        first_command = line.split(" ")[0]

        if line.startswith("$ cd"):
            argument = line.split(" ")[2]

            match argument:
                case "/":
                    current_path = ["/"]
                case "..":
                    current_path.pop()
                case _:
                    current_path.append(argument + "/")

        elif first_command.isnumeric():
            second_command = line.split(" ")[1]

            current_path.append(second_command)
            path_size_pairs.append(("".join(current_path), int(first_command)))
            current_path.pop()

    return path_size_pairs


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.
    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    path_mapped_to_total_size = {}

    for entry in entries:
        path, size = entry

        directories = ["/"]

        for index, char in enumerate(path):
            if char == "/" and index > 0:
                directories.append(path[:index])

        for directory in directories:
            path_mapped_to_total_size[directory] = (
                path_mapped_to_total_size.get(directory, 0) + size
            )

    return path_mapped_to_total_size


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    return sum(size for size in sizes.values() if size <= limit)


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    if needed_free > disk_size:
        raise ValueError(
            f"needed_free ({needed_free}) must be smaller or equal to disk_size ({disk_size})"
        )

    space_to_free_up = needed_free - (disk_size - sizes["/"])

    if space_to_free_up <= 0:
        return None

    smallest_so_far = sizes["/"]

    for size in sizes.values():
        if size >= space_to_free_up and size < smallest_so_far:
            smallest_so_far = size

    return smallest_so_far


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.

    When a path that does not exist is passed, the dict will be returned unmodified.
    """
    if path not in sizes:
        return sizes

    sizes_copy = sizes.copy()
    sizes_copy.pop(path)

    for current_path in sizes_copy.keys():
        if current_path in path:
            sizes_copy[current_path] -= sizes[path]

    return sizes_copy


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    print("Part 1")
    example_sizes = directory_sizes(parse_transcript(EXAMPLE))
    print("1:", small_directories_total(example_sizes, limit=5000))
    sizes = directory_sizes(parse_transcript(TRANSCRIPT))
    print("2:", small_directories_total(sizes))

    print("Part 2")
    print("3:", directory_to_delete(sizes))
    print("4:", small_directories_total(delete_directory(sizes, "/home/backup")))
    print("2 again:", small_directories_total(sizes))
