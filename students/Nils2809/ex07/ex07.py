# Exercise 07. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path

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
    """Read a DWD daily climate file into a DataFrame.

    Keep only the columns in COLUMNS, with our names; -999 (missing) becomes NaN. Add the
    columns `year` and `month`, as ints, worked out from `date` (an int such as 19470101).
    """
    wetter = pd.read_csv(path, sep=";", skipinitialspace=True, na_values=-999)
    wetter = wetter[list(COLUMNS.keys())]
    wetter = wetter.rename(columns=COLUMNS)
    wetter["year"] = wetter["date"] // 10000
    wetter["month"] = (wetter["date"] // 100) % 100
    return wetter


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather.groupby("year")[column].apply(lambda column: column.isna().sum())


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    bekannt = weather[weather["max_temp"].notna()]
    # heiße Tage pro Jahr
    return bekannt.groupby("year")["max_temp"].apply(lambda column: (column >= threshold).sum())


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    daten = weather[(weather["year"] >= first_year) & (weather["year"] <= last_year)]
    # gesamte Summe für den jeweiligen Monat
    Monatsergebnis = daten.groupby(["year", "month"])["rain"].sum()
    return Monatsergebnis.groupby("month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    heißeTage = hot_days(weather)
    plt.figure(figsize=(10, 5))
    plt.bar(heißeTage.index, heißeTage.values)
    plt.xlabel("Jahr")
    plt.ylabel("Heiße Tage")
    plt.title("Heiße Tage pro Jahr (>= 30°C)")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    regen = weather.copy()
    # regen mit dem Wert von thresohold vergleichen
    regen["rainy"] = (regen["rain"] >= threshold).astype(int)
    regen["rainy_tomorrow"] = regen["rainy"].shift(-1)
    return regen


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    # Trainingsdaten
    train = weather[weather["year"] <= last_train_year]
    test = weather[weather["year"] > last_train_year]
    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    # letzte Zeile entfernen
    test = test.dropna(subset=["rainy_tomorrow"])
    never = (test["rainy_tomorrow"] == 0).mean()
    same = (test["rainy_tomorrow"] == test["rainy"]).mean()
    return {
        "never": never,
        "same": same,
    }


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    if "rainy" not in weather.columns:
        weather = add_rainy(weather)
    # Zeile ohne Wert herausfiltern
    weather = weather.dropna(subset=features + ["rainy_tomorrow"])
    train, test = split_by_year(weather, 2015)
    trainDaten = train[features]
    trainZiel = train["rainy_tomorrow"]
    testDaten = test[features]
    testZiel = test["rainy_tomorrow"]
    results = []
    for depth in depths:
        modell = DecisionTreeClassifier(max_depth=depth, random_state=1)
        modell.fit(trainDaten, trainZiel)
        trainGenauigkeit = modell.score(trainDaten, trainZiel)
        testGenauigkeit = modell.score(testDaten, testZiel)
        results.append((depth, trainGenauigkeit, testGenauigkeit))
    return results, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    # Print your answers here, e.g. print("1:", ...)
    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")
    # Answer 1
    print(
        "1:",
        len(weather),
        "days from",
        weather["year"].min(),
        "to",
        weather["year"].max(),
    )

    # Answer 2
    missing = missing_per_year(weather, "max_temp")
    print("2:")
    print(missing.sort_values(ascending=False).head(10))
    mean_missing = missing_per_year(weather, "mean_temp")
    print("Mean temp missing:")
    print(mean_missing.loc[missing.sort_values(ascending=False).head(10).index])

    # Answer 3
    heiß = hot_days(weather)
    maximum = heiß.max()
    print(
        "3:",
        list(heiß[heiß == maximum].index),
        maximum,
        "hot days",
    )

    # Answer 4
    print(
        "4:",
        "1951-1980 =",
        heiß.loc[1951:1980].mean(),
    )
    print(
        "   ",
        "1996-2025 =",
        heiß.loc[1996:2025].mean(),
    )

    # Answer 5
    regen = monthly_rain(weather, 1947, 2025)
    nass = regen.idxmax()
    trocken = regen.idxmin()
    print(
        "5: wettest month =",
        nass,
        "(",
        regen[nass],
        "mm )",
    )
    print(
        "driest month =",
        trocken,
        "(",
        regen[trocken],
        "mm )",
    )

    # Answer 6
    weather = add_rainy(weather)
    table, baseline = model_table(
        weather,
        ["month", "rainy", "mean_temp", "humidity"],
        [1, 2, 3, 5, None],
    )
    print("6:")
    print("Baselines:", baseline)
    print("Results:")
    print(table)
