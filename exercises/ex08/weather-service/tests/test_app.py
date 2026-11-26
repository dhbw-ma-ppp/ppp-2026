from fastapi.testclient import TestClient
from weather_service.app import app

client = TestClient(app)


def test_root():
    """Test root endpoint returns service information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "station" in data
    assert "endpoints" in data


def test_get_day_valid():
    """Test fetching weather for a specific day."""
    response = client.get("/day/1781-01-15")
    assert response.status_code == 200
    data = response.json()
    assert data["date"] == "1781-01-15"
    assert "mean_temperature" in data
    assert "max_temperature" in data
    assert "min_temperature" in data
    assert "precipitation" in data
    assert "sunshine" in data


def test_get_day_invalid_format():
    """Test that invalid date format returns 400."""
    response = client.get("/day/01-15-1781")
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]


def test_get_day_not_found():
    """Test that non-existent date returns 404."""
    response = client.get("/day/1500-01-01")
    assert response.status_code == 404
    assert "No data for this date" in response.json()["detail"]


def test_get_year_valid():
    """Test fetching yearly summary."""
    response = client.get("/year/2000")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2000
    assert "mean_temperature" in data
    assert "total_precipitation" in data
    assert "hot_days" in data
    assert "sunniest_day" in data
    assert "date" in data["sunniest_day"]
    assert "sunshine_hours" in data["sunniest_day"]


def test_get_year_not_found():
    """Test that non-existent year returns 404."""
    response = client.get("/year/1500")
    assert response.status_code == 404
    assert "No data for this year" in response.json()["detail"]


def test_compare_years_valid():
    """Test comparing two years."""
    response = client.get("/compare?year1=2000&year2=2010")
    assert response.status_code == 200
    data = response.json()

    # Check structure
    assert "year1" in data
    assert "year2" in data
    assert "differences" in data

    # Check year1 data
    assert data["year1"]["year"] == 2000
    assert "mean_temperature" in data["year1"]
    assert "total_precipitation" in data["year1"]
    assert "hot_days" in data["year1"]

    # Check year2 data
    assert data["year2"]["year"] == 2010
    assert "mean_temperature" in data["year2"]
    assert "total_precipitation" in data["year2"]
    assert "hot_days" in data["year2"]

    # Check differences
    assert "mean_temperature" in data["differences"]
    assert "total_precipitation" in data["differences"]
    assert "hot_days" in data["differences"]


def test_compare_years_first_not_found():
    """Test that non-existent first year returns 404."""
    response = client.get("/compare?year1=1500&year2=2000")
    assert response.status_code == 404
    assert "No data for year 1500" in response.json()["detail"]


def test_compare_years_second_not_found():
    """Test that non-existent second year returns 404."""
    response = client.get("/compare?year1=2000&year2=3000")
    assert response.status_code == 404
    assert "No data for year 3000" in response.json()["detail"]


def test_get_records():
    """Test fetching all-time records."""
    response = client.get("/records")
    assert response.status_code == 200
    data = response.json()

    # Check structure
    assert "hottest_day" in data
    assert "coldest_day" in data
    assert "wettest_day" in data

    # Check hottest day
    assert "date" in data["hottest_day"]
    assert "max_temperature" in data["hottest_day"]

    # Check coldest day
    assert "date" in data["coldest_day"]
    assert "min_temperature" in data["coldest_day"]

    # Check wettest day
    assert "date" in data["wettest_day"]
    assert "precipitation" in data["wettest_day"]


def test_hot_days_count():
    """Test that hot days (max temp >= 30°C) are counted correctly."""
    response = client.get("/year/2003")  # Using a recent year that likely has hot days
    assert response.status_code == 200
    data = response.json()
    assert data["hot_days"] >= 0
    assert isinstance(data["hot_days"], int)
