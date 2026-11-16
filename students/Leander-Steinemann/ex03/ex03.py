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
    currentdir = ""
    listofpairs = []
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for line in lines:
        if line[0] in numbers:
            pairs = line.split(" ", 1)
            listofpairs.append((currentdir + pairs[1], int(pairs[0])))
        elif line.startswith("$ cd /"):
            currentdir = "/"
        elif line.startswith("$ cd .."):
            if currentdir == "/":
                continue
            a = currentdir.split("/")[-2]
            currentdir = currentdir[: len(currentdir) - (len(a) + 1)]
        elif line.startswith("$ cd "):
            currentdir += line[5:] + "/"
        else:  # Könnte man lassen aber finde es klarer, dass man weiß was passiert, wenn man kein $ cd oder eine Datei hat.
            continue
    return listofpairs


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    mapDirSize = {"/": 0}
    for pair in entries:
        a = pair[0].split("/")
        tempdir = "/"
        for rep in a[: len(a)]:
            if rep == "":
                continue
            if tempdir in mapDirSize:
                mapDirSize[tempdir] += int(pair[1])
            else:
                mapDirSize[tempdir] = int(pair[1])
            if tempdir == "/":
                tempdir += rep
            else:
                tempdir += "/" + rep
    return mapDirSize


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    return sum(size for size in sizes.values() if size <= limit)


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    smallestDir = sizes["/"]
    currentsize = sizes["/"]
    spaceNeededToBeFreed = needed_free - (disk_size - currentsize)
    if spaceNeededToBeFreed <= 0:
        return None
    else:
        for dir in sizes:
            if sizes[dir] < smallestDir and sizes[dir] >= spaceNeededToBeFreed:
                smallestDir = sizes[dir]
    return smallestDir


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    When path is not included in sizes i think the function should raise a KeyError
    """
    if path not in sizes:
        raise KeyError(f"Directory not found: {path}")
    newDict = {}
    a = path.split("/")
    b = a[: len(a) - 1]
    listPathInDir = []  # Diese Liste soll alle Directories enthalten, in denen path ist.
    tempDir = ""
    for dirstep in b:
        if dirstep == "":
            listPathInDir.append("/")
            continue
        tempDir += "/" + dirstep
        listPathInDir.append(tempDir)
    for pair in sizes:
        if pair.startswith(path):
            continue
        else:
            if pair in listPathInDir:
                newDict[pair] = sizes[pair] - sizes[path]
            else:
                newDict[pair] = sizes[pair]
    return newDict


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
