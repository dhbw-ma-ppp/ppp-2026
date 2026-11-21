# Exercise 07. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt  # noqa: F401  (you'll need it in Part 2)
import pandas as pd  # noqa: F401
from sklearn.tree import DecisionTreeClassifier  # noqa: F401  (you'll need it in Part 2)

# The DWD's daily data for Mannheim. It's large, so git ignores your copy of it (see README.md).
DATA_FILE = Path(__file__).parent / "mannheim.txt"
# A few lines of the same file, for the tests.
SAMPLE_FILE = Path(__file__).parent / "sample.txt"
LABEL = [
    "date",
    "mean_temp",
    "max_temp",
    "min_temp",
    "rain",
    "sunshine",
    "clouds",
    "humidity",
    "pressure",
    "year",
    "month",
]
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
    a = pd.read_csv(path, sep=";", na_values=-999, skipinitialspace=True)
    a = a[["MESS_DATUM", "TMK", "TXK", "TNK", "RSK", "SDK", "NM", "UPM", "PM"]]
    a = a.rename(columns=COLUMNS)
    a["year"] = a["date"] // 10000  # hinteren 4 Zahlen werden gelöscht
    a["month"] = a["date"] % 10000 // 100  # vordere 4 und hintere 2 Zahlen werden gelöscht
    return a


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    missing = weather.groupby("year")["date"].agg("count") - weather.groupby("year")[column].agg(
        "count"
    )
    return missing


def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    label = weather.columns
    weather = weather.loc[weather["max_temp"].notna(), label]
    weather["max_temp"] = weather["max_temp"] >= threshold
    hot = weather.groupby("year")["max_temp"].agg("sum")
    return hot


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    label = weather.columns
    weather = weather.loc[weather["rain"].notna(), label]
    weather_years = weather[(weather["year"] >= first_year) & (weather["year"] <= last_year)]
    rain_per_year = weather_years.groupby(["year", "month"])["rain"].agg("sum")
    weather_years = rain_per_year.groupby("month").agg("mean")
    return weather_years


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    a = hot_days(weather).to_dict()
    fig, ax = plt.subplots()
    ax.bar(a.keys(), a.values())
    fig.savefig(path)


def add_rainy(weather, threshold=1.0):  # test
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    last_day = len(weather)
    train = weather.copy()
    train["rainy"] = train["rain"].apply(lambda rain: 1 if rain >= threshold else 0)
    next_day = pd.Series(data=train["rainy"].iloc[1:].array)
    nan = pd.Series(data=float("nan"), index=[last_day])
    train["rainy_tomorrow"] = pd.concat([next_day, nan])
    return train


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    label = weather.columns
    return weather.loc[weather["year"] <= last_train_year, label], weather.loc[
        weather["year"] > last_train_year, label
    ]


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    never = (test["rainy_tomorrow"] == 0).mean()
    same = (test["rainy_tomorrow"] == test["rainy"]).mean()
    return {"never": never, "same": same}


def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    # Daten reinigen und sortieren
    data = add_rainy(weather)
    label1 = data.columns
    label2 = [*features, "rainy_tomorrow"]
    data = data.loc[data["year"] >= 1947, label1]

    train, test = split_by_year(data, 2015)
    train = train[label2].dropna()
    test = test[label2].dropna()
    train_x, train_y = train[features], train["rainy_tomorrow"]
    test_x, test_y = test[features], test["rainy_tomorrow"]
    base = baselines(test)

    # modell erstellen trainieren und testen
    ausgabe = []
    for depth in depths:
        tree = DecisionTreeClassifier(max_depth=depth)
        tree.fit(train_x, train_y)
        fitting_test = tree.predict(train_x)
        predictions = tree.predict(test_x)
        train_accuracy = (fitting_test == train_y).mean()
        test_accuracy = (predictions == test_y).mean()
        ausgabe.append((depth, train_accuracy, test_accuracy))
    return [ausgabe, base]


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(
        "1:", len(weather), "days from", weather["year"].iloc[0], "till", weather["year"].iloc[-1]
    )
    missing = missing_per_year(weather, "max_temp")
    missing = missing.loc[missing > 360]
    # Die Nans in max temp
    missing2 = weather.loc[(weather["year"] >= 1781) & (weather["year"] <= 1792)]
    missing2 = missing_per_year(missing2, "mean_temp")
    vergleich = pd.DataFrame(
        data={"year": missing.index, "max_temp": missing.array, "mean_temp": missing2.array}
    )
    print("2:", vergleich)
    hot = hot_days(weather)
    print("3:", hot.iloc[hot == hot.agg("max")])
    print("4", hot.loc[1951:1980].mean(), hot.loc[1996:2025].mean())
    wet = monthly_rain(weather, 1947, 2025)
    k = pd.DataFrame(data={"Wettest": wet.loc[wet == wet.max()], "Dry": wet.loc[wet == wet.min()]})
    print("5", k)

    data = add_rainy(weather)
    label = data.columns.drop(["rainy_tomorrow", "date"])
    print(label, data.columns, "lol")
    a, base = model_table(data, label, np.arange(1, len(label)))
    a.sort(key=lambda zwei: zwei[2])
    print("6", a[-1], base)
