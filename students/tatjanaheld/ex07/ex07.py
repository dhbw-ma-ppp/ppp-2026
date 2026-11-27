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

    weather = pd.read_csv(path, sep=";", skipinitialspace=True, na_values=-999)
    weather = weather[list(COLUMNS)]
    weather = weather.rename(columns=COLUMNS)

    weather["year"] = weather["date"] // 10000
    weather["month"] = weather["date"] // 100 % 100

    return weather


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""

    missing = weather[column].isna()
    return missing.groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """

    known = weather[weather["max_temp"].notna()]
    hot = known["max_temp"] >= threshold

    return hot.groupby(known["year"]).sum()


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""

    part = weather[weather["year"].between(first_year, last_year)]
    totals = part.groupby(["year", "month"])["rain"].sum()

    return totals.groupby("month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""

    counts = hot_days(weather)
    plt.bar(counts.index, counts.values)

    plt.xlabel("years")
    plt.ylabel("number of hot days")
    plt.title("hot days in Mannheim")

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

    train = weather[weather["year"] <= last_train_year]
    test = weather[weather["year"] > last_train_year]

    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """

    never = (test["rainy_tomorrow"] == 0).mean()
    same = (test["rainy_tomorrow"] == test["rainy"]).mean()

    return {"never": never, "same": same}


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """

    data = add_rainy(weather)
    data = data[data["year"] >= 1947]
    data = data.dropna(subset=features + ["rainy_tomorrow"])

    train, test = split_by_year(data, 2015)

    rows = []
    for depth in depths:
        tree = DecisionTreeClassifier(max_depth=depth, random_state=1)
        tree.fit(train[features], train["rainy_tomorrow"])

        train_score = tree.score(train[features], train["rainy_tomorrow"])
        test_score = tree.score(test[features], test["rainy_tomorrow"])

        rows.append((depth, train_score, test_score))

    return rows, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    print("1:", len(weather), weather["year"].min(), weather["year"].max())

    missing = missing_per_year(weather, "max_temp")
    print("2:", missing[missing > 300])
    missing_mean = missing_per_year(weather, "mean_temp")
    print("2 mean_temp:", missing_mean[missing > 300])

    hot = hot_days(weather)
    print("3:", hot.max(), hot[hot == hot.max()])

    print("4:", hot.loc[1951:1980].mean(), hot.loc[1996:2025].mean())

    rain = monthly_rain(weather, 1947, 2025)
    print("5 wettest:", rain.idxmax(), rain.max())
    print("5 driest:", rain.idxmin(), rain.min())

    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")

    rows, base = model_table(weather, ["rainy", "humidity", "clouds", "pressure"], [1, 3, 5, None])
    print("6 baselines:", base)
    for row in rows:
        print(row)
