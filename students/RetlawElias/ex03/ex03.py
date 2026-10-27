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
    # None Exception
    if lines is None:
        return None

    if type(lines) is not list:
        return None

    cwd = []
    entries = []

    for line in lines:
        if line.startswith("$ cd "):
            destination = line[5:]
            if destination == "/":  # root directory case
                cwd = []
            elif destination == "..":  # previous directory case
                if cwd:
                    cwd.pop()
            else:
                cwd.append(destination)  # next directory case
        elif line.startswith("$") or line.startswith("dir "):
            continue
        else:
            size_text, filename = line.split(" ", 1)
            size = int(size_text)
            path_parts = cwd + [filename]
            path = "/" + "/".join(path_parts)
            entries.append((path, size))
    return entries


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    sizes = {"/": 0}

    for path, size in entries:
        parts = path.strip("/").split("/")

        directory = "/"

        for part in parts[:-1]:
            if directory == "/":
                directory = "/" + part
            else:
                directory += "/" + part

            sizes.setdefault(directory, 0)
            sizes[directory] += size

        sizes["/"] += size

    return sizes


def small_directories_total(sizes, limit=100000):
    """Sum the sizes of directories at or below the limit."""
    sum = 0

    for size in sizes.values():
        if size <= limit:
            sum += size

    return sum


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    used = sizes["/"]
    candidates = []
    free = disk_size - used
    required = needed_free - free

    if required <= 0:
        return None

    for size in sizes.values():
        if size >= required:
            candidates.append(size)

    if not candidates:
        return None

    return min(candidates)


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    result = sizes.copy()

    if path not in result:
        return result

    deleted_size = result[path]

    for directory in list(result):
        if directory == path or directory.startswith(path.rstrip("/") + "/"):
            del result[directory]

    parent = path.rstrip("/").rsplit("/", 1)[0] or "/"

    while True:
        if parent in result:
            result[parent] -= deleted_size

        if parent == "/":
            break

        parent = parent.rsplit("/", 1)[0] or "/"
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
