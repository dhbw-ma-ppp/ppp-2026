# Exercise 07: weather in Mannheim

|                |                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------- |
| **AI level**   | **1**: AI may **explain**, it may not write code for you (as in exercises 5 and 6). Inline completion stays off. |
| **Part 1**     | in class, Fri Nov 20, **no AI**. Anything you finish at home falls under level 1.                                |
| **Part 2**     | at home, AI level 1                                                                                              |
| **Due**        | Thu Nov 26, 17:00, as a pull request                                                                             |
| **Review due** | Tue Dec 1, 17:00 (author answers before the Wednesday session on Dec 2)                                          |

## Getting started

```
git checkout main
git pull
uv sync
git checkout -b ex07-<login>
```

`uv sync` installs pandas, matplotlib and scikit-learn if you haven't done so since Friday.

Copy the folder `exercises/ex07` to `students/<login>/ex07` and work only in the copy. Check
your work with `uv run pytest students/<login>/ex07` and see your answers with
`uv run python students/<login>/ex07/ex07.py`.

**`mannheim.txt` is 4.8 MB.** Copy it along with everything else, but git ignores your copy (see
`.gitignore`), so it doesn't end up in your PR 25 times over. Two tests need it; in CI, where it
isn't there, they're skipped.

## AI level 1: explanations, not code

Same rules as exercises 5 and 6: you may ask an AI to explain a concept, an error message, or how
a library function works in general ("what does `shift` do in pandas?"). You may not ask it for
code for this exercise, paste your code in for it to fix, or paste the task in. Under **AI use**
in your PR: the questions you asked, and in two or three sentences, in your own words, what you
took from the answers. If you didn't use AI, write "none".

The pandas documentation and `help(pd.read_csv)` are always fine.

## The data

`mannheim.txt` is the daily climate data of the weather station in Mannheim, as published by the
Deutscher Wetterdienst (DWD), Germany's national weather service: one line per day, from 1781 to
the end of 2025, unchanged. (Source: Deutscher Wetterdienst, Climate Data Center, daily
observations, station 5906; licence CC BY 4.0, see https://www.dwd.de/copyright.)

```
STATIONS_ID;MESS_DATUM;QN_3;  FX;  FM;QN_4; RSK;RSKF; SDK;SHK_TAG;  NM; VPM;  PM; TMK; UPM; TXK; TNK; TGK;eor
       5906;17900101;-999;-999;-999;    1;   0.7;   1;-999;   0;   7.3;  -999; 1017.80;    4.2;-999;   -999;   -999;-999;eor
```

What you need to know:

- Fields are separated by `;`, and padded with spaces, in the header too.
- **`-999` means "not measured".** It isn't a temperature of -999 °C.
- `MESS_DATUM` is the date as one number, `YYYYMMDD`.
- The columns we use, and the names we give them, are in `COLUMNS` in `ex07.py`:

| DWD          | ours        | meaning                                                  |
| ------------ | ----------- | -------------------------------------------------------- |
| `MESS_DATUM` | `date`      | the day, e.g. `19470101`                                 |
| `TMK`        | `mean_temp` | mean temperature of the day, °C                          |
| `TXK`        | `max_temp`  | highest temperature of the day, °C                       |
| `TNK`        | `min_temp`  | lowest temperature of the day, °C                        |
| `RSK`        | `rain`      | rain (and snow, melted), mm                              |
| `SDK`        | `sunshine`  | hours of sunshine                                        |
| `NM`         | `clouds`    | cloud cover, in eighths of the sky (0 clear, 8 overcast) |
| `UPM`        | `humidity`  | relative humidity, %                                     |
| `PM`         | `pressure`  | air pressure, hPa                                        |

`sample.txt` has the header and nine lines of `mannheim.txt`, for the tests.

## Part 1 (in class, no AI)

1. `load_weather(path)`: read the file into a DataFrame. Keep only the columns in `COLUMNS`,
   renamed to our names, in that order; every `-999` becomes `NaN`. Then add two columns, `year`
   and `month`, as ints, worked out from `date`.

   Hints: `pd.read_csv` has parameters for the separator, for spaces after the separator, and for
   values that mean "missing" (look at `help(pd.read_csv)`). Selecting several columns is
   `table[list_of_names]`; `rename(columns=a_dict)` renames. For year and month, you don't need
   any date functions: `19470315` is a number.

   Answer 1: how many days does the file have, and from which year to which?

2. `missing_per_year(weather, column)`: a Series with one entry per year in `weather`: on how many
   days of that year `column` is missing.

   Answer 2: in which years is `max_temp` missing on (almost) every day? Look at `mean_temp` for
   the same years. What does that tell you about the station's history?

3. `hot_days(weather, threshold=30.0)`: a Series with one entry per year: on how many days
   `max_temp` was `threshold` or more. A year without any such day has 0; a year without **any**
   known `max_temp` isn't in the result at all (it would be wrong to say "0 hot days" for a year
   nobody measured).

   Answer 3: which year had the most hot days (30 °C or more), and how many? (If several years
   tie, give all of them.)

   Answer 4: the average number of hot days per year in 1951–1980, and in 1996–2025.
   (`series.loc[1951:1980]` selects by label, both ends included.)

## Part 2 (at home, AI level 1)

1. `monthly_rain(weather, first_year, last_year)`: for each month (1 to 12), the **average total
   rain** of that month over the years `first_year` to `last_year`. That's two steps: first the
   total of each month of each year, then the average of those totals per month.

   Answer 5: over 1947–2025, the wettest and the driest month, with their averages.

2. `plot_hot_days(weather, path)`: save a bar chart of `hot_days(weather)` (one bar per year) to
   `path`, with labelled axes and a title. In `ex07.py`, save it as `hot_days.png` next to
   `ex07.py`, and **commit the picture**.

   Look at your chart. What do you see? Which years don't have a bar, and why? Write two or three
   sentences in your PR.

3. **Will it rain tomorrow?** Wednesday's ideas and Friday's decision tree, on the weather.
   - `add_rainy(weather, threshold=1.0)`: a copy of `weather` with two new columns. `rainy` is
     1 on days with at least `threshold` mm of rain (1 mm is a common definition of a rain
     day), else 0. `rainy_tomorrow` is the **next row's** `rainy`; in the last row there is no next day, so
     it's `NaN`. The table has no gaps from 1947 on, so the next row is the next day.
   - `split_by_year(weather, last_train_year)`: the rows up to and including that year, and the
     rows after it.
   - `baselines(test)`: the accuracy of two models that don't learn anything, on `test`, as a dict:
     `"never"`: it never rains tomorrow; `"same"`: tomorrow is like today.
   - `model_table(weather, features, depths)`: see the docstring. For each depth in `depths`,
     train a `DecisionTreeClassifier(max_depth=depth, random_state=1)` on the years 1947–2015 and
     test it on 2016–2025.

   Choose your features from the columns (and `month`, `rainy`). Try a few combinations and depths,
   including `None`.

   Answer 6: the two baselines; and a table of depth, train accuracy and test accuracy for your
   best choice of features.

   **In your PR, in a few sentences of your own:** would you use your model to decide whether to
   take an umbrella? Compare with the baselines. And: why do we test on the **last** ten years,
   instead of 15% of the days picked at random, as on Friday?

4. **Add at least two more tests of your own** at the end of `test_ex07.py`. Write each test case
   down first: which input, which expected result, and which case it covers. Small DataFrames made
   in the test (as in `test_monthly_rain`) are easier to check than the real file.

## Optional

- A **heatmap**: the mean temperature of every month of every year from 1947 on, as a grid (years
  as rows, months as columns) with `imshow`. Hint: after grouping by two columns, `unstack()`
  turns the second one into columns.
- A line plot of the yearly mean temperature, with a **10-year rolling mean** on top
  (`rolling(10)`).
- Hot days with a different threshold (35 °C?), or frost days (`min_temp` below 0).

## Your pull request

- Title: `ex07 <login>`
- Paste the output of `uv run python students/<login>/ex07/ex07.py` under **Result**, in a code
  block.
- `hot_days.png` committed; your sentences about the chart and about the model.
- Under **AI use**: your questions and what you took from the answers (see above).
- CI must be green: all tests pass, ruff is happy.
