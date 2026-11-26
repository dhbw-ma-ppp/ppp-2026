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
        na_values=[-999],
        sep=";",
        skipinitialspace=True,
    )
    weather = weather[list(COLUMNS)].rename(columns=COLUMNS)
    weather["year"] = weather["date"] // 10000
    weather["month"] = (weather["date"] // 100) % 100
    return weather


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    missing = weather[column].isna()
    return missing.groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    measured = weather.dropna(subset=["max_temp"])
    is_hot = measured["max_temp"] >= threshold
    return is_hot.groupby(measured["year"]).sum()


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    in_period = weather["year"].between(first_year, last_year)
    selected = weather.loc[in_period]
    monthly_totals = selected.groupby(["year", "month"])["rain"].sum(min_count=1)
    monthly_averages = monthly_totals.groupby(level="month").mean()
    return monthly_averages


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    yearly_counts = hot_days(weather)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(yearly_counts.index, yearly_counts.values, width=0.9)
    ax.set_title("Days reaching 30 °C or more in Mannheim")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of hot days")
    ax.set_xlim(weather["year"].min() - 0.5, weather["year"].max() + 0.5)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    result = weather.copy()
    result["rainy"] = (result["rain"] >= threshold).fillna(False).astype(int)
    result["rainy_tomorrow"] = result["rainy"].shift(-1)
    return result


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    train = weather.loc[weather["year"] <= last_train_year]
    test = weather.loc[weather["year"] > last_train_year]
    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    known = test.loc[test["rainy_tomorrow"].notna()]
    tomorrow = known["rainy_tomorrow"]
    return {
        "never": (tomorrow == 0).mean(),
        "same": (tomorrow == known["rainy"]).mean(),
    }


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    if "rainy_tomorrow" not in weather.columns:
        weather = add_rainy(weather)
    period = weather.loc[weather["year"].between(1947, 2025)]
    features = list(features)
    required = features + ["rainy_tomorrow"]
    complete = period.loc[period[required].notna().all(axis=1)]
    train, test = split_by_year(complete, 2015)
    x_train = train[features]
    y_train = train["rainy_tomorrow"]
    x_test = test[features]
    y_test = test["rainy_tomorrow"]
    rows = []
    for depth in depths:
        tree = DecisionTreeClassifier(max_depth=depth, random_state=1)
        tree.fit(x_train, y_train)
        train_accuracy = tree.score(x_train, y_train)
        test_accuracy = tree.score(x_test, y_test)
        rows.append((depth, train_accuracy, test_accuracy))
    return rows, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    print()

    # for Answer 1: how many days does the file have, and from which year to which?
    first_year = weather["year"].min()
    last_year = weather["year"].max()
    print(f"Answer 1: The file contains {len(weather)} days, from {first_year} to {last_year}.")

    print()

    # for Answer 2: in which years is `max_temp` missing on (almost) every day? Look at `mean_temp` for
    # the same years. What does that tell you about the station's history?
    days_per_year = weather.groupby("year").size()
    missing_max_temp = missing_per_year(weather, "max_temp")
    missing_mean_temp = missing_per_year(weather, "mean_temp")
    summary_of_missing_max_temp = pd.DataFrame(
        {
            "recorded_days": days_per_year,
            "missing_max_temp": missing_max_temp,
            "missing_mean_temp": missing_mean_temp,
        }
    )
    selected_years = missing_max_temp >= 0.95 * days_per_year
    print("Answer 2: Years with max_temp missing on nearly all recorded days")
    print(summary_of_missing_max_temp[selected_years].to_string())
    # This tells us that the weather station was already recording the temperature in general,
    # but didn't record the max temperature or the data was lost in some way or another. After a big time gap
    # we can see that they were keeping track of it right after the gap, as seen in mannheim.txt

    print()
    # for Answer 3: which year had the most hot days (30 °C or more), and how many?
    # (If several years tie, give all of them.)
    hot_days_per_year = hot_days(weather)
    most_hot_days = hot_days_per_year.max()
    recorded_years = hot_days_per_year[hot_days_per_year == most_hot_days]

    print("Answer 3: Years with the most hot days (= 30 °C or more) in every recorded year")
    for year, count in recorded_years.items():
        print(f"{year}: {count} hot days")

    # for Answer 4: Average the yearly counts in each period.
    average_early = hot_days_per_year.loc[1951:1980].mean()
    average_recent = hot_days_per_year.loc[1996:2025].mean()

    print()

    print("Answer 4: Average hot days per year in the following two time periods")
    print(f"1951–1980: {average_early:.1f}")
    print(f"1996–2025: {average_recent:.1f}\n")

    # for Answer 5: over 1947–2025, the wettest and the driest month, with their averages.
    averages = monthly_rain(weather, 1947, 2025)
    wettest = averages.idxmax()
    driest = averages.idxmin()
    print("Answer 5: Average monthly rainfall in Mannheim (1947–2025)")
    print(f"Wettest month: {wettest} ({averages[wettest]:.1f} mm)")
    print(f"Driest month: {driest} ({averages[driest]:.1f} mm)\n")

    # For saving the hot_day bar chart
    plot_hot_days(weather, Path(__file__).with_name("hot_days.png"))

    # for Answer 6: the two baselines; and a table of depth, train accuracy and test accuracy for your
    # best choice of features.
    features = ["month", "rainy", "humidity", "pressure", "clouds"]
    depths = [1, 2, 3, 5, 10, 20, None]

    rows, baseline_scores = model_table(weather, features, depths)

    print("Answer 6: Predicting rain tomorrow")
    print("Features:", ", ".join(features))
    print(f"Never predicts rain: {baseline_scores['never']:.1%}")
    print(f"Predicts the same as today: {baseline_scores['same']:.1%}s\n")
    print(f"{'Depth':>6}  {'Train accuracy':>15}  {'Test accuracy':>15}")
    for depth, train_accuracy, test_accuracy in rows:
        print(f"{str(depth):>6}  {train_accuracy:>15.1%}  {test_accuracy:>15.1%}")
