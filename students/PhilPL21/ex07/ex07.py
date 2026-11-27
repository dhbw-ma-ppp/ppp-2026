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
    data_field = pd.read_csv(
        path,
        sep=";",
        skipinitialspace=True,
        na_values=[-999],
        usecols=list(COLUMNS.keys()),
    )

    data_field = data_field[list(COLUMNS.keys())].rename(columns=COLUMNS)

    data_field["year"] = (data_field["date"] // 10000).astype(int)
    data_field["month"] = ((data_field["date"] // 100) % 100).astype(int)

    return data_field


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather[column].isna().groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    known = weather.dropna(subset=["max_temp"])
    return known.groupby("year")["max_temp"].apply(
        lambda temperatures: (temperatures >= threshold).sum()
    )


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    selected = weather[weather["year"].between(first_year, last_year)]

    totals_per_year = selected.groupby(["year", "month"])["rain"].sum(min_count=1).reset_index()

    averages = totals_per_year.groupby("month")["rain"].mean()

    return averages


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
    result = weather.copy()

    result["rainy"] = result["rain"].ge(threshold).where(result["rain"].notna()).astype(float)

    result["rainy_tomorrow"] = result["rainy"].shift(-1)

    return result


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    train = weather[weather["year"] <= last_train_year].copy()
    test = weather[weather["year"] > last_train_year].copy()

    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    known_tomorrow = test.dropna(subset=["rainy_tomorrow"])

    never_accuracy = (known_tomorrow["rainy_tomorrow"] == 0).mean()

    known_today_and_tomorrow = known_tomorrow.dropna(subset=["rainy"])

    same_accuracy = (
        known_today_and_tomorrow["rainy"] == known_today_and_tomorrow["rainy_tomorrow"]
    ).mean()

    return {
        "never": never_accuracy,
        "same": same_accuracy,
    }


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    data = weather.copy()

    if "rainy" not in data.columns or "rainy_tomorrow" not in data.columns:
        data = add_rainy(data)

    data = data[data["year"].between(1947, 2025)]
    train, test = split_by_year(data, 2015)

    train = train.dropna(subset=list(features) + ["rainy_tomorrow"])
    test = test.dropna(subset=list(features) + ["rainy_tomorrow"])

    X_train = train[list(features)]
    y_train = train["rainy_tomorrow"].astype(int)
    X_test = test[list(features)]
    y_test = test["rainy_tomorrow"].astype(int)

    rows = []
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=1)
        model.fit(X_train, y_train)

        rows.append(
            (
                depth,
                model.score(X_train, y_train),
                model.score(X_test, y_test),
            )
        )

    return rows, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    # 1. Number of measurements and time period
    print("Answer 1:")
    print("Number of days:", len(weather))
    print("First year:", weather["year"].min())
    print("Last year:", weather["year"].max())

    # 2. Missing values and yearly mean temperature
    missing_max = missing_per_year(weather, "max_temp")
    missing_mean = missing_per_year(weather, "mean_temp")

    missing_years = missing_max[missing_max >= 350].index

    print("Answer 2: Missing:")
    print("max_temp:")
    print(missing_max.loc[missing_years])

    print("mean_temp:")
    print(missing_mean.loc[missing_years])

    # 3. Number of hot days per year
    hot = hot_days(weather)

    max_hot_days = hot.max()
    years_with_most_hot_days = hot[hot == max_hot_days]

    print("Answer 3: Hot days")
    print("Years with the most hot days:")
    print(years_with_most_hot_days)
    print("Maximum number of hot days:", max_hot_days)

    # 4. Average number of hot days in two periods
    hot_1951_1980 = hot.loc[1951:1980].mean()
    hot_1996_2025 = hot.loc[1996:2025].mean()

    print("Answer 4:")
    print("Average hot days 1951-1980:", round(hot_1951_1980, 2))
    print("Average hot days 1996-2025:", round(hot_1996_2025, 2))

    # 5. Average monthly rainfall
    rain = monthly_rain(weather, 1947, 2025)

    print("Answer 5:")
    print("Average rainfall per month:")

    print("Wettest month:", rain.idxmax(), "with", round(rain.max(), 2), "mm")
    print("Driest month:", rain.idxmin(), "with", round(rain.min(), 2), "mm")

    # 6. Baselines
    rows, base = model_table(weather, ["rainy", "humidity"], [1, 3, 5, None])

    print(base)

    for row in rows:
        print(row)
