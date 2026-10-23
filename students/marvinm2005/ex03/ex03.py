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

    lines is a list of stringsh like EXAMPLE. Paths are full paths, e.g. "/photos/trip.jpcleag",
    in the order the files appear in the transcript.
    """

    pairs = []  # list of (path, size) pairs
    current_paths = [""]  # list as a stack for file paths

    # Go through every line and enumerate
    for line_number, line in enumerate(lines, start=1):
        # check if alle entries in the list are strings
        if not isinstance(line, str):
            raise ValueError(f"Zeile {line_number}: Es wird eine Textzeile erwartet.")

        # formats the line by removing unnecessary parts (e.g. spaces)
        line = line.strip()

        if "$ cd /" in line[:6]:
            current_paths = [""]

        elif "$ cd .." in line[:7]:
            # Check if you are in the root directory
            if not current_paths:
                raise ValueError(
                    f"Zeile {line_number}: Über das Hauptverzeichnis / "
                    "kann nicht hinausgewechselt werden."
                )
            # Move to the parent directory
            current_paths.pop()

        elif "$ cd" in line[:4]:
            current_paths.append(current_paths[-1] + "/" + line[5:])

        # The case with a file we want to add to our list of (path, size) pairs
        # Files with no extension are not allowed!
        elif "." in line.split()[-1]:
            # split the line into two parts (for the file size and the path)
            parts = line.split(maxsplit=1)
            # check if both parts are available
            if len(parts) != 2:
                raise ValueError(f"Zeile {line_number}: Gültiger Dateieintrag erwartet")

            size_text, filename = parts

            # An error will be thrown if "size" cannot be casted to an integer
            try:
                size = int(size_text)
            except ValueError:
                raise ValueError(
                    f"Zeile {line_number}: Ungültige Dateigröße: {size_text!r}"
                ) from None

            # No negative file sizes allowed
            if size < 0:
                raise ValueError(f"Zeile {line_number}: Dateigrößen dürfen nicht negativ sein.")

            filepath = current_paths[-1] + "/" + line.split()[1]
            size = line.split()[0]
            pairs.append((filepath, int(size)))

        # if no one of these commands are in "line", an error will be thrown
        elif "$ ls" not in line[:4] and "dir " not in line[:4]:
            raise ValueError(f"Zeile {line_number}: Ungültiger Befehl")
    return pairs


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    pathssizes = {}
    directories = []  # Liste mit directory paths

    for entry in entries:  # für ein Paar
        path = entry[0]  #
        directories = []
        while "/" in path:
            path = path[: path.rfind("/")]

            directories.append(path)
        for directory in directories:
            groesse = int(entry[1])
            pathssizes[directory] = pathssizes.get(directory, 0) + groesse
    pathssizes["/"] = pathssizes.pop("")
    return pathssizes


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    sum = 0
    for wert in sizes.values():
        if wert < limit:
            sum += wert
    return sum


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    used_space = sizes["/"]
    additional_space = needed_free - (disk_size - used_space)
    if additional_space <= 0:
        return None

    candidates = (size for size in sizes.values() if size >= additional_space)
    return min(candidates, default=None)


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    path = "/" + path.strip("/") if path != "/" else "/"
    if path not in sizes:
        return sizes.copy()

    if path == "/":
        return {"/": 0}

    removed_size = sizes[path]
    result = {}

    for directory, size in sizes.items():
        # Every parent directory also loses the files inside `path`.
        if path.startswith(directory.rstrip("/")):
            size -= removed_size

        # A directory without any remaining files does not appear in directory_sizes.
        if size != 0:
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

    print(parse_transcript(EXAMPLE))
