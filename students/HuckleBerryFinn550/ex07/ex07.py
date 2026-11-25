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
    years = weather[(weather["year"] >= first_year) & (weather["year"] <= last_year)]
    total = years.groupby(["year", "month"])["rain"].sum()
    return total.groupby("month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    hot_days_data = hot_days(weather)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(hot_days_data.index, hot_days_data.values)
    ax.set_xlabel("Year")
    ax.set_ylabel("Days with max_temp of 30 °C or more")
    ax.set_title("Hot days per year in Mannheim")
    fig.savefig(path)
    plt.close(fig)


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    rainy = weather.copy()
    rainy["rainy"] = (rainy["rain"] >= threshold).astype(int)
    rainy["rainy_tomorrow"] = rainy["rainy"].shift(-1)
    return rainy


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    train = weather[weather["year"] <= last_train_year]
    test = weather[weather["year"] > last_train_year]
    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    test = test[test["rainy_tomorrow"].notna()]
    never = (test["rainy_tomorrow"] == 0).mean()
    same = (test["rainy"] == test["rainy_tomorrow"]).mean()
    return {"never": never, "same": same}


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    data = weather[weather["year"] >= 1947]
    data = add_rainy(data)
    data = data.dropna(subset=features + ["rainy_tomorrow"])
    train, test = split_by_year(data, 2015)

    data_table = []
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=1)
        model.fit(train[features], train["rainy_tomorrow"])
        train_accuracy = model.score(train[features], train["rainy_tomorrow"])
        test_accuracy = model.score(test[features], test["rainy_tomorrow"])
        data_table.append((depth, train_accuracy, test_accuracy))

    return data_table, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)
    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")

    # Answer 1: how many days, from which year to which
    print("1:", len(weather), "days, from", weather["year"].min(), "to", weather["year"].max())
    print("\n")
    # Answer 2: years where max_temp is missing on (almost) every day, and mean_temp for those days
    missing_max = missing_per_year(weather, "max_temp")
    missing_mean = missing_per_year(weather, "mean_temp")
    years = missing_max[missing_max > 300].index
    print("2: days with max_temp missing, in the years where it is missing on more than 300 days:")
    print(missing_max.loc[years])
    print("days with mean_temp missing (same years):")
    print(missing_mean.loc[years])
    print("\n")
    # Answer 3: the years with the most hot days
    hot = hot_days(weather)
    print("3: most hot days:")
    print(hot[hot == hot.max()])
    print("\n")
    # Answer 4: average hot days/year
    print("4: 1951-1980:", hot.loc[1951:1980].mean())
    print("   1996-2025:", hot.loc[1996:2025].mean())
    print("\n")
    # Answer 5: wettest and driest month
    rain = monthly_rain(weather, 1947, 2025)
    print("5: wettest month:", rain.idxmax(), round(rain.max(), 1), "mm")
    print("driest month: ", rain.idxmin(), round(rain.min(), 1), "mm")

    # The chart for hot days
    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")
    print("\n")
    # Answer 6: the baselines and the table for the best features
    features = ["humidity", "clouds", "pressure", "sunshine", "month", "rainy"]
    table, base = model_table(weather, features, [1, 2, 3, 5, 10, None])
    print("6: baselines:", base)
    for depth, train_accuracy, test_accuracy in table:
        print(f"depth {str(depth)}   train {train_accuracy}   test {test_accuracy}")
