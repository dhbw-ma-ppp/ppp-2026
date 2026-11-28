# Exercise 07. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

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
    data_field = pd.read_csv(path, sep=";", skipinitialspace=True, na_values=-999)
    data_field = data_field[list(COLUMNS)].rename(columns=COLUMNS)
    data_field["year"] = data_field["date"] // 10000
    data_field["month"] = data_field["date"] // 100 % 100
    return data_field


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather[column].isna().groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    # Years without measurements should not be counted as having zero hot days.
    known = weather.dropna(subset=["max_temp"])
    return (known["max_temp"] >= threshold).groupby(known["year"]).sum()


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    years = weather[weather["year"] >= first_year]
    years = years[years["year"] <= last_year]
    monthly_totals = years.groupby(["year", "month"])["rain"].sum(
        min_count=1
    )  # min_count=1 prevents taking 0s from empty measurements.
    monthly_averages = monthly_totals.groupby("month").mean()
    return monthly_averages


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    hot_days_per_year = hot_days(weather)
    ax = hot_days_per_year.plot(kind="bar")
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Hot days")
    ax.set_title("Hot days per year")
    ax.figure.savefig(path)
    plt.close(ax.figure)


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
    test = test.dropna(subset=["rainy_tomorrow"])  # if tomorrow is unknown cannot check prediction
    never_accuracy = (test["rainy_tomorrow"] == 0).mean()
    same_accuracy = (test["rainy_tomorrow"] == test["rainy"]).mean()
    return {"never": never_accuracy, "same": same_accuracy}


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """

    data = add_rainy(weather)
    data = data[data["year"] >= 1947]
    # model needs features and actual outcome for all rows.
    needed_columns = list(features) + ["rainy_tomorrow"]
    data = data.dropna(subset=needed_columns)
    train, test = split_by_year(data, 2015)

    x_train = train[features]
    y_train = train["rainy_tomorrow"]
    x_test = test[features]
    y_test = test["rainy_tomorrow"]

    rows = []
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=1)
        model.fit(x_train, y_train)
        train_accuracy = model.score(x_train, y_train)
        test_accuracy = model.score(x_test, y_test)
        rows.append((depth, train_accuracy, test_accuracy))

    return rows, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)
    # Print your answers here, e.g. print("1:", ...)
