# Mannheim Weather Service

A FastAPI web service for querying DWD (Deutscher Wetterdienst) daily climate data from station 5906 (Mannheim).

## Setup

This project uses uv with Python 3.14. Install dependencies:

```bash
uv sync
```

## Running the Service

Start the development server:

```bash
uv run uvicorn weather_service.app:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

## Endpoints

### `GET /`
Root endpoint with service information.

### `GET /day/{date}`
Get weather data for a specific day.

**Parameters:**
- `date`: Date in YYYY-MM-DD format (e.g., `2020-07-15`)

**Example:**
```bash
curl http://localhost:8000/day/2020-07-15
```

**Response:**
```json
{
  "date": "2020-07-15",
  "mean_temperature": 20.5,
  "max_temperature": 28.3,
  "min_temperature": 14.2,
  "precipitation": 0.0,
  "sunshine": 12.5
}
```

### `GET /year/{year}`
Get yearly summary statistics.

**Parameters:**
- `year`: Four-digit year (e.g., `2020`)

**Example:**
```bash
curl http://localhost:8000/year/2020
```

**Response:**
```json
{
  "year": 2020,
  "mean_temperature": 11.4,
  "total_precipitation": 625.8,
  "hot_days": 15,
  "sunniest_day": {
    "date": "2020-05-20",
    "sunshine_hours": 15.2
  }
}
```

### `GET /compare`
Compare weather statistics between two years.

**Query Parameters:**
- `year1`: First year to compare
- `year2`: Second year to compare

**Example:**
```bash
curl "http://localhost:8000/compare?year1=2000&year2=2010"
```

**Response:**
```json
{
  "year1": {
    "year": 2000,
    "mean_temperature": 11.0,
    "total_precipitation": 580.0,
    "hot_days": 10,
    "sunniest_day": {...}
  },
  "year2": {
    "year": 2010,
    "mean_temperature": 10.5,
    "total_precipitation": 620.0,
    "hot_days": 12,
    "sunniest_day": {...}
  },
  "differences": {
    "mean_temperature": -0.5,
    "total_precipitation": 40.0,
    "hot_days": 2
  }
}
```

### `GET /records`
Get all-time weather records.

**Example:**
```bash
curl http://localhost:8000/records
```

**Response:**
```json
{
  "hottest_day": {
    "date": "2003-08-13",
    "max_temperature": 39.8
  },
  "coldest_day": {
    "date": "1929-02-11",
    "min_temperature": -22.0
  },
  "wettest_day": {
    "date": "2016-05-29",
    "precipitation": 71.3
  }
}
```

## Running Tests

Run the test suite with pytest:

```bash
uv run pytest
```

For verbose output:

```bash
uv run pytest -v
```

## Data

The service uses DWD daily climate data from station 5906 (Mannheim). Key columns:
- **MESS_DATUM**: Date (YYYYMMDD format)
- **TMK**: Daily mean temperature (°C)
- **TXK**: Daily maximum temperature (°C)
- **TNK**: Daily minimum temperature (°C)
- **RSK**: Precipitation (mm)
- **SDK**: Sunshine duration (hours)

Missing values are represented as `-999` in the source data and handled as `null` in API responses.

## Project Structure

```
weather-service/
├── weather_service/
│   ├── __init__.py
│   └── app.py          # FastAPI application
├── tests/
│   ├── __init__.py
│   └── test_app.py     # Test suite
├── mannheim.txt        # DWD weather data
├── pyproject.toml      # Project configuration
└── README.md
```
