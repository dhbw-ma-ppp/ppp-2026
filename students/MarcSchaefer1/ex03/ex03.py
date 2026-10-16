# Exercise 03. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import TRANSCRIPT
import copy

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

    current_path = ""
    ReturnList = []

    ints = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    for element in lines:
        if element[0] == "$":
            if element[2:4] == "cd" and element[5:7] != "..":
                if element[5] != "/":
                    current_path += element[5:] + "/"
                else:
                    current_path = "/"

            elif element[5:7] == "..":
                current_path = current_path.rstrip("/").rsplit("/", 1)[0] + "/"

                # entferne rechtes / mit .rstrip
                # teile bei dem nächsten / von rechts mit rsplit
                # wähle das erste Element, den verbleibenden Pfad mit [0]

            elif element[2:4] == "ls":
                pass

        elif element[0:3] == "dir":
            pass

        else:
            pos = 0
            size = ""

            for char in element:
                if char in ints:
                    size = size + char
                    pos += 1
                else:
                    break

            size = int(size)
            name = element[pos + 1 :]

            ReturnList.append((current_path + name, size))

    return ReturnList


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """

    returnDict = {"/": 0}

    for obj in entries:
        Path = obj[0]
        Size = obj[1]
        Stack = []

        for dir in Path.split("/")[:-1]:
            Stack.append(dir)

        dirPath = ""

        for dir in Stack:
            if dir == "":  # Urpsrung / wird Abgeschnitten
                returnDict["/"] += Size
            else:
                dirPath += "/" + dir  # Path wird tiefer verfolgt

                if dirPath not in returnDict:
                    returnDict[dirPath] = Size  # neu angelegt falls nicht enthalten
                else:
                    returnDict[dirPath] += Size  # erhöht falls enthalten

    return returnDict


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""

    total = 0

    for size in sizes.values():
        if size < limit:
            total += size

    return total


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    root = sizes["/"]
    freeSpace = disk_size - root

    toBeFreed = needed_free - freeSpace

    SmallestOption = ("", float("inf"))

    if toBeFreed > 0:
        for path, size in sizes.items():
            if size >= toBeFreed:
                if size < SmallestOption[1]:
                    SmallestOption = (path, size)

        return SmallestOption[1]

    else:
        return None


def delete_directory(sizes, path):
    """
    Return a new dict of directory sizes, as if the directory `path` had been deleted.
    If path is not in sizes return the unchanged sizes, as path is not in it, it is automatically removed.
    """

    newDir = copy.deepcopy(sizes)  # deepcopy shallow copy will still change sizes

    prefix = path.rstrip("/") + "/"  # Einheitlichkeit für paths mit / und ohne / am ende

    contained = False

    for obj in list(newDir):
        if obj == path or obj.startswith(prefix):
            del newDir[obj]
            contained = True

    if not contained:
        return newDir

    parent = path.rstrip("/").rsplit("/", 1)[0] or "/"  # Direktes parent dir

    while True:
        if parent in newDir:
            newDir[parent] -= sizes[path]  # Parent wird in größe reduziert

        if parent == "/":
            break

        parent = parent.rsplit("/", 1)[0] or "/"  # Schritt nach außen

    return newDir


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
