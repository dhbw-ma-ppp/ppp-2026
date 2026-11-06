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
    path = []
    files = []

    for line in lines:
        command = line.split()[0]
        if line.split()[0].isdigit is False:
            raise ValueError
        elif len(line.split()) > 2 and line.split()[1] == "cd":
            if line == "$ cd /":
                path = [""]
            elif line.split()[2] == "..":
                if len(path) >= 1:
                    path.pop()
            else:
                path.append(line.split()[2])
        elif len(line.split()) > 1 and line.split()[0] != "$" and line.split()[0] != "dir":
            path.append(line.split()[1])
            joinedpath = "/".join(path)
            slicedjoinedpath = joinedpath[1:]
            pair = ("/" + slicedjoinedpath, int(command))
            files.append(pair)
            path.pop()
    return files


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    sizedictionary = {}
    for entry in entries:
        path = entry[0].split("/"[:])
        size = entry[1]
        temp_path = "/"

        for element in path:
            if element != "":
                if temp_path in sizedictionary:
                    sizedictionary[temp_path] += int(size)
                elif temp_path not in sizedictionary:
                    sizedictionary[temp_path] = int(size)
                if temp_path != "/":
                    temp_path += "/" + element
                elif temp_path == "/":
                    temp_path += element
    return sizedictionary


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
        raise ValueError("disk_size is too small")
    used = sizes["/"]
    if used > disk_size:
        raise ValueError
    disk_free = disk_size - used
    blocked = needed_free - disk_free
    if blocked <= 0:
        return None
    deletable = {path: size for path, size in sizes.items() if size >= blocked}
    smallest = min(deletable.values())
    return smallest


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    copy = sizes.copy()
    if path not in copy:
        return copy
    size_to_delete = copy[path]
    del copy[path]
    splitted_path = path.split("/")
    i = -1

    for path_element in splitted_path:
        path_with_no_delete = "/".join(splitted_path[:i])
        if path_with_no_delete != "":
            copy[path_with_no_delete] = copy[path_with_no_delete] - size_to_delete
        i = i - 1
    copy["/"] = copy["/"] - size_to_delete
    return copy


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
