# Exercise 07. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path
import calendar
import matplotlib.pyplot as plt  # noqa: F401  (you'll need it in Part 2)
import pandas as pd  # noqa: F401
from sklearn.tree import DecisionTreeClassifier  # noqa: F401  (you'll need it in Part 2)

# The DWD's daily data for Mannheim. It's large, so git ignores your copy of it (see README.md).
DATA_FILE = Path(__file__).parent / "mannheim.txt"
# A few lines of the same file, for the tests.
SAMPLE_FILE = Path(__file__).parent / "sample.txt"

# The columns we use: the DWD's name -> our name.
COLUMNS = {
    "MESS_DATUM": "date",
    "TMK": "mean_temp",
    "TXK": "max_temp",
    "TNK": "min_temp",
    "RSK": "rain",
    "SDK": "sunshine",
    "NM": "clouds",
    "UPM": "humidity",
    "PM": "pressure",
}

# ---------------------------------------------------------------- Part 1 (in class)


def load_weather(path):
    """Read a DWD daily climate file into a DataFrame."""

    # CSV-Datei einlesen; -999 wird als fehlender Wert (NaN) behandelt
    table = pd.read_csv(path, sep=";", skipinitialspace=True, na_values=-999)

    # Nur benötigte Spalten behalten und umbenennen
    table = table[list(COLUMNS)]
    table = table.rename(columns=COLUMNS)

    # Jahr und Monat aus dem Datum berechnen
    table["year"] = table["date"] // 10000
    table["month"] = table["date"] // 100 % 100

    return table


def missing_per_year(weather, column):
    """For every year: count how many days a column is missing."""

    # Fehlende Werte markieren und pro Jahr zählen
    missing = weather[column].isna()
    return missing.groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """Count hot days per year."""

    # ohne bekannte Höchsttemperatur entfernen
    known = weather.dropna(subset=["max_temp"])

    # an welchen Tagen der Grenzwert erreicht wird?
    hot = known["max_temp"] >= threshold

    # Heiße Tage im Jahr zählen
    return hot.groupby(known["year"]).sum()


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """Calculate the average monthly rainfall."""

    # Gewünschten Zeitraum einzäunen
    data = weather[(weather["year"] >= first_year) & (weather["year"] <= last_year)]

    # Gesamtniederschlag = Monat + Monat ...
    monthly = data.groupby(["year", "month"])["rain"].sum()

    # Durchschnittliche Niederschlag pro Monat
    return monthly.groupby("month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days per year."""

    # Heiße Tage pro Jahr berechnen
    hot = hot_days(weather)

    # Balkendiagramm erstellen
    hot.plot(kind="bar")
    plt.xlabel("Year")
    plt.ylabel("Number of hot days")
    plt.title("Hot days per year in Mannheim")

    # Jede 20. Jahreszahl anzeigen
    plt.xticks(range(0, len(hot), 20))

    # Diagramm speichern und anzeigen
    plt.savefig(path)
    plt.show()


def add_rainy(weather, threshold=1.0):
    """Add rainy and rainy_tomorrow columns."""

    result = weather.copy()

    # 1, wenn es mindestens threshold mm regnet, sonst 0
    result["rainy"] = (result["rain"] >= threshold).astype(int)

    # Regenstatus von der Nächsten übernehmen
    result["rainy_tomorrow"] = result["rainy"].shift(-1)

    return result


def split_by_year(weather, last_train_year):
    """Split data into training and test sets."""

    # Trainingsdaten bis zum angegebenen Jahr
    train = weather[weather["year"] <= last_train_year]

    # Testdaten vom nächsten Jahren
    test = weather[weather["year"] > last_train_year]

    return train, test


def baselines(test):
    """Calculate the accuracy of two simple baseline models."""

    # Zeilen ohne Wert entfernen
    test = test.dropna(subset=["rainy_tomorrow"])

    # 1: Es regnet morgen nie
    never = (test["rainy_tomorrow"] == 0).mean()

    # 2: Morgen ist das Wetter wie heute
    same = (test["rainy"] == test["rainy_tomorrow"]).mean()

    return {"never": never, "same": same}


def model_table(weather, features, depths):
    """Train decision trees and compare their accuracy."""

    # Regeninformationen ergänzen
    weather = add_rainy(weather)

    # ab 1947 verwenden
    data = weather[weather["year"] >= 1947]

    # Zeilen mit fehlenden Werten entfernen
    data = data.dropna(subset=features + ["rainy_tomorrow"])

    # Daten in Trainings- und Testdaten aufteilen
    train, test = split_by_year(data, 2015)

    results = []

    # Für jede Baumtiefe einen Entscheidungsbaum trainieren
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=1)

        # Modell mit den Trainingsdaten trainieren
        model.fit(train[features], train["rainy_tomorrow"])

        # Genauigkeit auf Trainings- und Testdaten berechnen
        train_accuracy = model.score(train[features], train["rainy_tomorrow"])
        test_accuracy = model.score(test[features], test["rainy_tomorrow"])

        # Ergebnisse speichern
        results.append((depth, train_accuracy, test_accuracy))

    return results, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    # Answer 1
    print("\nAnswer 1:")
    print("Number of days:", len(weather))
    print("First year:", weather["year"].min())
    print("Last year:", weather["year"].max())

    # Answer 2
    print("\nAnswer 2:")
    missing_max = missing_per_year(weather, "max_temp")
    missing_mean = missing_per_year(weather, "mean_temp")

    print("Missing max_temp:")
    print(missing_max[missing_max > 0].to_string())

    print("Missing mean_temp:")
    print("No missing values." if missing_mean.empty else missing_mean)

    # Answer 3
    print("\nAnswer 3:")
    hot = hot_days(weather)
    print("Most hot days:", hot.max())
    print("Year:", hot[hot == hot.max()].index.tolist())

    # Answer 4
    print("\nAnswer 4:")
    print("1951-1980:", hot.reindex(range(1951, 1981), fill_value=0).mean())
    print("1996-2025:", hot.reindex(range(1996, 2026), fill_value=0).mean())

    # Answer 5
    print("\nAnswer 5:")
    rain = monthly_rain(weather, 1947, 2025)
    print("Wettest month:", calendar.month_name[rain.idxmax()], round(rain.max(), 2), "mm")
    print("Driest month:", calendar.month_name[rain.idxmin()], round(rain.min(), 2), "mm")

    # Plot
    plot_hot_days(weather, "hot_days.png")

    # Answer 6
    print("\nAnswer 6:")
    results, baseline = model_table(
        weather, ["month", "rainy", "humidity", "pressure"], [1, 2, 3, 5, None]
    )

    print("Baselines:", baseline)

    for result in results:
        print(result)
