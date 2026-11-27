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
    data_frame = pd.read_csv(path, sep=";", skipinitialspace=True, na_values=-999)

    data_frame = data_frame[list(COLUMNS.keys())].rename(columns=COLUMNS)

    data_frame["year"] = data_frame["date"] // 10000
    data_frame["month"] = (data_frame["date"] % 10000) // 100

    return data_frame


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return weather.groupby("year")[column].apply(lambda s: s.isna().sum())


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    known = weather.dropna(subset=["max_temp"])
    return known.groupby("year")["max_temp"].apply(lambda s: (s >= threshold).sum())


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    subset = weather[(weather["year"] >= first_year) & (weather["year"] <= last_year)]
    monthly_totals = subset.groupby(["year", "month"])["rain"].sum()
    return monthly_totals.groupby("month").mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    counts = hot_days(weather)
    fig, ax = plt.subplots(figsize=(12, 5))
    counts.plot(kind="bar", ax=ax, width=0.8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Num hot days")
    ax.set_title("Hot days/year")
    step = max(1, len(counts) // 20)
    ax.set_xticks(range(0, len(counts), step))
    ax.set_xticklabels(counts.index[::step], rotation=45)
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
    valid = test.dropna(subset=["rainy_tomorrow"])
    y_true = valid["rainy_tomorrow"]
    never_acc = (y_true == 0).mean()
    same_acc = (valid["rainy"] == y_true).mean()
    return {"never": never_acc, "same": same_acc}


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """

    data = weather[weather["year"] >= 1947].copy()
    data = add_rainy(data)
    data = data.dropna(subset=features + ["rainy_tomorrow", "year"])

    train, test = split_by_year(data, 2015)
    X_train, y_train = train[features], train["rainy_tomorrow"]
    X_test, y_test = test[features], test["rainy_tomorrow"]

    rows = []
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=1)
        model.fit(X_train, y_train)
        rows.append((depth, model.score(X_train, y_train), model.score(X_test, y_test)))

    return rows, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)

    print("1:", len(weather), "days from", weather["date"].min(), "to", weather["date"].max())

    missing_max = missing_per_year(weather, "max_temp")
    almost_all = missing_max[missing_max > 300]
    print("2: years with almost no max_temp:", almost_all.index.tolist())
    print(
        "   corresponding mean_temp missing:",
        missing_per_year(weather, "mean_temp").loc[almost_all.index].to_dict(),
    )

    hot = hot_days(weather)
    max_hot = hot.max()
    best_years = hot[hot == max_hot].index.tolist()
    print("3:", best_years, "with", max_hot, "hot days")

    print("4: 1951–1980 average:", round(hot.loc[1951:1980].mean(), 2))
    print("   1996–2025 average:", round(hot.loc[1996:2025].mean(), 2))

    rain = monthly_rain(weather, 1947, 2025)
    print("5: wettest month", rain.idxmax(), "with", round(rain.max(), 1), "mm")
    print("   driest month ", rain.idxmin(), "with", round(rain.min(), 1), "mm")

    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")
    print("   (hot_days.png saved)")

    features = ["rainy", "humidity", "month"]
    rows, base = model_table(weather, features, [1, 2, 3, None])
    print("6: baselines:", base)
    print("   depth | train  | test")
    for depth, tr, te in rows:
        print(f"   {str(depth):5} | {tr:.3f} | {te:.3f}")
