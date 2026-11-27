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
    # weather_not_renamed = pd.read_csv(filepath_or_buffer = path ,sep = ";" , skipinitialspace = True ,
    #                                  usecols = list(COLUMNS),
    #                                  na_values = [-999])
    # weather = weather_not_renamed.rename(columns= COLUMNS)
    weather = pd.read_csv(
        filepath_or_buffer=path,
        sep=";",
        skipinitialspace=True,
        # usecols=list(COLUMNS),
        na_values=[-999],
    )  # .rename(columns= COLUMNS)
    weather = weather[list(COLUMNS)].rename(columns=COLUMNS)
    weather["year"] = weather["date"] // 10000
    weather["month"] = weather["date"] % 10000 // 100

    return weather


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""

    return weather[column].isna().groupby(weather["year"]).sum()


# print(missing_per_year(load_weather(SAMPLE_FILE), COLUMNS))
def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    weather_known_max_temp = weather.dropna(subset=["max_temp"])
    return (
        (weather_known_max_temp["max_temp"] >= threshold)
        .groupby(weather_known_max_temp["year"])
        .sum()
    )


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    weather_yearspan = weather[(weather["year"] >= first_year) & (weather["year"] <= last_year)]
    weather_rain_sums = weather_yearspan.groupby(["year", "month"])["rain"].sum()
    return weather_rain_sums.groupby("month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    hot_days_per_year = hot_days(weather)
    fig, ax = plt.subplots()
    ax.bar(hot_days_per_year.index, hot_days_per_year.values)
    ax.set_xlabel("Year")
    ax.set_ylabel("Hot Days")
    ax.set_title("Hot days per year")
    fig.savefig(path)
    plt.close(fig)


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    weather_with_rainy = weather.copy()
    weather_with_rainy["rainy"] = (weather_with_rainy["rain"] >= threshold).astype(int)
    weather_with_rainy["rainy_tomorrow"] = weather_with_rainy["rainy"].shift(-1)
    return weather_with_rainy


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    train = weather["year"] <= last_train_year
    return weather[train], weather[~train]


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    never = (test["rainy_tomorrow"] == 0).mean()
    same_as_before = (test["rainy"] == test["rainy_tomorrow"]).mean()
    return {"never": never, "same": same_as_before}


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    weather = add_rainy(weather)
    weather = weather[weather["year"] >= 1947]
    weather = weather.dropna(subset=features + ["rainy_tomorrow"])
    test = weather[weather["year"] > 2015]
    train = weather[weather["year"] <= 2015]
    results = []
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=1)
        model.fit(train[features], train["rainy_tomorrow"])
        train_accuracy = model.score(train[features], train["rainy_tomorrow"])
        test_accuracy = model.score(test[features], test["rainy_tomorrow"])
        results.append((depth, train_accuracy, test_accuracy))
    return results, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)
    # Print your answers here, e.g. print("1:", ...)
    # Answer 1:
    print(f"1: days: {len(weather)}, from {weather['year'].min()} to {weather['year'].max()}")
    # Answer 2:
    missing_max = missing_per_year(weather, "max_temp")
    print(
        f"2: Years with max_temp missing on at least 85% of days: {list(missing_max[missing_max >= 365 * 85 // 100].index)}"
    )
    print(
        f"   mean_temp is missing for:\n{missing_per_year(weather, 'mean_temp').loc[missing_max[missing_max >= 365 * 85 // 100].index]}"
    )
    # Answer 3:
    print(
        f"3: highest number of hot days: {list(hot_days(weather)[hot_days(weather) == hot_days(weather).max()].index)} with {hot_days(weather).max()}"
    )
    # Answer 4:
    print(f"4: mean of hot days 1951-1980: {hot_days(weather).loc[1951:1980].mean():.2f}")
    print(f"   mean of hot days 1996-2025: {hot_days(weather).loc[1996:2025].mean():.2f}")
    # Answer 5:
    print(
        f"5: wettest month: {monthly_rain(weather, 1947, 2025).idxmax()} with {monthly_rain(weather, 1947, 2025).max():.2f}"
    )
    print(
        f"   driest month: {monthly_rain(weather, 1947, 2025).idxmin()} with {monthly_rain(weather, 1947, 2025).min():.2f}"
    )

    print("plot_hot_days graph:")
    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")

    # Answer 6:
    features = ["rainy", "humidity", "pressure", "clouds", "month"]
    rows, base = model_table(weather, features, [1, 3, 5, 8, 20, None])
    print(f"6: baselines: never: {base['never']:.3f}, same: {base['same']:.3f}")
    for depth, train_acc, test_acc in rows:
        print(f"depth: {depth!s:>5}, train: {train_acc:.3f}, test: {test_acc:.3f}")
