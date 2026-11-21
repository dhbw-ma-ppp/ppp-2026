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

HOT_DAYS_PATH = Path(__file__).parent / "hot_days.png"

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
    weather = pd.read_csv(
        path, sep=";", na_values=[-999], skipinitialspace=True, usecols=COLUMNS.keys()
    )

    # To order them like COLUMNS are orderd
    weather = weather[COLUMNS.keys()]

    weather = weather.rename(columns=COLUMNS)
    weather["year"] = weather["date"] // 10_000
    weather["month"] = weather["date"] // 100 % 100
    return weather


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather[column].isna().groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    known = weather[~weather["max_temp"].isna()]
    result = (known["max_temp"] >= threshold).groupby(known["year"]).sum()
    return result


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    total_per_month_per_year = (
        weather.groupby(["year", "month"])["rain"].sum().loc[first_year:last_year]
    )
    total_per_month = total_per_month_per_year.groupby("month").mean()
    return total_per_month


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    hot = hot_days(weather)

    fig, ax = plt.subplots()
    ax.bar(hot.index, hot.values)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of hot days")
    ax.set_title("Hot days per year")

    fig.savefig(path)


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    result = weather.copy()

    result["rainy"] = result["rain"].apply(lambda rain: 1 if rain >= threshold else 0)
    result["rainy_tomorrow"] = result["rainy"].shift(-1)
    return result


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    if last_train_year not in weather["year"].values:
        raise ValueError(f"{last_train_year} is not in weather.")

    train = weather[weather["year"] <= last_train_year]
    test = weather[weather["year"] > last_train_year]
    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    if len(test) <= 0:
        return {"never": 0, "same": 0}

    known = test[~test["rainy_tomorrow"].isna()]
    never = (known["rainy_tomorrow"] == 0).sum() / len(test)
    same = (known["rainy_tomorrow"] == known["rainy"]).sum() / len(test)

    result = {"never": never, "same": same}
    return result


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """

    weather_cleaned = add_rainy(weather)

    known = weather_cleaned[~weather_cleaned["rainy_tomorrow"].isna()]
    for feature in features:
        known = known[~known[feature].isna()]
    known = known[known["year"] >= 1947]

    train, test = split_by_year(known, 2015)

    results = []

    for depth in depths:
        tree = DecisionTreeClassifier(max_depth=depth, random_state=1)
        tree.fit(train[features], train["rainy_tomorrow"])
        train_accuracy = tree.score(train[features], train["rainy_tomorrow"])
        test_accuracy = tree.score(test[features], test["rainy_tomorrow"])
        result = (depth, train_accuracy, test_accuracy)
        results.append(result)

    return results, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    # Print your answers here, e.g. print("1:", ...)
    print(
        f"Answer 1: Number of days: {len(weather)}, from {weather['year'].min()} to {weather['year'].max()}."
    )

    missing = missing_per_year(weather, "max_temp")
    bad_years = missing[missing > 350].index

    mean_temp = weather[weather["year"].isin(bad_years)].groupby("year")["mean_temp"].mean()

    print(f"Answer 2: Missing: {missing[bad_years]}, mean_temp: {mean_temp}")
    # The mean temperature was recorded but not the max one

    hot = hot_days(weather)
    hot_years = hot[hot == hot.max()]
    print(f"Answer 3: Hottest years: {hot_years}")

    average_number_hot_days = hot.loc[1951:1980].mean()
    print(f"Answer 4: Average number of hot days {average_number_hot_days}")

    rain = monthly_rain(weather, 1947, 2025)
    print(f"Answer 5: Wettest: {rain[rain == rain.max()]}, driest: {rain[rain == rain.min()]}")

    plot_hot_days(weather, HOT_DAYS_PATH)
    # zwischen 1792 bis 1936 scheint es gar keine Einträge zu geben, dazu passen auch die circa 34.000 Tage aus Answer 2

    features = ["rainy", "mean_temp", "sunshine", "clouds", "humidity", "pressure", "month"]
    dephts = [None, 1, 2, 3, 4, 5, 6, 8, 10, 20]

    print(f"Answer 6: {model_table(weather, features, dephts)}")
