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
# Diese Funktion gibt den oberen path der Eingabe zurück
def delete_till(path, zeichen):
    if path == "/":
        return "/"
    path = path[:-1]
    for i in range(len(path) - 1, 0, -1):
        if path[i] == zeichen:
            path = path[:-1]
            break
        path = path[:-1]
    return path


# Gibt alle Directories zurück von entries
def directory(entries):
    L = []
    for filename, size in entries:
        direct = filename
        for i in range(filename.count("/")):
            direct = delete_till(direct, "/")
            if direct not in L:
                L.append(direct)
    return L


def parse_transcript(lines):
    entries = []
    directory_name = "/"
    number = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in lines:
        # geht alle $ cd möglichkeiten durch mit .. zum root wechseln und tiefer gehen
        if "$ cd " in i:
            if i[5:] == "..":
                directory_name = delete_till(directory_name, "/")
                if directory_name != "/":
                    directory_name += "/"
            elif i[-1] == "/":
                directory_name = "/"
            else:
                directory_name += i[5:] + "/"
        # wenn eine Nummer da ist Speichert er den directory mit dem filenamen und ihre größe als int
        if i[0] in number:
            size, filename = i.split(" ")
            entries.append((directory_name + filename, int(size)))

    return entries


def directory_sizes(entries):
    sizes = {}
    path = directory(entries)
    # geht durch alle directories und schaut ob die dateien in allen Entries dazu gehören um die größen zu addieren
    for direct in path:
        eigenersize = 0

        for filename, size in entries:
            # ein direct Name kann am anfang 2 mal vorhanden sein
            # zb /Baum /Baumstamm aber der root '/' darf net '//' werden
            direct_tree = direct
            if direct != "/":
                direct_tree = direct + "/"

            if filename.startswith(direct_tree):
                eigenersize += size

        sizes[direct] = eigenersize

    return sizes


# iteriert durch sizes und addiert ihrer value die kleiner limit ist
def small_directories_total(sizes, limit=100000):
    comb_size = 0
    for size in sizes.values():
        if size <= limit:
            comb_size += size
    return comb_size


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50_000_000, needed_free=20_000_000):
    # needed ist der freizugebene platz, fall <=0 gib None zurück
    # minsize als obere Schranke des kleinsten paths

    needed = needed_free - disk_size + sizes["/"]
    minsize = list(sizes.values())[0]
    if needed <= 0:
        return None

    # iteriert durch sizes und speichert alles was mind. needed speicher hat und kleiner als
    # der zurzeit kleinste path hat.
    for key in sizes:
        value = sizes[key]
        if value >= needed and value < minsize:
            minsize = value
    return minsize


def delete_directory(sizes, path):
    """Der Code gibt eine Copy von sizes zurück
    und gibt als Print an das so ein Path net gibt"""

    # Kopiert sizes und löscht path von Kopie
    sizes2 = deepcopy(sizes)
    a = sizes2.pop(path, None)
    if a is None:
        print("Dieses Path gibt es nicht in sizes")
        return sizes2

    # geht alle oberen paths durch die Verbunden sind und
    # subtrahiert die gelöschten Datenvon der gesammt Menge
    pathn = delete_till(path, "/")
    if pathn != "/":
        pathn += "/"
    for key in sizes2:
        if pathn.startswith(key):
            sizes2[key] = sizes2[key] - a
    return sizes2


# ---------------------------------------------------------------- Answers
print(parse_transcript(EXAMPLE))

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
