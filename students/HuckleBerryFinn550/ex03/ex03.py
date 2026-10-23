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
    pairs = []
    root = []
    if lines is not None and isinstance(lines, list):
        for entry in lines:
            entries = entry.split()
            if entries[1] == "cd":
                if entries[2] == "/":
                    root.clear()
                elif entries[2] == "..":
                    if len(root) >= 1:
                        root.pop()
                else:
                    root.append(entries[2])
            elif not entry.startswith("$ ls") and not entry.startswith("dir"):
                root.append(entries[1])
                pair = ("/" + "/".join(root), int(entries[0]))
                pairs.append(pair)
                root.pop()
    else:
        raise TypeError("Invalid transcript format.")
    return pairs


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    pathSize = {}
    totalSize = 0

    for entry in entries:
        path = entry[0]
        number = entry[1]
        pathSplitted = path.split("/")
        totalSize += number

        for i in range(len(pathSplitted)):
            root = "/".join(pathSplitted[:-i])
            pathSize.update({root: pathSize.get(root, 0) + number})

    pathSize.update({"/": totalSize})
    return pathSize


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    sumUnderLimit = sum(s for s in sizes.values() if s <= limit)
    return sumUnderLimit


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    currentlyUsed = sizes.get("/")
    if disk_size - currentlyUsed >= needed_free:
        return None
    else:
        stillNeededSpace = needed_free - (disk_size - currentlyUsed)
        smallestDirectory = sizes.get("/")
        for s in sizes.values():
            if stillNeededSpace <= s < smallestDirectory:
                smallestDirectory = s
        return smallestDirectory


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change. If path doesn't exist, raises ValueError.
    """
    dictAfterDeletion = {}
    if path in sizes:
        pathSize = sizes.get(path)
        pathNameSplitted = path.split("/")
        significantName = str(pathNameSplitted[1])
        for key in sizes.keys():
            if key == "/":
                dictAfterDeletion.update({key: sizes.get(key) - pathSize})
            elif significantName in key:
                if sizes.get(key) - pathSize != 0:
                    dictAfterDeletion.update(
                        {key: sizes.get(key) - pathSize}
                    )  # path-deleted object
            else:
                dictAfterDeletion[key] = sizes.get(key)
        dictAfterDeletion.update({"": sizes.get("/") / pathSize})
        del dictAfterDeletion[""]
        return dictAfterDeletion
    else:
        raise ValueError("Directory path does not exist")


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
