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
    df = pd.read_csv(path, sep=";", skipinitialspace=True, na_values=-999)
    df = df[list(COLUMNS)]
    df = df.rename(columns=COLUMNS)
    df["year"] = df["date"] // 10000
    df["month"] = (df["date"] // 100) % 100
    return df


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather[column].isna().groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    known_temps = weather.groupby("year")["max_temp"].count()

    max_temp_sum = (weather["max_temp"] >= threshold).groupby(weather["year"]).sum()
    return max_temp_sum.loc[known_temps > 0]


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    weather = weather.loc[(weather["year"] >= first_year) & (weather["year"] <= last_year)]

    monthly_totals = weather.groupby(["year", "month"])["rain"].sum()
    monthly_averages = monthly_totals.groupby(level="month").mean()

    return monthly_averages


def plot_hot_days(weather, path):
    hot = hot_days(weather)

    plt.figure()
    plt.bar(hot.index, hot.values)
    plt.xlabel("Year")
    plt.ylabel("Number of hot days")
    plt.title("Hot days per year in Mannheim")
    plt.savefig(path)
    plt.close()


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    result = weather.copy()
    result["rainy"] = (result["rain"] >= threshold).astype(int)
    result["rainy_tomorrow"] = result["rainy"].shift(-1)
    return result


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    train = weather.loc[weather["year"] <= last_train_year]
    test = weather.loc[weather["year"] > last_train_year]
    return train, test


def baselines(test):
    """Accuracy of two models without learning."""
    never = (test["rainy_tomorrow"] == 0).mean()
    same = (test["rainy"] == test["rainy_tomorrow"]).mean()
    return {
        "never": never,
        "same": same,
    }


def model_table(weather, features, depths):
    """Train decision trees and compare their accuracy."""
    weather = add_rainy(weather)
    weather = weather.loc[weather["year"] >= 1947]
    weather = weather.dropna(subset=features + ["rainy_tomorrow"])
    train, test = split_by_year(weather, 2015)
    X_train = train[features]
    y_train = train["rainy_tomorrow"]
    X_test = test[features]
    y_test = test["rainy_tomorrow"]
    results = []
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=1)
        model.fit(X_train, y_train)
        train_accuracy = model.score(X_train, y_train)
        test_accuracy = model.score(X_test, y_test)
        results.append((depth, train_accuracy, test_accuracy))
    base = baselines(test)
    return results, base


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)
    # Print your answers here, e.g. print("1:", ...)
