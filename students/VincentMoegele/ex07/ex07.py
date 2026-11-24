# Exercise 07. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401  (you'll need it in Part 2)
from matplotlib.ticker import MaxNLocator
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
    weather_data = pd.read_csv(
        path, sep=";", skipinitialspace=True, usecols=list(COLUMNS), na_values=-999
    )
    weather_data = weather_data.rename(columns=COLUMNS)
    weather_data["year"] = weather_data["date"] // 10000
    weather_data["month"] = weather_data["date"] // 100 % 100

    return weather_data[list(COLUMNS.values()) + ["year", "month"]]


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""

    return weather.groupby("year")[column].apply(lambda values: values.isna().sum())


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    known = weather.dropna(subset=["max_temp"])
    return known.groupby("year")["max_temp"].apply(lambda values: (values >= threshold).sum())


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    period = weather[weather["year"].between(first_year, last_year)]
    totals = period.groupby(["year", "month"])["rain"].sum(min_count=1)
    return totals.groupby(level="month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""

    char_data = hot_days(weather)

    fig, ax = plt.subplots(figsize=(25, 10))
    char_data.plot.bar(ax=ax)
    ax.set_ylabel("hot days")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    fig.savefig(path)


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    rainy_weather = weather.copy()
    rainy_weather["rainy"] = (rainy_weather["rain"] >= threshold).astype(int)
    rainy_weather["rainy_tomorrow"] = rainy_weather["rainy"].shift(-1)
    return rainy_weather


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    train_data = weather[weather["year"] <= last_train_year]
    test_data = weather[weather["year"] > last_train_year]
    return train_data, test_data


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    accuracies = {}
    test2 = test.dropna(subset=["rainy_tomorrow"])
    accuracies["never"] = float((test2["rainy_tomorrow"] == 0).mean())
    accuracies["same"] = float((test2["rainy"] == test2["rainy_tomorrow"]).mean())
    return accuracies


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    weather_with_rainy = add_rainy(weather)
    clear_weather_with_rainy = weather_with_rainy.dropna(subset=["rainy_tomorrow", *features])
    weather_newer_1947 = clear_weather_with_rainy[clear_weather_with_rainy["year"] >= 1947]
    train_data, test_data = split_by_year(weather_newer_1947, 2015)
    baseline_on_test_data = baselines(test_data)
    train_features = train_data[features]
    test_features = test_data[features]
    train_targets = train_data["rainy_tomorrow"]
    test_targets = test_data["rainy_tomorrow"]

    results = []

    for depth in depths:
        tree = DecisionTreeClassifier(max_depth=depth, random_state=1)
        tree.fit(train_features, train_targets)
        train_accuracy = tree.score(train_features, train_targets)
        test_accuracy = tree.score(test_features, test_targets)
        results.append((depth, train_accuracy, test_accuracy))

    return results, baseline_on_test_data


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    print("1:", len(weather), "days", "from", weather["year"].min(), "to", weather["year"].max())

    max_temp_missing = missing_per_year(weather, "max_temp")
    nearly_unmeasured = max_temp_missing[max_temp_missing >= weather.groupby("year").size() * 0.95]
    mean_temp_missing = missing_per_year(weather, "mean_temp")

    print("2: max temp missing nearly all days:")
    for year in nearly_unmeasured.index:
        print(year, "max temp:", max_temp_missing[year], "mean temp:", mean_temp_missing[year])

    hot = hot_days(weather, threshold=30.0)
    hotest_days = hot.max()
    years = list(hot[hot == hotest_days].index)

    print("3: number of hot days:", hotest_days, "in year:", years)

    print(
        "4: average hot days from 1951-1980:",
        int(hot.loc[1951:1980].mean()),
        "average hot days from 1996-2025:",
        int(hot.loc[1996:2025].mean()),
    )

    rain_month = monthly_rain(weather, 1951, 2025)
    wettest_month = rain_month.max()
    driest_month = rain_month.min()
    idx_wettest_month = rain_month.idxmax()
    idx_driest_month = rain_month.idxmin()
    print(
        "5: wettest month between 1947 and 2025:",
        idx_wettest_month,
        "month, average rain:",
        wettest_month.round(0),
        "mm driest month between 1947 and 2025:",
        idx_driest_month,
        "month, average rain:",
        driest_month.round(0),
        "mm",
    )
    plot_hot_days(weather, Path(__file__).with_name("hot_days.png"))

    feature_combinations = [
        ["rainy"],
        ["month"],
        ["rainy", "month"],
        ["rainy", "rain"],
        ["rainy", "humidity"],
        ["rainy", "pressure"],
        ["rainy", "clouds"],
        ["rainy", "sunshine"],
        ["rainy", "min_temp", "max_temp", "month"],
        ["rainy", "humidity", "pressure"],
        ["rainy", "humidity", "clouds"],
        ["rainy", "pressure", "clouds"],
        ["rainy", "rain", "humidity", "pressure"],
        ["rainy", "humidity", "pressure", "clouds", "month"],
        [
            "rainy",
            "mean_temp",
            "max_temp",
            "min_temp",
            "rain",
            "sunshine",
            "clouds",
            "humidity",
            "pressure",
            "month",
        ],
    ]
    depths = list(range(1, 21, 5))
    depths.append(None)
    print("")
    print("6:")
    for features in feature_combinations:
        rows, baseline_scores = model_table(weather, features, depths)
        print("")
        print("features:", features)
        print(
            f"baselines: {{'never': {baseline_scores['never']:.4f}, "
            f"'same': {baseline_scores['same']:.4f}}}"
        )
        print("")
        print(f"{'depths':>7} | {'train accuracies':>17} | {'test accuracies':>15}")
        for row in rows:
            depth, train_accuracy, test_accuracy = row
            print(f"{str(depth):>7} | {train_accuracy:>17.4f} | {test_accuracy:>15.4f}")
