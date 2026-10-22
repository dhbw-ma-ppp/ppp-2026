# Exercise 03. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import TRANSCRIPT
from copy import deepcopy

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
    Dateipfad = []
    for line in lines:
        if line == "$ cd /":
            path = []
        elif line == "$ cd ..":
            path.pop()
        elif line.startswith("$ cd "):
            path.append(line[5:])
        else:
            lineAnfang = line.split()
            if len(lineAnfang) > 0 and lineAnfang[0].isdigit():
                size = int(lineAnfang[0])
                Dateiname = lineAnfang[1]
                if len(path) == 0:
                    route = "/" + Dateiname
                else:
                    route = "/" + "/".join(path) + "/" + Dateiname
                Dateipfad.append((route, size))
    return Dateipfad


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    sizes = {}
    for path, size in entries:
        teile = path.split("/")
        AktuellerOrdner = "/"
        sizes["/"] = sizes.get("/", 0) + size
        for i in range(1, len(teile) - 1):
            if i == 1:
                AktuellerOrdner = "/" + teile[i]
            else:
                AktuellerOrdner = AktuellerOrdner + "/" + teile[i]
            sizes[AktuellerOrdner] = sizes.get(AktuellerOrdner, 0) + size
    return sizes


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    if sizes is None:
        return "keine Größen übergeben"
    else:
        total = sum(size for size in sizes.values() if size < limit)
        return total


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    if sizes["/"] <= disk_size - needed_free:
        return None
    else:
        OrdnerzumLöschen = sizes.get("/")
        gebrauchterPlatz = needed_free - (disk_size - sizes["/"])
        if gebrauchterPlatz <= 0:
            return None
        else:
            for a in sizes:
                if sizes["/"] > sizes[a] >= gebrauchterPlatz:
                    OrdnerzumLöschen = sizes[a]
        return OrdnerzumLöschen


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    if path not in sizes:
        return sizes
    sizesCopy = sizes.copy()
    sizesCopy.pop(path)
    for Dateipfad in sizesCopy.keys():
        if Dateipfad in path:
            sizesCopy[Dateipfad] -= sizes[path]
    return sizesCopy


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
