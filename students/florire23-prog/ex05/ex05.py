# Exercise 05. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from puzzle_input import CAVE

EXAMPLE_TEXT = """
19999
19111
19191
11191
99991
"""

# A path through EXAMPLE_TEXT's grid (see README.md, answer 2).
# fmt: off
EXAMPLE_PATH = [
    (0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 3), (1, 4),
    (2, 4), (3, 4), (4, 4),
]
# fmt: on

# ---------------------------------------------------------------- Part 1 (in class)


def parse_grid(text):
    """Gibt das Gitter aus `text` als Liste von Zeilen zurück, wobei jede Zeile eine
    Liste von Ganzzahlen ist.

    `text` enthält eine Zeile pro Zeile und eine Ziffer pro Position. Leere Zeilen und
    Leerzeichen am Anfang oder Ende einer Zeile sind egal.
    """

    zeilen = []  # hier sammeln wir die fertigen Zeilen

    for zeile in text.splitlines():  # Zeile für Zeile durchgehen
        zeile = zeile.strip()  # Leerzeichen am Anfang und Ende entfernen
        if zeile == "":  # leere Zeile = "" => überspringen
            continue

        reihe = []  # neue Zeile für das Gitter
        for ziffer in zeile:  # jede Ziffer einzeln anschauen
            reihe.append(int(ziffer))  # Ziffer in eine Ganzzahl umwandeln
        zeilen.append(reihe)  # fertige Zeile ans Gitter anhängen

    return zeilen  # Gitter zurückgeben


def path_risk(grid, path):
    """Return the total risk of following `path`, a list of (row, col) positions.

    The risk of the first position doesn't count: you're already there.
    """
    risk = 0  # Risikozähler
    rest = path[1:]  # erste Position weg, die zählt nicht

    for zeile, spalte in rest:  # jede weitere Position durchgehen
        risk += grid[zeile][spalte]  # Risiko der Position dazuzählen

    return risk  # Gesamtrisiko zurückgeben


def lowest_risk(grid, row=0, col=0, speicher=None):
    """Gibt das niedrigste Gesamtrisiko von (row, col) bis zur unteren rechten Ecke zurück.

    Züge gehen nur nach rechts oder nach unten. Das Risiko von (row, col) selbst zählt nicht.
    """

    # Beim ersten Aufruf einen leeren Zwischenspeicher anlegen
    if speicher is None:
        speicher = {}

    letzte_zeile = len(grid) - 1
    letzte_spalte = len(grid[0]) - 1

    # Am Ziel kostet nichts mehr
    if row == letzte_zeile and col == letzte_spalte:
        return 0

    # Schon berechnet? Dann direkt zurückgeben
    if (row, col) in speicher:
        return speicher[(row, col)]

    wege = []

    if col < letzte_spalte:
        wege.append(grid[row][col + 1] + lowest_risk(grid, row, col + 1, speicher))

    if row < letzte_zeile:
        wege.append(grid[row + 1][col] + lowest_risk(grid, row + 1, col + 1 - 1, speicher))

    speicher[(row, col)] = min(wege)
    return speicher[(row, col)]


# ---------------------------------------------------------------- Part 2 (at home)


def neighbours(grid, row, col):
    """Return the positions directly above, below, left and right of (row, col) that are
    inside the grid, as a list of (row, col) pairs, in any order."""

    nachbarn = []  # Speicherort für gefundenen Nachbarn

    # ------------------------Oben oder Runter------------------------------#
    # len(grid)Anzahl zeilen / um nach unten +1 , nach oben -1
    # Oben
    if row > 0:
        nachbarn.append((row - 1, col))  # Gibt es über dem aktuellen Feld eine weitere Zeile

    # Unten
    if row < len(grid) - 1:
        nachbarn.append((row + 1, col))  # Gibt es unter dem aktuellen Feld eine weitere Zeile

    # -------------------------Links oder Rechts-----------------------------#
    # Links
    if col > 0:
        nachbarn.append((row, col - 1))  # Gibt es links vom aktuellen Feld eine weitere Zeile

    # Rechts
    if col < len(grid[row]) - 1:
        nachbarn.append((row, col + 1))  # Gibt es rechts vom aktuellen Feld eine weitere Zeile

    return nachbarn


def lowest_risk_any_direction(grid):
    """Gibt das kleinste Gesamtrisiko vom Start bis zum Ziel zurück."""

    zeilen = len(grid)
    spalten = len(grid[0])

    # Tabelle anlegen: eine Zeile pro Gitterzeile
    risiken = []

    for _ in range(zeilen):
        # Jede Zeile ist eine eigene Liste voller unendlich
        risiken.append(
            [float("inf")] * spalten
        )  # Erzeugt Zeile mit n-Spalten / Alle Werte sind unendlich
        # BSP: 4 Spalten (inf, inf, inf, inf)
        # risiken.append hängt neue Zeile an bisherige Tabelle

    risiken[0][0] = 0  # Startfeld kostet nichts
    Felder_Risiko = {0: [(0, 0)]}  # Felder nach Risikostufe: {Risiko: [(Zeile, Spalte)]}

    risiko = 0  # aktuelle Risikostufe

    while Felder_Risiko:
        felder = Felder_Risiko.pop(risiko, [])
        # pop gibt Liste der Risikowerte [Zeile, Spalten] - Paar zurück
        # [] als Notfall, falls es einen wert nicht gibt wird eine leere liste ausgegeben und nicht das Programm beendet

        for row, col in felder:  # Prüfung ob Eintrag in Felder noch aktuell ist
            if risiken[row][col] != risiko:
                continue  # gespeicherte Wert != dieser Stufe => veraltet => überspringen

            if row == zeilen - 1 and col == spalten - 1:
                return risiko  # Ziel erreicht / Feld Unten Rechts

            for neue_row, neue_col in neighbours(grid, row, col):
                neues_risiko = risiko + grid[neue_row][neue_col]
                # Alle Nachbarn holen, die im Gitter liegen
                # Jedes Element == (Zeile, Spalte) des Nachbarfeldes
                # neues Risiko = Startrisiko=0 oder aktuelles Risiko der Stufe + Risikowert vom Nachbarn

                if (
                    neues_risiko < risiken[neue_row][neue_col]
                ):  # Nur speichern, wenn der neue Weg günstiger ist
                    risiken[neue_row][neue_col] = (
                        neues_risiko  # Bestwert für dieses Feld aktualisieren
                    )
                    Felder_Risiko.setdefault(neues_risiko, []).append(
                        (neue_row, neue_col)
                    )  # Neue Risikostufe anlegen / einsortieren

        risiko += 1  # nächste Stufe


# ---------------------------------------------------------------- Answers

if __name__ == "__main__":
    example = parse_grid(EXAMPLE_TEXT)
    cave = parse_grid(CAVE)

    print("Part 1")
    print("1:", lowest_risk(example))
    print("2:", path_risk(example, EXAMPLE_PATH))

    print("Part 2")
    print("3:", lowest_risk(cave))
    print("4:", lowest_risk_any_direction(example))
    print("5:", lowest_risk_any_direction(cave))
