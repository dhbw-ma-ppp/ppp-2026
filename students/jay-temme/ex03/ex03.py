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

    # checks if lines is a list
    if type(lines) is not list:
        raise TypeError("lines must be of type list")

    # checks if lines only contains strings
    for line in lines:
        if type(line) is not str:
            raise TypeError("all items in lines must be of type string")

    # creates an empty dictionary to store files (dict to avoid duplicates)
    files = dict()

    # tracks the directory the user is currently in
    current_path = [""]

    for line in lines:
        line_list = line.split(" ")

        # checks if the line navigates to the root
        if line == "$ cd /":
            current_path = [""]

        # checks if the line navigates to  navigate to the previous directory
        elif line == "$ cd ..":
            if len(current_path) > 1:
                current_path.pop()

        # checks if the line navigates to a specific directory and does that
        elif line[0:4] == "$ cd":
            directories = line[5:].split("/")

            for directory in directories:
                current_path.append(directory)

        # checks if the line lists the contents of the current directory
        elif line == "$ ls":
            pass

        # checks if the line lists a file
        elif line_list[0].isdecimal():
            file_size = int(line_list[0])
            file_name = " ".join(line_list[1:])
            file_path = "/".join(current_path)

            # adds the file to the files dict
            files[f"{file_path}/{file_name}"] = file_size

        # checks if the line lists a directory
        elif line_list[0] == "dir":
            pass

        # raises a ValueError otherwise
        else:
            raise ValueError("lines contain unknown input or output")

    return [(file_path_name, file_size) for (file_path_name, file_size) in files.items()]


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """

    # checks if entries is a list
    if type(entries) is not list:
        raise TypeError("entries must be of type list")

    # iterates through every item in entries
    for file in entries:
        # checks if file is a (string, integer) tuple
        if type(file) is not tuple or type(file[0]) is not str or type(file[1]) is not int:
            raise TypeError("all items in entries must be tuples of a string and an integer")

        # checks if all paths start with "/"
        if not file[0].startswith("/"):
            raise ValueError('all paths in entries must start with "/"')

    directories = dict()

    for file in entries:
        # seperate directories in the file path into a list
        directory = file[0].split("/")[:-1]

        file_size = file[1]

        # iterates over each directory the file is under
        for i in range(len(directory)):
            trimmed_directory = "/".join(directory[: i + 1])
            if trimmed_directory == "":
                trimmed_directory = "/"

            # adds the file size to each directory the file is under
            directories[trimmed_directory] = directories.get(trimmed_directory, 0) + file_size

    return directories


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""

    # checks if sizes is a dictionary
    if type(sizes) is not dict:
        raise TypeError("sizes must be of type dictionary")

    # checks if all values in sizes are integers
    for size in sizes.values():
        if type(size) is not int:
            raise TypeError("all values in sizes must be integers")

    # checks if disk_size is an integer
    if type(limit) is not int:
        raise TypeError("limit must be of type integer")

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

    # checks if sizes is a dictionary
    if type(sizes) is not dict:
        raise TypeError("sizes must be of type dictionary")

    # checks if disk_size is an integer
    if type(disk_size) is not int:
        raise TypeError("disk_size must be of type integer")

    # checks if disk_size is an integer
    if type(needed_free) is not int:
        raise TypeError("needed_free must be of type integer")

    # checks if needed_free is less than disk_size
    if disk_size < needed_free:
        raise ValueError("needed_free must not be greater than disk_size")

    # checks if all values in sizes are integers
    for size in sizes.values():
        if type(size) is not int:
            raise TypeError("all values in sizes must be integers")

    # checks if all keys in sizes are valid directories
    for directory in sizes:
        if not directory.startswith("/"):
            raise ValueError('all keys in sizes must start with "/"')

    # checks if a root directory exists in sizes
    if "/" not in sizes:
        raise ValueError('"/" must be a key in sizes')

    # checks if enough space is already free
    if sizes["/"] <= disk_size - needed_free:
        return None

    # minimum size of directory to delete
    minimum = sizes["/"]

    # iterates through sizes to check for the smallest directory to delete
    for directory, size in sizes.items():
        # checks if the directory would free enough space
        if sizes["/"] - size < disk_size - needed_free:
            # checks if the size is a new minimum size
            if size < minimum:
                minimum = size

    return minimum


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    Raises a ValueError if `path` is not in `sizes`.
    """

    # checks if sizes is a dictionary
    if type(sizes) is not dict:
        raise TypeError("sizes must be of type dictionary")

    # checks if path is a string
    if type(path) is not str:
        raise TypeError("path must be of type string")

    # checks if path is in sizes
    if path not in sizes:
        raise ValueError("specified directory does not exist")

    # checks if all values in sizes are integers
    for size in sizes.values():
        if type(size) is not int:
            raise TypeError("all values in sizes must be integers")

    new_sizes = dict()

    for directory in sizes:
        # checks if path is directory
        if path == directory:
            # does nothing
            pass

        # checks if path is under directory
        elif set(directory.split("/")) <= set(path.split("/")):
            # adds directory and size with the size of path subtracted to new_sizes
            new_sizes[directory] = sizes[directory] - sizes[path]

        # checks if directory is under path
        elif set(path.split("/")) <= set(directory.split("/")):
            # doesn't add directory since it's getting deleted
            pass

        else:
            # adds unrelated directories to new_sizes without changing them
            new_sizes[directory] = sizes[directory]

    return new_sizes


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
