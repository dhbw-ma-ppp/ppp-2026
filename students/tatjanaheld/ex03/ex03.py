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

    result = []
    pfad = []

    for line in lines:
        if line == "$ cd /":
            pfad = []
        elif line == "$ cd ..":
            pfad.pop()
        elif line.startswith("$ cd "):
            pfad.append(line[5:])
        elif line == "$ ls" or line.startswith("dir "):
            pass
        else:
            teile = line.split()
            groesse = int(teile[0])
            name = teile[1]

            voller_pfad = ""
            for ordner in pfad:
                voller_pfad = voller_pfad + "/" + ordner
            voller_pfad = voller_pfad + "/" + name

            result.append((voller_pfad, groesse))

    return result


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    result = {}
    for pfad, groesse in entries:
        teile = pfad.split("/")
        ordner = teile[1:-1]

        if "/" not in result:
            result["/"] = 0
        result["/"] = result["/"] + groesse

        aktuell = ""
        for name in ordner:
            aktuell = aktuell + "/" + name
            if aktuell not in result:
                result[aktuell] = 0
            result[aktuell] = result[aktuell] + groesse

    return result


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""

    summe = 0
    for ordner in sizes:
        if sizes[ordner] <= limit:
            summe = summe + sizes[ordner]
    return summe


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """

    belegt = sizes["/"]
    frei = disk_size - belegt
    fehlt = needed_free - frei

    if fehlt <= 0:
        return None

    kleinster = None
    for ordner in sizes:
        groesse = sizes[ordner]
        if groesse >= fehlt:
            if kleinster is None or groesse < kleinster:
                kleinster = groesse

    return kleinster


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    if path == "/":
        return {}
    if path not in sizes:
        return dict(sizes)

    weg = sizes[path]
    neu = {}
    for ordner in sizes:
        if ordner == path or ordner.startswith(path + "/"):
            continue

        groesse = sizes[ordner]
        if ordner == "/" or path.startswith(ordner + "/"):
            groesse = groesse - weg
        neu[ordner] = groesse
    return neu


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
