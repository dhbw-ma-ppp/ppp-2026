# Exercise 07. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401  (you'll need it in Part 2)
import pandas as pd  # noqa: F401
import numpy as np
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
    weather_data = pd.read_csv(path, na_values=-999, sep=";")
    weather_data.columns = weather_data.columns.str.strip()
    weather_data = weather_data[list(COLUMNS.keys())].rename(columns=COLUMNS)

    weather_data["year"] = weather_data["date"] // 10000
    weather_data["month"] = (weather_data["date"] // 100) % 100

    return weather_data


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    array_column_is_na = weather[column].isna()
    column_is_na_by_year = array_column_is_na.groupby(weather["year"])
    return column_is_na_by_year.sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    maxtemp_is_atleast_threshold = weather["max_temp"] >= threshold
    missing = missing_per_year(weather, "max_temp")
    days = weather.groupby("year").size()
    maxtemp_is_atleast_threshold_by_year = maxtemp_is_atleast_threshold.groupby(
        weather["year"]
    ).sum()
    maxtemp_is_atleast_threshold_by_year_cleaned = maxtemp_is_atleast_threshold_by_year[
        (days != missing)
    ]

    return maxtemp_is_atleast_threshold_by_year_cleaned


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    weather_time_range = weather[(weather["year"] >= first_year) & (weather["year"] <= last_year)]
    a = weather_time_range.groupby(["year", "month"])["rain"].sum()
    mean_rain_per_month = a.groupby(level="month").mean()
    return mean_rain_per_month


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    hot_days_per_year = hot_days(weather)

    fig, ax = plt.subplots()
    ax.bar(hot_days_per_year.index, hot_days_per_year.values)
    ax.set_xlabel("year")
    ax.set_ylabel("hot days")
    ax.set_title("Hot Days per Year")
    fig.savefig(path)


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    weather_new = weather.copy()
    weather_new["rainy"] = weather["rain"].apply(
        lambda rain: np.nan if np.isnan(rain) else 1 if rain >= threshold else 0
    )
    weather_new["rainy_tomorrow"] = weather_new["rainy"].shift(-1)
    return weather_new


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    weather_up_until = weather[(weather["year"] <= last_train_year)]
    weather_after = weather[(weather["year"] > last_train_year)]
    return weather_up_until, weather_after


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    accuracy = {}
    never = test["rainy"] == 0
    never_accuracy = never.mean()
    same = test["rainy"] == test["rainy_tomorrow"]
    same_accuracy = same.mean()
    accuracy["never"] = never_accuracy
    accuracy["same"] = same_accuracy
    return accuracy


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    return_list = []
    weather_with_rainy_and_rainytomorrow = add_rainy(weather)
    weather_from_1947 = weather_with_rainy_and_rainytomorrow[
        (weather_with_rainy_and_rainytomorrow["year"] >= 1947)
    ]
    weather_from_1947 = weather_from_1947.dropna(subset=features + ["rainy_tomorrow"])
    training_data, test_data = split_by_year(weather_from_1947, 2015)
    baseline_test_data = baselines(test_data)

    for depth in depths:
        tree = DecisionTreeClassifier(max_depth=depth, random_state=1)
        tree.fit(training_data[features], training_data["rainy_tomorrow"])
        predictions_training = tree.predict(training_data[features])
        accuracy_training = (predictions_training == training_data["rainy_tomorrow"]).mean()
        predictions_test = tree.predict(test_data[features])
        accuracy_test = (predictions_test == test_data["rainy_tomorrow"]).mean()
        return_list.append((depth, accuracy_training, accuracy_test))

    return return_list, baseline_test_data


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print("Answer 1:")
    print(len(weather))
    print(weather["year"].min(), weather["year"].max())
    print("Answer 2:")
    missing = missing_per_year(weather, "max_temp")
    print(missing[missing >= 200])
    mean_temp = missing_per_year(weather, "mean_temp")
    print(mean_temp[missing >= 350])
    # The Station didn't pick up any temperatures until the year 1973.
    print("Answer 3:")
    hot = hot_days(weather)
    print(hot[hot == hot.max()])
    print("Answer 4:")
    print("1951–1980: ", hot.loc[1951:1980].mean())
    print("1996-2025: ", hot.loc[1996:2025].mean())
    print("Answer 5:")
    rain = monthly_rain(weather, 1947, 2025)
    print(rain.idxmax(), rain.max())
    print(rain.idxmin(), rain.min())
    plot_hot_days(weather, "hot_days.png")
    print("Answer 6:")
    rows, base = model_table(
        weather,
        ["rainy", "humidity"],
        [1, 2, 3, 5, 10, None],
    )
    print("Baselines:", base)
    for row in rows:
        print(row)
