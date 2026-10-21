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
    cwd = "/"        # cwd = Current Working Directory
    cwd_size = 0
    pairs = []
    sumUpNextLines = False

    for line in lines:
        if sumUpNextLines:
            if "$" in line:     # Empty Folder
                sumUpNextLines = False
                if cwd_size > 0:
                    cwd_size = 0
            elif "dir" in line:    # Another Folder listed
                pass
            else:
                cwd_size += int(line[0:line.find(" ")])
                pairs.append((cwd + line[line.find(" ")+1::], int(line[0:line.find(" ")])))

        if "$ cd " in line:
            strippedString = line.replace("$ cd ", "")
            if strippedString == "..":
                if cwd == "/":
                    pass 
                else:
                    tmp = cwd[0:-1:]
                    cwd = cwd[0:tmp.rfind("/")+1]
            elif strippedString == "/":
                cwd = "/"
            else:
                if "/" in strippedString:
                    parts = strippedString.split("/")
                    for part in parts:
                        cwd += part +"/"
                else:
                    cwd += strippedString +"/"


        if "$ ls" in line:
            sumUpNextLines = True

    print(pairs)
    return pairs


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    directories = {}

    for entry in entries:
        l = entry[0].split("/")
        for item in l:
            if "." in item:
                pass
            else:
                directories["/" + item] = 0

    for path, value in entries:
        for key in directories.keys():
            if key in path:
                directories[key] += value

    print(directories)
    return directories




def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    sum = 0
    for dir in sizes:
        sum += sizes[dir]
        if sum > limit:
            return limit
    return sum

# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    pass  # replace this line with your code


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    pass  # replace this line with your code


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
