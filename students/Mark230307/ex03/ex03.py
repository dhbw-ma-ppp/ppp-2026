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
        return -1
    help = []
    files = []
    for line in lines:
        if line == "$ cd /":
            help = []
        elif line == "$ cd ..":
            if help:
                help.pop()
        elif line.startswith("$ cd "):
            folder = line[5:]
            help.append(folder)
        elif line.startswith("$"):
            continue
        elif line.startswith("dir "):
            continue
        else:
            size, name = line.split(" ", 1)
            path = "/" + "/".join(help + [name])
            files.append((path, int(size)))
    return files


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    if entries is None:
        return -1
    sizes = {"/": 0}
    for path, size in entries:
        sizes["/"] += size
        parts = path.strip("/").split("/")
        current = ""
        for folder in parts[:-1]:
            current += "/" + folder
            if current not in sizes:
                sizes[current] = 0
            sizes[current] += size
    return sizes


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    total = 0
    for directory, size in sizes.items():
        if size <= limit:
            total += size
    return total


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
    missing_space = needed_free - free_space
    smallest = None
    for directory, size in sizes.items():
        if size >= missing_space:
            if smallest is None or size < smallest:
                smallest = size
    return smallest


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.

    If path is not found in sizes, it will return sizes completely unchanged, since there was
    never a path to be deleted in the first place.
    """
    if path not in sizes:
        return sizes
    result = {}
    deleted_size = sizes[path]
    for directory, size in sizes.items():
        if directory == path or directory.startswith(path + "/"):
            continue
        elif path.startswith(directory + "/") or directory == "/":
            result[directory] = size - deleted_size
        else:
            result[directory] = size
    return result


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
