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
help(pd.read_csv)


def load_weather(path):
    """Read a DWD daily climate file into a DataFrame.

    Keep only the columns in COLUMNS, with our names; -999 (missing) becomes NaN. Add the
    columns `year` and `month`, as ints, worked out from `date` (an int such as 19470101).
    """

    df = pd.read_csv(path, sep=";", na_values=[-999])
    df.columns = df.columns.str.strip()
    df = df.rename(
        columns={
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
    )
    df = df[list(COLUMNS.values())]
    # // to cut off right side
    # % to cut off left side
    df["year"] = df["date"] // 10000
    df["month"] = (df["date"] // 100) % 100
    # df["day"] = df["date"] % 100
    return df


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather[column].isna().groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    known = weather[weather["max_temp"].notna()]
    return (known["max_temp"] >= threshold).groupby(known["year"]).sum()


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    pass  # replace this line with your code


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    pass  # replace this line with your code


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    pass  # replace this line with your code


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    pass  # replace this line with your code


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    pass  # replace this line with your code


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    pass  # replace this line with your code


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)
    # Print your answers here, e.g. print("1:", ...)
