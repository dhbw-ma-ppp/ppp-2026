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
    directory = []
    files = []
    delimiter = "/"
    for line in lines:
        if line == "$ cd /":
            directory = []
        elif line == "$ cd ..":
            directory.pop()
        elif line.startswith("$ cd "):
            directory.append(line.split(" ")[2])
        elif line == "$ ls":
            continue
        elif line.startswith("dir"):
            continue
        else:
            size = int(line.split(" ")[0])
            filename = line.split(" ")[1]
            if len(directory) > 0:
                path = "/" + delimiter.join(directory) + "/" + filename
            else:
                path = "/" + filename
            files.append((path, size))
    return files


def directory_sizes(entries):
    """Return the total size of files under each directory, including root."""
    dictionary = {}

    for filename, size in entries:
        parent_directory_parts = filename.strip("/").split("/")[:-1]

        for depth in range(len(parent_directory_parts), -1, -1):
            if depth > 0:
                key = "/" + "/".join(parent_directory_parts[:depth])
            else:
                key = "/"
            dictionary[key] = dictionary.get(key, 0) + size

    return dictionary


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    sum_of_directories = 0
    for size in sizes.values():
        if size <= limit:
            sum_of_directories = sum_of_directories + size
        else:
            continue
    return sum_of_directories


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    total_size = sizes["/"]
    free_space = disk_size - total_size

    if free_space < needed_free:
        small = {}
        size_to_delete = needed_free - free_space
        for key in sizes:
            if sizes[key] >= size_to_delete:
                small[key] = sizes[key]

        minvalue = total_size

        for value in small.values():
            if value < minvalue:
                minvalue = value
        return minvalue
    else:
        return None


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.

    If path does not exist, it will return a copy of the original sizes.
    """

    remaining_sizes = {}
    deleted_sizes = {}
    for directory_path in sizes:
        if path in directory_path:
            deleted_sizes[directory_path] = sizes[directory_path]
        else:
            remaining_sizes[directory_path] = sizes[directory_path]

    for affected_directory_path in deleted_sizes:
        parent_directory_parts = affected_directory_path.strip("/").split("/")[:-1]

        for depth in range(len(parent_directory_parts), -1, -1):
            if depth > 0:
                directory_path = "/" + "/".join(parent_directory_parts[:depth])
            else:
                directory_path = "/"
            remaining_sizes[directory_path] = (
                remaining_sizes.get(directory_path, 0) - deleted_sizes[affected_directory_path]
            )

    return remaining_sizes


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
