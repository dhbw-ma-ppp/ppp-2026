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


def load_weather(path: Path) -> pd.DataFrame:
    """Read a DWD daily climate file into a DataFrame.

    Keep only the columns in COLUMNS, with our names; -999 (missing) becomes NaN. Add the
    columns `year` and `month`, as ints, worked out from `date` (an int such as 19470101).
    """
    weather = pd.read_csv(
        path,
        sep=";",
        na_values=[-999],
        skiprows=1,
        header=None,
        usecols=[1, 6, 8, 10, 12, 13, 14, 15, 16],
        names=[
            "date",
            "rain",
            "sunshine",
            "clouds",
            "pressure",
            "mean_temp",
            "humidity",
            "max_temp",
            "min_temp",
        ],
    )
    weather["year"] = weather["date"] // 10000
    weather["month"] = (weather["date"] // 100) % 100
    return weather


def missing_per_year(weather: pd.DataFrame, column: str) -> pd.Series:
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather.loc[weather[column].isna(), ["year", column]]["year"].value_counts()


def hot_days(weather: pd.DataFrame, threshold: int = 30.0) -> pd.Series:
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    pass  # replace this line with your code


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
    print(
        f"1:\n"
        f"\tThe file has {weather['date'].count()} days and goes from the year {weather['year'].min()} to the year {weather['year'].max()}."
    )
    print(
        f"2:\n"
        f"\t`max_temp` was missing on almost every day of the years {missing_per_year(weather, 'max_temp').keys().to_numpy()} while `mean_temp` is missing from {missing_per_year(weather, 'mean_temp').to_numpy()}.\n"
        f"\tThis tells us that the weather station was not recording the maximum temperature until {missing_per_year(weather, 'max_temp').keys().to_numpy().max() + 1}."
    )
