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

# -----------------------------------------
# ----------------------- Part 1 (in class)


def parse_transcript(lines):
    """Return a list of (path, size) pairs, one per file listed in the transcript.

    lines is a list of strings like EXAMPLE. Paths are full paths, e.g. "/photos/trip.jpg",
    in the order the files appear in the transcript.
    """
    pairs = []
    point = []

    for line in lines:
        line = line.rstrip("\n")
        if not line:
            continue
        if line.startswith("$ cd"):
            directory = line[5:]

            if directory == "/":
                point = []
            elif directory == "..":
                if point:
                    point.pop()
            else:
                point.append(directory)

        elif line.startswith("$ ls") or line.startswith("dir "):
            continue

        else:
            size, filename = line.split(" ", 1)
            pairs.append(("/" + "/".join(point + [filename]), int(size)))

    return pairs


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    sizes = {}
    for path, size in entries:
        parts = list(p for p in path.split("/") if p)
        dir_parts = parts[:-1]

        sizes["/"] = sizes.get("/", 0) + size

        current = ""
        for part in dir_parts:
            current += "/" + part
            sizes[current] = sizes.get(current, 0) + size

    return sizes


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    return sum(v for k, v in sizes.items() if v <= limit)


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    used_space = sizes["/"]
    free_space = disk_size - used_space

    if free_space >= needed_free:
        return None

    required_space = needed_free - free_space
    smallest_size = float("inf")

    for size in sizes.values():
        if size >= required_space and size < smallest_size:
            smallest_size = size

    if smallest_size == float("inf"):
        return None

    return smallest_size


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    sizes_left = sizes.copy()

    if path not in sizes:
        return sizes_left

    deleted_size = sizes[path]

    for directory in list(sizes_left):
        if directory == path or directory.startswith(path + "/"):
            del sizes_left[directory]
        elif directory == "/" or path.startswith(directory + "/"):
            sizes_left[directory] -= deleted_size

    return sizes_left


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
