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


def load_weather(path: Path) -> pd.DataFrame:
    """Read a DWD daily climate file into a DataFrame.

    Keep only the columns in COLUMNS, with our names; -999 (missing) becomes NaN. Add the
    columns `year` and `month`, as ints, worked out from `date` (an int such as 19470101).
    """
    weather = pd.read_csv(
        path,
        sep=";",
        na_values=[-999],
        skiprows=1,
        header=None,
        usecols=[1, 6, 8, 10, 12, 13, 14, 15, 16],
        names=[
            "date",
            "rain",
            "sunshine",
            "clouds",
            "pressure",
            "mean_temp",
            "humidity",
            "max_temp",
            "min_temp",
        ],
    )[list(COLUMNS.values())]
    weather["year"] = weather["date"] // 10000
    weather["month"] = (weather["date"] // 100) % 100
    return weather


def missing_per_year(weather: pd.DataFrame, column: str) -> pd.Series:
    """For every year in `weather`: on how many days `column` is missing (NaN)."""
    return (
        pd.merge(
            weather["year"].value_counts(),
            weather.loc[weather[column].isna(), ["year", column]]["year"].value_counts(),
            how="left",
            on="year",
        )["count_y"]
        .fillna(0)
        .convert_dtypes()
    )


def hot_days(weather: pd.DataFrame, threshold: int = 30.0) -> pd.Series:
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    return (
        pd.merge(
            weather.loc[weather["max_temp"].notna()]["year"].value_counts(),
            weather.loc[weather["max_temp"] >= threshold]["year"].value_counts(),
            how="left",
            on="year",
        )["count_y"]
        .fillna(0)
        .convert_dtypes()  # makes values ints rather than floats
    )


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather: pd.DataFrame, first_year: int, last_year: int) -> pd.Series:
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    temp = weather.copy()
    return (
        temp.loc[first_year <= temp["year"]]
        .loc[temp["year"] <= last_year]
        .groupby(["year", "month"])
        .sum()
        .groupby("month")
        .mean()["rain"]
    )


def plot_hot_days(weather: pd.DataFrame, path: Path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    plt.bar(hot_days(weather).index, hot_days(weather).values)
    plt.savefig(path)


def add_rainy(weather: pd.DataFrame, threshold: int = 1.0) -> pd.DataFrame:
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    output = weather.copy()
    output["rainy"] = (output["rain"] >= threshold).astype(int)
    output["rainy_tomorrow"] = output["rainy"].shift(-1)
    return output


def split_by_year(weather: pd.DataFrame, last_train_year: int) -> tuple[pd.DataFrame]:
    """Rows up to and including last_train_year, and the rows after it."""
    return (
        weather.loc[weather["year"] <= last_train_year],
        weather.loc[weather["year"] > last_train_year],
    )


def model_never(day: pd.Series) -> int:
    return 0


def model_same(day: pd.Series) -> int:
    return day.at["rainy"]


def accuracy(model, test: pd.DataFrame) -> float:
    return float((test.apply(model, axis=1) == test["rainy_tomorrow"]).mean())


def baselines(test: pd.DataFrame) -> dict[str:float]:
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    return {"never": accuracy(model_never, test), "same": accuracy(model_same, test)}


def model_table(
    weather: pd.DataFrame, features: list[str], depths: list[int]
) -> tuple[list[tuple[int]], dict[str:float]]:
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """
    results = []
    train, test = split_by_year(weather.loc[weather["year"] >= 1947], 2015)
    train = train[features + ["rainy_tomorrow"]].dropna()
    test = test[features + ["rainy_tomorrow"]].dropna()
    for depth in depths:
        tree = DecisionTreeClassifier(max_depth=depth, random_state=1)
        tree.fit(train[features], train["rainy_tomorrow"])
        results.append(
            (
                depth,
                float(
                    (tree.predict(train[features]) == train["rainy_tomorrow"]).astype(int).mean()
                ),
                float((tree.predict(test[features]) == test["rainy_tomorrow"]).astype(int).mean()),
            )
        )
    _, test = split_by_year(weather.loc[weather["year"] >= 1947], 2015)
    return results, baselines(test)


if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)

    print(
        f"1:"
        f"\tThe file has {weather['date'].count()} days and goes from the year {weather['year'].min()} to the year {weather['year'].max()}.\n"
    )

    missing_max_temp = missing_per_year(weather, "max_temp")
    missing_max_temp = missing_max_temp.loc[missing_max_temp > 300]
    missing_mean_temp = missing_per_year(weather, "mean_temp")
    missing_mean_temp = missing_mean_temp.loc[missing_mean_temp > 300]
    print(
        f"2:"
        f"\t`max_temp` was missing on almost every day of the year{'' if missing_max_temp.size == 1 else 's'} {missing_max_temp.keys().to_numpy()} while `mean_temp` is missing from {missing_mean_temp.keys().to_numpy()}.\n"
        f"\tThis tells us that the weather station was not recording the maximum temperature until {missing_max_temp.keys().to_numpy().max() + 1}.\n"
    )

    hot_days_series = hot_days(weather)
    hot_years = hot_days_series.loc[hot_days_series == hot_days_series.max()].index.to_numpy()
    print(
        f"3:"
        f"\tThe year{'' if hot_years.size == 1 else 's'} {hot_years} had the most hot days with {hot_days_series.max()} hot days.\n"
    )

    hot_days_1951__ = hot_days_series.loc[1951 <= hot_days_series.keys()]
    avg_hot_days_1951_1980 = hot_days_1951__.loc[hot_days_1951__.keys() <= 1980].mean()
    hot_days_1990__ = hot_days_series.loc[1996 <= hot_days_series.keys()]
    avg_hot_days_1996_2025 = hot_days_1990__.loc[hot_days_1990__.keys() <= 2025].mean()
    print(
        f"4:"
        f"\tThere {'was' if avg_hot_days_1951_1980 == 1 else 'were'} {avg_hot_days_1951_1980} hot day{'' if avg_hot_days_1951_1980 == 1 else 's'} between 1951 and 1980.\n"
        f"\tThere {'was' if avg_hot_days_1996_2025 == 1 else 'were'} {avg_hot_days_1996_2025} hot day{'' if avg_hot_days_1996_2025 == 1 else 's'} between 1996 and 2025.\n"
    )

    monthly_rain_s = monthly_rain(weather, 2000, 2020)
    wettest_month = monthly_rain_s.loc[monthly_rain_s == monthly_rain_s.max()]
    driest_month = monthly_rain_s.loc[monthly_rain_s == monthly_rain_s.min()]
    print(
        f"5:"
        f"\tThe wettest month on average from 1947 to 2025 was month {wettest_month.index.item()} with an average total rain of {wettest_month.item()}.\n"
        f"\tThe driest month on average from 1947 to 2025 was month {driest_month.index.item()} with an average total rain of {driest_month.item()}.\n"
    )

    plot_hot_days(weather, Path(__file__).parent / "hot_days.png")

    rainy_df = add_rainy(weather)
    features = ["rain", "clouds", "humidity"]
    rows, base = model_table(
        rainy_df,
        features,
        [3, 4, 5, 6, 7],
    )
    print(
        f"6:"
        f"\tBaselines: {base}\n"
        f"\tModel with features {features}:\n"
        f"\tdepth\ttrain accuracy\ttest accuracy"
    )
    for row in rows:
        print(f"\t{row[0]}\t{round(row[1], 5)}\t\t{round(row[2], 5)}")
