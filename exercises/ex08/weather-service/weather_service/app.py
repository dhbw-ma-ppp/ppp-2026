from fastapi import FastAPI, HTTPException
from pathlib import Path
import pandas as pd
from datetime import datetime

app = FastAPI(title="Mannheim Weather Service")

# Load data
DATA_PATH = Path(__file__).parent.parent / "mannheim.txt"
df = pd.read_csv(
    DATA_PATH,
    sep=";",
    skipinitialspace=True,
    na_values=[-999],
)

# Parse dates and extract year
df["date"] = pd.to_datetime(df["MESS_DATUM"], format="%Y%m%d")
df["year"] = df["date"].dt.year


@app.get("/")
def root():
    return {
        "message": "Mannheim Weather Service",
        "station": "DWD Station 5906 (Mannheim)",
        "endpoints": ["/day/{date}", "/year/{year}", "/compare", "/records"],
    }


@app.get("/day/{date}")
def get_day(date: str):
    """Get weather data for a specific day (YYYY-MM-DD)."""
    try:
        query_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    day_data = df[df["date"] == query_date]

    if day_data.empty:
        raise HTTPException(status_code=404, detail="No data for this date")

    row = day_data.iloc[0]

    return {
        "date": date,
        "mean_temperature": row["TMK"] if pd.notna(row["TMK"]) else None,
        "max_temperature": row["TXK"] if pd.notna(row["TXK"]) else None,
        "min_temperature": row["TNK"] if pd.notna(row["TNK"]) else None,
        "precipitation": row["RSK"] if pd.notna(row["RSK"]) else None,
        "sunshine": row["SDK"] if pd.notna(row["SDK"]) else None,
    }


@app.get("/year/{year}")
def get_year(year: int):
    """Get summary statistics for a specific year."""
    year_data = df[df["year"] == year]

    if year_data.empty:
        raise HTTPException(status_code=404, detail="No data for this year")

    # Calculate statistics
    mean_temp = year_data["TMK"].mean()
    total_precip = year_data["RSK"].sum()
    hot_days = (year_data["TXK"] >= 30).sum()

    # Find sunniest day
    sunniest = year_data.loc[year_data["SDK"].idxmax()]

    return {
        "year": year,
        "mean_temperature": round(mean_temp, 2) if pd.notna(mean_temp) else None,
        "total_precipitation": round(total_precip, 2) if pd.notna(total_precip) else None,
        "hot_days": int(hot_days),
        "sunniest_day": {
            "date": sunniest["date"].strftime("%Y-%m-%d"),
            "sunshine_hours": sunniest["SDK"] if pd.notna(sunniest["SDK"]) else None,
        },
    }


@app.get("/compare")
def compare_years(year1: int, year2: int):
    """Compare weather statistics between two years."""
    year1_data = df[df["year"] == year1]
    year2_data = df[df["year"] == year2]

    if year1_data.empty:
        raise HTTPException(status_code=404, detail=f"No data for year {year1}")
    if year2_data.empty:
        raise HTTPException(status_code=404, detail=f"No data for year {year2}")

    # Calculate statistics for both years
    def calc_stats(data):
        mean_temp = data["TMK"].mean()
        total_precip = data["RSK"].sum()
        hot_days = (data["TXK"] >= 30).sum()
        sunniest = data.loc[data["SDK"].idxmax()]

        return {
            "mean_temperature": round(mean_temp, 2) if pd.notna(mean_temp) else None,
            "total_precipitation": round(total_precip, 2) if pd.notna(total_precip) else None,
            "hot_days": int(hot_days),
            "sunniest_day": {
                "date": sunniest["date"].strftime("%Y-%m-%d"),
                "sunshine_hours": sunniest["SDK"] if pd.notna(sunniest["SDK"]) else None,
            },
        }

    stats1 = calc_stats(year1_data)
    stats2 = calc_stats(year2_data)

    # Calculate differences
    diff_temp = None
    diff_precip = None
    if stats1["mean_temperature"] is not None and stats2["mean_temperature"] is not None:
        diff_temp = round(stats2["mean_temperature"] - stats1["mean_temperature"], 2)
    if stats1["total_precipitation"] is not None and stats2["total_precipitation"] is not None:
        diff_precip = round(stats2["total_precipitation"] - stats1["total_precipitation"], 2)

    return {
        "year1": {
            "year": year1,
            **stats1,
        },
        "year2": {
            "year": year2,
            **stats2,
        },
        "differences": {
            "mean_temperature": diff_temp,
            "total_precipitation": diff_precip,
            "hot_days": stats2["hot_days"] - stats1["hot_days"],
        },
    }


@app.get("/records")
def get_records():
    """Get all-time weather records."""
    # Hottest day
    hottest = df.loc[df["TXK"].idxmax()]

    # Coldest day
    coldest = df.loc[df["TNK"].idxmin()]

    # Wettest day
    wettest = df.loc[df["RSK"].idxmax()]

    return {
        "hottest_day": {
            "date": hottest["date"].strftime("%Y-%m-%d"),
            "max_temperature": hottest["TXK"] if pd.notna(hottest["TXK"]) else None,
        },
        "coldest_day": {
            "date": coldest["date"].strftime("%Y-%m-%d"),
            "min_temperature": coldest["TNK"] if pd.notna(coldest["TNK"]) else None,
        },
        "wettest_day": {
            "date": wettest["date"].strftime("%Y-%m-%d"),
            "precipitation": wettest["RSK"] if pd.notna(wettest["RSK"]) else None,
        },
    }
