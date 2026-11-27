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
    table = pd.read_csv(path, sep=";", skipinitialspace=True, na_values=[-999, "-999"])
    # Header names are padded with spaces too; strip them to be safe.
    table.columns = table.columns.str.strip()
    weather = table[list(COLUMNS)].rename(columns=COLUMNS)
    weather["year"] = (weather["date"] // 10000).astype(int)
    weather["month"] = (weather["date"] // 100 % 100).astype(int)
    return weather


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather[column].isna().groupby(weather["year"]).sum()


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    known = weather.dropna(subset=["max_temp"])
    return (known["max_temp"] >= threshold).groupby(known["year"]).sum()


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    selected = weather[(weather["year"] >= first_year) & (weather["year"] <= last_year)]
    totals = selected.groupby(["year", "month"])["rain"].sum()
    return totals.groupby("month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    hot = hot_days(weather)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(hot.index, hot.values)
    ax.set_xlabel("Year")
    ax.set_ylabel("Days with max_temp >= 30 °C")
    ax.set_title("Hot days per year, Mannheim")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


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
    return {
        "never": float((test["rainy_tomorrow"] == 0).mean()),
        "same": float((test["rainy"] == test["rainy_tomorrow"]).mean()),
    }


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    features = list(features)
    data = add_rainy(weather)
    data = data[data["year"] >= 1947]
    data = data.dropna(subset=features + ["rainy_tomorrow"])
    train, test = split_by_year(data, 2015)

    rows = []
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=1)
        model.fit(train[features], train["rainy_tomorrow"])
        rows.append(
            (
                depth,
                model.score(train[features], train["rainy_tomorrow"]),
                model.score(test[features], test["rainy_tomorrow"]),
            )
        )
    return rows, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")

    days = weather.groupby("year").size()
    miss_max = missing_per_year(weather, "max_temp")
    bad_years = miss_max[miss_max / days > 0.9]
    hot = hot_days(weather)
    rain = monthly_rain(weather, 1947, 2025)
    rows, base = model_table(
        weather, ["rainy", "humidity", "pressure", "clouds", "month"], [1, 2, 3, 5, 8, None]
    )

    print(
        # Antwort 1: Anzahl Tage und Zeitraum
        f"1: Anzahl der {len(weather)} Tage, {weather['year'].min()} bis {weather['year'].max()}",
        # Antwort 2: Jahre, in denen max_temp fast immer fehlt, und mean_temp dort
        f"2: max_temp fehlt fast immer in:\n{bad_years}\n"
        f"   mean_temp fehlt dort an:\n{missing_per_year(weather, 'mean_temp')[bad_years.index]}",
        # Antwort 3: Jahr(e) mit den meisten heißen Tagen
        f"3: meiste heiße Tage: {hot[hot == hot.max()].to_dict()}",
        # Antwort 4: Durchschnitt heißer Tage pro Jahr in zwei Zeiträumen
        f"4: Ø 1951-1980: {hot.loc[1951:1980].mean():.1f}, Ø 1996-2025: {hot.loc[1996:2025].mean():.1f}",
        # Antwort 5: nassester und trockenster Monat (1947-2025)
        f"5: nassester Monat: {rain.idxmax()} ({rain.max():.1f} mm), "
        f"trockenster: {rain.idxmin()} ({rain.min():.1f} mm)",
        # Antwort 6: Baselines und Tabelle Tiefe / Train / Test
        f"6: Baselines: {base}\n   Tiefe  Train  Test\n"
        + "\n".join(f"   {str(d):>5}  {tr:.3f}  {te:.3f}" for d, tr, te in rows),
        sep="\n",
    )
