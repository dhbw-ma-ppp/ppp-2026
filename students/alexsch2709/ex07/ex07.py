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
    weather = pd.read_csv(
        path,
        sep=";",
        skipinitialspace=True,
        na_values=-999
    )
    weather = weather[list(COLUMNS.keys())]
    weather = weather.rename(columns=COLUMNS)

    weather["year"] = weather["date"] // 10000
    weather["month"] = (weather["date"] // 100) % 100

    return weather


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather.groupby("year")[column].apply(
        lambda s: s.isna().sum()
    )


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    known = weather.dropna(subset=["max_temp"])

    return known.groupby("year")["max_temp"].apply(
        lambda s: (s >= threshold).sum()
    )


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    selected = weather[
        (weather["year"] >= first_year)
        & (weather["year"] <= last_year)
    ]
    monthly_totals = (
        selected
        .groupby(["year", "month"])["rain"]
        .sum()
    )

    return monthly_totals.groupby("month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    data = hot_days(weather)

    plt.figure(figsize=(12, 6))
    data.plot(kind="bar")

    plt.title("Hot days per year")
    plt.xlabel("Year")
    plt.ylabel("Number of hot days (>=30°C)")

    plt.tight_layout()
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
    valid = test.dropna(subset=["rainy_tomorrow"])
    actual = valid["rainy_tomorrow"]
    never = (actual == 0).mean()
    same = (valid["rainy"] == actual).mean()

    return {
        "never": never,
        "same": same
    }


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    if "rainy" not in weather.columns or "rainy_tomorrow" not in weather.columns:
        weather = add_rainy(weather)

    data = weather[weather["year"] >= 1947].copy()
    required = features + ["rainy_tomorrow"]
    data = data.dropna(subset=required)
    train, test = split_by_year(data, 2015)

    x_train = train[features]
    y_train = train["rainy_tomorrow"]
    x_test = test[features]
    y_test = test["rainy_tomorrow"]
    table = []

    for depth in depths:
        model = DecisionTreeClassifier(
            max_depth=depth,
            random_state=1
        )
        model.fit(x_train, y_train)
        table.append(
            (
                depth,
                model.score(x_train, y_train),
                model.score(x_test, y_test),
            )
        )

    return table, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)

    # Answer 1
    print("Answer 1")
    print("Number of days:", len(weather))
    print("From year:", weather["year"].min())
    print("To year:", weather["year"].max())

    # Answer 2
    print("\nAnswer 2")
    missing_max = missing_per_year(weather, "max_temp")
    missing_mean = missing_per_year(weather, "mean_temp")

    print("Years with the most missing max_temp values:")
    print(missing_max.sort_values(ascending=False).head(10))

    print("\nMissing mean_temp values in the same years:")
    print(missing_mean.loc[missing_max.sort_values(ascending=False).head(10).index])

    # Answer 3
    print("\nAnswer 3")
    hot = hot_days(weather)

    max_hot_days = hot.max()
    hottest_years = hot[hot == max_hot_days].index.tolist()

    print("Most hot days:", max_hot_days)
    print("Year(s):", hottest_years)

    # Answer 4
    print("\nAnswer 4")

    avg_1951_1980 = hot.loc[1951:1980].mean()
    avg_1996_2025 = hot.loc[1996:2025].mean()

    print("Average hot days per year (1951-1980):", round(avg_1951_1980, 2))
    print("Average hot days per year (1996-2025):", round(avg_1996_2025, 2))

    # Answer 5
    print("\nAnswer 5")

    rain = monthly_rain(weather, 1947, 2025)

    wettest_month = rain.idxmax()
    driest_month = rain.idxmin()

    print(
        "Wettest month:",
        wettest_month,
        "Average rain:",
        round(rain.max(), 2),
        "mm"
    )

    print(
        "Driest month:",
        driest_month,
        "Average rain:",
        round(rain.min(), 2),
        "mm"
    )

    # Create hot_days.png
    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")

    # Answer 6
    print("\nAnswer 6")

    rows, base = model_table(
        weather,
        ["rainy", "humidity"],
        [1, 2, 3, 5, None]
    )

    print("Baselines:")
    print(base)

    print("\nDepth | Train Accuracy | Test Accuracy")
    for depth, train_score, test_score in rows:
        print(depth, "|", round(train_score, 3), "|", round(test_score, 3))
