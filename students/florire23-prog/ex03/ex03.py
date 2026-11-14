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

    current_dir = []
    files = []

    for line in lines:
        line = line.strip()  # Schleife geht jede Zeile aus lines einzeln ab und strip entfernt die Leerzeichen am Anfang und Ende

        if line.startswith("$ cd "):  # cd für Verzeichnis wechseln in das nächste Verzeichnis
            target = line[5:]  # Pos. 5 das ersten fünf zeichen "$ cd "

            if (
                target == "/"
            ):  # Bei / wechsel zum Wurzelverzeichnis und current_dir wird zur leeren liste
                current_dir = []
            elif target == "..":  # über $ cd .. wechslen wir eine Ebene nach oben
                if current_dir:
                    current_dir.pop()  # pop um den letzten eintrag aus dem "stapel" rauszunehmen
            else:
                current_dir.append(
                    target
                )  # Ziel weder / noch .. => wird der Verzeichnisname an die Liste angehängt

        elif (
            line.startswith("$ ls") or line.startswith("dir ")
        ):  # $ ls listet dateien und verzeichnisse auf. dir zeigt an ob unterverzeichnisse vorhanden
            continue

        else:
            parts = line.split(maxsplit=1)
            size = int(parts[0])
            name = parts[
                1
            ]  # Zeile keine der bisherigen Bedingungen entspricht, behandelt der Code sie als Datei.

            path = "/" + "/".join(current_dir + [name])
            files.append(
                (path, size)
            )  # ergänzt am anfang / und zwischen den DAteien "/". Und Dateigröße wird angegeben

    return files


def directory_sizes(entries):
    """Return a dict mapping every directory path to the total size of all files under it.

    entries is a list of (path, size) pairs, e.g. ("/a/b/c.txt", 100). A directory's total
    size includes every file anywhere below it, however deep. The root directory is "/".
    """

    sizes = {"/": 0}

    for path, size in entries:  # Der Code geht jeden Eintrag in entries durch.
        parts = path.strip(
            "/"
        ).split(
            "/"
        )  # Diese Zeile entfernt die Schrägstriche am Anfang und Ende und zerlegt den Pfad an jedem /
        directories = ["/"]

        for i in range(1, len(parts)):
            directories.append(
                "/" + "/".join(parts[:i])
            )  # Zuerst wird das Wurzelverzeichnis / in die Liste aufgenommen. Danach werden die übergeordneten Verzeichnisse des Dateipfads ermittelt.

        for directory in directories:
            sizes[directory] = (
                sizes.get(directory, 0) + size
            )  # Hier wird die Größe der aktuellen Datei zu jedem Verzeichnis addiert, das in directories steht.

    return sizes  # Es wird die aufsummierte Größe zurückgegeben


def small_directories_total(sizes, limit=100000):

    total = 0

    for path, size in sizes.items():
        if path != "/" and size <= limit:
            total += size

    return total  # Der Code addiert alle Größen, die den Grenzwert nicht überschreiten, und gibt die Summe zurück.


# ---------------------------------------------------------------- Part 2 (at home)


def directory_to_delete(sizes, disk_size=50000000, needed_free=20000000):
    """Return the size of the smallest directory whose deletion frees enough space.

    The disk holds `disk_size` in total; at least `needed_free` must stay unused.
    `sizes["/"]` is the space currently used. Return None if enough space is free already.
    """
    used = sizes["/"]  # aktuell belegten speicher ermitteln
    free = disk_size - used  # freier speicher berechnen

    if free >= needed_free:
        return None  # falls genug speicher frei ist muss nichts gelöscht werden

    needed = needed_free - free  # Speicherplatz berechnung, da platz gebraucht wird

    for size in sorted(sizes.values()):
        if size >= needed:
            return size

    return None  # None zurüchgeben wenn kein verzeichnis groß genug ist


def delete_directory(sizes, path):
    """Return a new dict of directory sizes, as if the directory `path` had been deleted.

    The result is what directory_sizes would return for the files that remain.
    `sizes` itself must not change.
    """
    new_sizes = sizes.copy()  # kopie erstellen

    if path not in new_sizes:
        return new_sizes

    deleted_size = new_sizes[path]  # gröse speichern des verzeichnisses das gelöscht werden soll

    for directory in new_sizes.copy():  # verzeichnis löschen
        if directory == path or directory.startswith(
            path + "/"
        ):  # schauen ob richtiges verzeichnis + gibt es Unterv.
            del new_sizes[directory]  # stimmt bedingung: löschen

    for directory in new_sizes:  # gröse anpassen
        if directory == "/" or path.startswith(
            directory + "/"
        ):  # HAupteverzeichnis "/" oder Verzeichnis
            new_sizes[directory] -= (
                deleted_size  # gröse verzeichnis wird von der Grösse des Gesamten abgezogen
            )

    return new_sizes  # ergebnis zurückgeben


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
