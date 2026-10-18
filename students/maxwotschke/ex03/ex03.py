# Exercise 03. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.
from zipfile import sizeCentralDir

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
    pair = []
    file_list = []

    for commandline in lines:
        command1 = commandline.split()[0]
        #print("commandline", commandline)
        #if len(commandline.split()) > 1:
            #command2 = commandline.split()[1]
            #if len(commandline.split()) > 2
                #command3 = commandline.split()[2]

        # elif isinstance(command1, int):
        #     path.append(commandline.split()[2])
        #     pair = ["/".join(path), command1]
        #     print("append in file_list")
        #     file_list.append(pair)
        #     path.pop()
        if len(commandline.split()) > 2 and commandline.split()[1] == "cd":

            if commandline == "$ cd /":
                path = [""]
                #print("zurück zum start")

            elif commandline.split()[2] == "..":
                if len(path) >= 1:
                    path.pop()
                    #print("ordner zurück", path)
            else:
                path.append(commandline.split()[2])
                #print ("ordner weiter", path)
        elif len(commandline.split()) > 1 and commandline.split()[0] != "$" and commandline.split()[0] != "dir":
            path.append(commandline.split()[1])
            joinedpath = "/".join(path)
            slicedjoinedpath = joinedpath[1:]
            pair = ("/" + slicedjoinedpath, int(command1))
            #print("pair:", pair)
            file_list.append(pair)
            path.pop()
            #print("append in file_list",file_list)
    #print("FINAL ERGEBNIS EINS:",file_list)
    return file_list

    # Alles Quatsch, stack zum tracken vom directory?

    # commandlist = []
    # for commandline in lines:
    #     command = commandline.split()[0]
    #     command2 = commandline.split()[1]
    #     command3 = commandline.split()[2]
    #
    #     if command == "dir":
    #         commandlist.append(list(command2))
    #
    #     if isinstance(command, int):
    #         commandlist.append(commandline)
    #
    #     if command == "$":
    #         if command2 == "cd" and command3 != "..":
    #             while command != "$":
    #                 command3.append(commandline)
    #         if command2 == "cd" and command3 == "..":
    #                 pass


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """
    #[('/notes.txt', 100), ('/photos/trip.jpg', 4000), ('/photos/summer/beach.jpg', 2500),
    #('/photos/summer/sunset.jpg', 1500), ('/music/song.mp3', 3000)]

    sizedictionary = {}
    for entry in entries:
        path = entry[0].split("/"[:])
        size = entry[1]
        temp_path = "/"
        #print("ENTRY0", path)
        #print(path.split("/")[:])
        for element in path:
        #pathwithoutdata = "/" + "/".join(path.split("/")[1:-1]) + "/"
        #print(pathwithoutdata)
        #if path.find(".") >= 0:
            if element != "":
                if temp_path in sizedictionary:
                    sizedictionary[temp_path] += int(size)
                    #print("TRUE")
                elif temp_path not in sizedictionary:
                    #print("False")
                    sizedictionary[temp_path] = int(size)
                if temp_path != "/":
                    temp_path += "/" + element
                elif temp_path == "/":
                    temp_path += element
    #print("SIZEDICTIONARY", sizedictionary)
    return sizedictionary


def small_directories_total(sizes, limit=100000):
    """Return the sum of the sizes of all directories whose total size is at most `limit`."""
    #small_directories = {path: size for path, size in sizes.items() if size <= limit}
    #total = sum(age for age in ages.values() if age >= 36)
    small_directories_sum = sum(size for size in sizes.values() if size <= limit)
    return small_directories_sum

# ---------------------------------------------------------------- Part 2 (at home)

def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.
    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    # needed free kleiner disk size?
    # alle sizes addieren, kleiner als disk size?
    # insgesamt size - alle disk sizes (grade frei), needed free - grade frei, wenn negativ muss nix deleted werden
    # directory nur mit dateien > differenz, wenn keine dann error oder so
    # davon die kleinste suchen und ausgeben
    if needed_free > disk_size:
        raise ValueError("disk_size is too small")
    used_size = sizes["/"]
    if used_size > disk_size:
        raise ValueError
    disk_free = disk_size - used_size
    blocked = needed_free - disk_free
    if blocked <= 0:
        return None
    deletable = {path: size for path, size in sizes.items() if size >= blocked}
    smallest = min(deletable.values())
    #smallest_path = [path for path, size in deletable.items() if size == smallest]
    return smallest




def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    copied_sizes = sizes.copy()
    del copied_sizes[path]
    return directory_sizes(list(copied_sizes.items()))



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
