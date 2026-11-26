# Exercise 07. See README.md for the full task.
# Replace each `pass` line with your code, ending with `return`.

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401  (you'll need it in Part 2)
import pandas as pd  # noqa: F401
from sklearn.tree import DecisionTreeClassifier  # noqa: F401  (you'll need it in Part 2)
from sklearn.metrics import accuracy_score

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
    data = pd.read_csv(path, usecols=COLUMNS.keys(), sep=';', skipinitialspace=True, na_values=-999)
    data = data.rename(columns=COLUMNS)
    data['year'] = (data['date'] // 10000).astype(int)
    data['month'] = ((data['date'] // 100) % 100).astype(int)
    data = data[list(COLUMNS.values()) + ['year', 'month']]
    return data


def missing_per_year(weather, column):
    """For every year in `weather`: on how many days `column` is missing (NaN)."""

    result = {}

    for year in weather['year'].unique():
        year_data = weather[weather['year'] == year]

        missing = year_data[column].isna().sum()

        result[year] = missing

    return pd.Series(result)



def hot_days(weather, threshold=30.0):
    """For every year with at least one known max_temp: how many days reached `threshold`.

    A year with no such day has 0; a year without any max_temp isn't in the result.
    """
    hotDays = {}

    for year in weather['year'].unique():
        year_data = weather[weather['year'] == year]
        known_temps = year_data['max_temp'].dropna()

        if len(known_temps) > 0:
            hot = (known_temps >= threshold).sum()
            hotDays[year] = hot

    return pd.Series(hotDays)


# ---------------------------------------------------------------- Part 2 (at home)


def monthly_rain(weather, first_year, last_year):
    """The average total rain of each month (1 to 12), over the years first_year..last_year."""
    
    selected = weather[(weather['year'] >= first_year) &(weather['year'] <= last_year)]
    monthly_totals = selected.groupby(['year', 'month'])['rain'].sum(min_count=1)

    return monthly_totals.groupby('month').mean()


def plot_hot_days(weather, path):
    """Save a bar chart of hot days (30 °C or more) per year as a picture at `path`."""
    hotDays = hot_days(weather)

    plt.figure(figsize=(14, 6))

    hotDays.plot(kind='bar')

    plt.xlabel('Year')
    plt.ylabel('Number of hot days')
    plt.title('Number of hot days (30 °C or more) per year')

    plt.tight_layout()
    plt.savefig(path)
    plt.close()



def add_rainy(weather, threshold=1.0):
    """Return a copy of `weather` with two new columns.

    `rainy`: 1 if `rain` is at least `threshold` mm that day, else 0.
    `rainy_tomorrow`: the next row's `rainy`; NaN in the last row.
    """
    result = weather.copy()

    result['rainy'] = (result['rain'] >= threshold).astype(float)
    result.loc[result['rain'].isna(), 'rainy'] = float('nan')
    result['rainy_tomorrow'] = result['rainy'].shift(-1)

    return result


def split_by_year(weather, last_train_year):
    """Rows up to and including last_train_year, and the rows after it."""
    
    train = weather[weather['year'] <= last_train_year]
    test = weather[weather['year'] > last_train_year]

    return train, test


def baselines(test):
    """Accuracy of two models without learning, on `test` (with `rainy` and `rainy_tomorrow`).

    Return a dict: "never": it never rains tomorrow; "same": tomorrow is like today.
    """
    test = test.dropna(subset=['rainy', 'rainy_tomorrow'])

    actual = test['rainy_tomorrow']
    never = [0] * len(test)
    same = test['rainy']

    return {'never': accuracy_score(actual, never),'same': accuracy_score(actual, same)}



def model_table(weather, features, depths):
    """Train decision trees that predict `rainy_tomorrow` from `features`, one per depth.

    Use the years from 1947 on; drop rows where a feature or `rainy_tomorrow` is missing;
    train on the years up to 2015 and test on the years after. Return a list of
    (depth, train accuracy, test accuracy), and the baselines on the test years.
    """

    weather = add_rainy(weather)
    train, test = split_by_year(weather, 2015)
    base = baselines(test)

    train = train.dropna(subset=features + ['rainy_tomorrow'])
    test = test.dropna(subset=features + ['rainy_tomorrow'])
    X_train = train[features]
    y_train = train['rainy_tomorrow']
    X_test = test[features]
    y_test = test['rainy_tomorrow']

    results = []

    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth,random_state=1)

        model.fit(X_train, y_train)

        train_accuracy = model.score(X_train, y_train)
        test_accuracy = model.score(X_test, y_test)

        results.append((depth, train_accuracy, test_accuracy))

    return results, base



if __name__ == "__main__":
    weather = load_weather(DATA_FILE)
    print(weather)
    # Print your answers here, e.g. print("1:", ...)
    weather = add_rainy(weather)

    rows, base = model_table(
        weather,
        ['rainy', 'humidity'],
        [1, None]
    )

    print("Baselines:", base)
    print("Decision trees:", rows)

