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
        # separation through semicolons, skip spaces, change -999 to NaN
        path,
        sep=";",
        skipinitialspace=True,
        na_values=[-999],
    )
    # print(list(COLUMNS))
    weather = weather[list(COLUMNS)]  # select all cols with already existing dict
    weather = weather.rename(columns=COLUMNS)  # renaming columns

    weather["year"] = weather["date"] // 10000  # all cols: AAAABBCC --> AAAA
    weather["month"] = (weather["date"] // 100) % 100
    return weather


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    missing = weather[column].isna()
    years = missing.groupby(weather["year"])
    # print(years.sum)
    return years.sum()  # true 1, false 0


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    measured = weather.copy()  # original weather shouldn't change
    measured = measured[
        measured["max_temp"].notna()
    ]  # content within outer "[]" filters the rows; notna() keeps only rows with max temp

    measured["hot"] = measured["max_temp"] >= threshold
    # print(measured)
    return measured.groupby("year")["hot"].sum()


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    wanted = weather[
        (weather["year"] >= first_year) & (weather["year"] <= last_year)
    ]  # select rows with correct years
    grouped = wanted.groupby(["year", "month"])  # we want year-month combinations
    monthly_totals = grouped["rain"].sum()  # total rain for a month
    grouped_months = monthly_totals.groupby("month")
    monthly_averages = grouped_months.mean()  # calculate avg for certain month (of different years)
    return monthly_averages


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    counts = hot_days(weather)  # use our function to count hot days
    fig, ax = plt.subplots(
        figsize=(12, 4)
    )  # matplotlib diagram; keyword argument figsize=(12, 4) for size in inches
    ax.bar(counts.index, counts)  # method bar from object ax; years on x axis, hot days on y axis
    ax.set_xlabel("Year")
    ax.set_ylabel("Days with at least 30 °C")
    ax.set_title("Hot days per year in Mannheim")
    fig.tight_layout()  # optimize distances automatically
    fig.savefig(path)
    plt.close(fig)


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    result = weather.copy()

    result["rainy"] = (result["rain"] >= threshold).astype(int)

    result["rainy_tomorrow"] = result["rainy"].shift(
        -1
    )  # shift(-1) shifts values of a col 1 line up
    return result  # result makes only sense when data for tomorrow is not missing!


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    train = weather[weather["year"] <= last_train_year]
    test = weather[weather["year"] > last_train_year]
    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    known = test[test["rainy_tomorrow"].notna()]  # checks if values are not NaN
    return {
        "never": (known["rainy_tomorrow"] == 0).mean(),  # no rain, compared to tomorrow
        "same": (
            known["rainy"] == known["rainy_tomorrow"]
        ).mean(),  # current state of rainy, compared to tomorrow
    }


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    data = add_rainy(weather)
    data = data[data["year"] >= 1947]
    data = data.dropna(subset=features + ["rainy_tomorrow"])  # remove rows with empty values
    train, test = split_by_year(data, 2015)  # split train and test data

    train_features = train[features]
    train_label = train["rainy_tomorrow"]
    test_features = test[features]
    test_label = test["rainy_tomorrow"]

    rows = []
    for depth in depths:
        tree = DecisionTreeClassifier(
            max_depth=depth, random_state=1
        )  # decision tree; random_state=1 makes result reproducable
        tree.fit(train_features, train_label)
        train_score = tree.score(train_features, train_label)
        test_score = tree.score(test_features, test_label)
        rows.append((depth, train_score, test_score))

    return rows, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)

    print(
        "1: Days:",
        len(weather),
        "Period:",
        weather["year"].min(),
        "to",
        weather["year"].max(),
    )
    missing_max = missing_per_year(weather, "max_temp")
    missing_mean = missing_per_year(weather, "mean_temp")
    day_counts = weather.groupby("year")["date"].count()
    almost_all_missing = missing_max[missing_max >= day_counts * 0.9]
    print("2: Years with at least 90% missing daily maximum temperatures:")
    print(
        pd.DataFrame(
            {
                "missing_max": almost_all_missing,
                "missing_mean": missing_mean.loc[almost_all_missing.index],
            }
        )
    )

    hot = hot_days(weather)
    most = hot.max()
    print("3: Most hot days:", list(hot[hot == most].index), "with", most, "days")
    print(
        "4: Average 1951-1980:", hot.loc[1951:1980].mean()
    )  # accessing part of a DataFrame by Name/Label
    print("   Average 1996-2025:", hot.loc[1996:2025].mean())

    rain = monthly_rain(weather, 1947, 2025)
    print(
        "5: Wettest month:", rain.idxmax(), "with", rain.max(), "mm"
    )  # idxmax() gives label of first occurrence of highest value
    print("   Driest month:", rain.idxmin(), "with", rain.min(), "mm")

    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")

    features = ["rainy", "humidity", "pressure"]
    depths = [1, 2, 3, 4, 5, 6, 8, None]
    results, base = model_table(weather, features, depths)
    print("6: Baselines:", base)
    print("   Model features:", features)
    for depth, train_score, test_score in results:
        print(
            "   Depth:",
            depth,
            "Train:",
            round(train_score, 3),
            "Test:",
            round(test_score, 3),
        )
