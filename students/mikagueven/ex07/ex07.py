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
    daily = pd.read_csv(
        path, sep=";", na_values=-999, usecols=COLUMNS.keys(), skipinitialspace=True
    )  # read file, cols seperated by ;, set -999 to NaN, filter cols, remove initial whitespace
    daily = daily.rename(columns=COLUMNS)  # rename cols
    daily = daily[list(COLUMNS.values())]  # sort cols to use right order
    daily["year"] = daily["date"].astype(str).str[:4].astype(int)
    daily["month"] = daily["date"].astype(str).str[4:6].astype(int)
    return daily


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    missing = weather[column].isna()  # check which values are missing
    result = missing.groupby(weather["year"]).sum()  # count missing values per year
    return result


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    valid = weather.dropna(subset=["max_temp"])  # remove days with missing max_temp
    is_hot = valid["max_temp"] >= threshold  # check which days reached the temperature threshold
    result = is_hot.groupby(valid["year"]).sum()  # count hot days per year
    return result


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    if first_year > last_year:
        raise ValueError("First year must not be greater than last year!")
    sub = weather[
        (weather["year"] >= first_year) & (weather["year"] <= last_year)
    ]  # select the requested years
    yearly_month_totals = sub.groupby(["year", "month"])[
        "rain"
    ].sum()  # calculate total rain per month and year
    result = yearly_month_totals.groupby(
        level="month"
    ).mean()  # calculate average rain for each month
    return result


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    counts = hot_days(weather)  # calculate hot days per year
    fig, ax = plt.subplots(figsize=(12, 5))  # create a new figure and chart
    ax.bar(counts.index, counts.values, width=0.9)  # create a bar chart
    ax.set_xlabel("Year")  # set x-axis label
    ax.set_ylabel("Hot days (>= 30 °C)")  # set y-axis label
    ax.set_title("Hot days per year")  # set chart title
    ax.set_xlim(weather["year"].min() - 0.5, weather["year"].max() + 0.5)
    fig.tight_layout()  # adjust spacing
    fig.savefig(path)  # save chart as an image
    plt.close(fig)


def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    df = weather.copy()  # create a copy of the weather data
    df["rainy"] = (df["rain"] >= threshold).astype(int)  # set 1 if it rains, otherwise 0
    df["rainy_tomorrow"] = df["rainy"].shift(
        -1
    )  # move rainy values one row up to get tomorrow's rain
    return df


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    train = weather[
        weather["year"] <= last_train_year
    ]  # select training data up to last_train_year
    test = weather[weather["year"] > last_train_year]  # select testing data after last_train_year
    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    valid = test.dropna(subset=["rainy_tomorrow"])  # remove rows without tomorrow's rain data
    never_acc = float((valid["rainy_tomorrow"] == 0).mean())  # accuracy if it never predicts rain
    same_acc = float(
        (valid["rainy_tomorrow"] == valid["rainy"]).mean()
    )  # accuracy if tomorrow is like today
    return {"never": never_acc, "same": same_acc}


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    df = (
        weather if "rainy_tomorrow" in weather.columns else add_rainy(weather)
    )  # add rainy columns if missing
    df = df[df["year"] >= 1947].dropna(
        subset=list(features) + ["rainy_tomorrow"]
    )  # select years and remove missing values
    train, test = split_by_year(df, 2015)  # split data into training and testing sets
    X_train, y_train = (
        train[features],
        train["rainy_tomorrow"],
    )  # prepare training inputs and correct answers
    X_test, y_test = (
        test[features],
        test["rainy_tomorrow"],
    )  # prepare testing inputs and correct answers
    results = []  # store accuracy results for each tree
    for d in depths:
        tree = DecisionTreeClassifier(
            max_depth=d, random_state=1
        )  # create decision tree with selected depth
        tree.fit(X_train, y_train)  # train the decision tree
        train_acc = float(tree.score(X_train, y_train))  # calculate accuracy on training data
        test_acc = float(tree.score(X_test, y_test))  # calculate accuracy on testing data
        results.append((d, train_acc, test_acc))  # save depth and both accuracy values
    return results, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)
    # Print your answers here, e.g. print("1:", ...)
    # Answer 1: Print the total number of recorded days and the first and last year
    print(f"1: {len(weather)} days, from {weather['year'].min()} to {weather['year'].max()}")

    # Answer 2: Count how many days per year have missing temperature values
    m_max = missing_per_year(weather, "max_temp")  # count missing maximum temperatures
    m_mean = missing_per_year(weather, "mean_temp")  # count missing average temperatures
    # Find years where the maximum temperature is missing on more than 300 days
    bad_years = m_max[m_max > 300].index
    # Print the missing values for both temperature columns in each affected year
    for year in bad_years:
        print(f"2: {year}: max_temp missing = {m_max[year]}, mean_temp missing = {m_mean[year]}")

    # Answer 3: Find the year with the highest number of hot days (at least 30 C)
    hd = hot_days(weather)  # count hot days for every year
    max_hd = hd.max()  # find the highest number of hot days
    top_years = list(hd[hd == max_hd].index)  # get all years with the highest number
    print(f"3: {top_years} with {max_hd} hot days")

    # Answer 4: Compare the average number of hot days in two different 30-year periods
    avg_old = hd.loc[1951:1980].mean()  # calculate the average for 1951 to 1980
    avg_new = hd.loc[1996:2025].mean()  # calculate the average for 1996 to 2025
    print(f"4: 1951-1980 = {avg_old:.2f}, 1996-2025 = {avg_new:.2f}")

    # Answer 5: Find which month has the highest and lowest average rainfall
    # calculate average rainfall for each month from 1947 to 2025
    mr = monthly_rain(weather, 1947, 2025)
    # get the month number with the highest average rainfall
    wettest_month = mr.idxmax()
    # get the month number with the lowest average rainfall
    driest_month = mr.idxmin()

    print(
        f"5: wettest = month {wettest_month} ({mr[wettest_month]:.1f} mm), "
        f"driest = month {driest_month} ({mr[driest_month]:.1f} mm)"
    )

    # Plot Hot Days
    out_path = Path(__file__).parent / "hot_days.png"
    plot_hot_days(weather, out_path)

    # Answer 6: Predict whether it will rain on the next day using weather data
    features = [
        "rain",
        "rainy",
        "humidity",
        "pressure",
        "clouds",
        "mean_temp",
    ]  # select the weather values used for prediction
    depths = [1, 2, 3, 4, 5, 6, 8, 10, None]  # different maximum tree depths to compare

    # Train decision trees with different depths and calculate their accuracy
    rows, base = model_table(weather, features, depths)

    print("6:")
    # Print the accuracy of two simple prediction methods for comparison
    print(f"  Baselines: never = {base['never']:.4f}, same = {base['same']:.4f}")
    print("  Depth | Train Acc | Test Acc")
    for depth, train_acc, test_acc in rows:
        # Print the tree depth and its accuracy on training and testing data
        print(f"  {str(depth):>5} | {train_acc:9.4f} | {test_acc:8.4f}")
