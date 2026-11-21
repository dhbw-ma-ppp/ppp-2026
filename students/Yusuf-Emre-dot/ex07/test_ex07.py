import math

import pandas as pd
import pytest
import numpy as np
from ex07 import (
    COLUMNS,
    DATA_FILE,
    SAMPLE_FILE,
    add_rainy,
    baselines,
    hot_days,
    load_weather,
    missing_per_year,
    model_table,
    monthly_rain,
    plot_hot_days,
    split_by_year,
)

# The real file isn't committed (see README.md), so tests that need it are skipped in CI.
needs_data = pytest.mark.skipif(not DATA_FILE.exists(), reason="mannheim.txt not found")

# ---------------------------------------------------------------- Part 1


def test_load_columns():
    weather = load_weather(SAMPLE_FILE)
    assert list(weather.columns) == list(COLUMNS.values()) + ["year", "month"]
    assert len(weather) == 9


def test_load_values():
    weather = load_weather(SAMPLE_FILE)
    assert weather["date"][0] == 17900101
    assert weather["rain"][0] == 0.7
    assert weather["max_temp"][2] == 31.8


def test_load_missing_is_nan():
    weather = load_weather(SAMPLE_FILE)
    assert weather["max_temp"].isna().sum() == 2
    assert weather["sunshine"].isna().sum() == 2
    assert (weather == -999).sum().sum() == 0


def test_load_year_and_month():
    weather = load_weather(SAMPLE_FILE)
    assert list(weather["year"]) == [1790, 1790, 2003, 2003, 2003, 2003, 2003, 2004, 2004]
    assert list(weather["month"]) == [1, 1, 8, 8, 8, 12, 12, 1, 1]


@needs_data
def test_load_real_file():
    weather = load_weather(DATA_FILE)
    assert len(weather) == 34334
    assert weather["date"].min() == 17810101
    assert weather["date"].max() == 20251231


def test_missing_per_year():
    weather = load_weather(SAMPLE_FILE)
    assert missing_per_year(weather, "max_temp").to_dict() == {1790: 2, 2003: 0, 2004: 0}
    assert missing_per_year(weather, "mean_temp").to_dict() == {1790: 0, 2003: 0, 2004: 0}


def test_hot_days():
    weather = load_weather(SAMPLE_FILE)
    assert hot_days(weather).to_dict() == {2003: 3, 2004: 0}


def test_hot_days_threshold_counts():
    weather = load_weather(SAMPLE_FILE)
    assert hot_days(weather, threshold=34.5).to_dict() == {2003: 2, 2004: 0}


# ---------------------------------------------------------------- Part 2


def test_monthly_rain():
    weather = pd.DataFrame(
        {
            "year": [2001, 2001, 2001, 2002, 2002],
            "month": [1, 1, 2, 1, 2],
            "rain": [1.0, 2.0, 5.0, 7.0, 0.0],
        }
    )
    assert monthly_rain(weather, 2001, 2002).to_dict() == {1: 5.0, 2: 2.5}  # Fehler?


def test_monthly_rain_only_the_given_years():
    weather = pd.DataFrame(
        {"year": [2000, 2001, 2002], "month": [1, 1, 1], "rain": [100.0, 4.0, 100.0]}
    )
    assert monthly_rain(weather, 2001, 2001).to_dict() == {1: 4.0}


def test_plot_hot_days(tmp_path):
    # tmp_path is an empty folder that pytest makes for this test
    path = tmp_path / "hot_days.png"
    plot_hot_days(load_weather(SAMPLE_FILE), path)
    assert path.exists()


def test_add_rainy():
    weather = pd.DataFrame({"rain": [0.0, 1.0, 0.9, 5.0]})
    result = add_rainy(weather)
    assert list(result["rainy"]) == [0, 1, 0, 1]
    assert list(result["rainy_tomorrow"][:3]) == [1, 0, 1]
    assert math.isnan(result["rainy_tomorrow"][3])


def test_add_rainy_leaves_the_original_alone():
    weather = pd.DataFrame({"rain": [0.0, 1.0]})
    add_rainy(weather)
    assert list(weather.columns) == ["rain"]


def test_split_by_year():
    weather = pd.DataFrame({"year": [2014, 2015, 2015, 2016, 2020]})
    train, test = split_by_year(weather, 2015)
    assert list(train["year"]) == [2014, 2015, 2015]
    assert list(test["year"]) == [2016, 2020]


def test_baselines():
    test = pd.DataFrame({"rainy": [0, 1, 1, 0], "rainy_tomorrow": [1, 1, 0, 0]})
    assert baselines(test) == {"never": 0.5, "same": 0.5}


@needs_data
def test_model_table():
    rows, base = model_table(load_weather(DATA_FILE), ["rainy", "humidity"], [1, None])
    assert [depth for depth, _, _ in rows] == [1, None]
    assert base["never"] == pytest.approx(0.717, abs=0.001)
    for _, train_score, test_score in rows:
        assert 0.5 < train_score <= 1
        assert 0.5 < test_score < 0.8

@needs_data
def test_split_doesnt_change_weather():
    weather = load_weather(DATA_FILE)
    cop = weather.copy()
    split_by_year(weather, 2000)
    assert weather.equals(cop)

@needs_data
def test_model_better_baseline():
    weather = load_weather(DATA_FILE)
    data = add_rainy(weather)
    label = data.columns.drop(["rainy_tomorrow"])
    print(label, data.columns, "lol")
    a, base = model_table(data, label, np.arange(1, len(label)))
    a.sort(key=lambda zwei: zwei[2])
    best = a[-1][2]
    assert best > base["never"] and best > base["same"]
