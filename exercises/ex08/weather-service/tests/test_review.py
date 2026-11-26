"""Your tests for the AI's weather service. The AI's own tests are in test_app.py.

Two kinds of tests belong here:

1. A test that checks a *value*, not just that a key exists. It passes if the code is right.
2. A test that shows a problem: it fails on the AI's code. Mark it with
   @pytest.mark.xfail(strict=True, reason="..."), so CI stays green and everyone can see what is
   broken. If you fix the code, the test passes, strict=True makes pytest complain about that,
   and you remove the marker.
"""

import pytest
from fastapi.testclient import TestClient
from weather_service.app import app

client = TestClient(app)


def test_day_values_match_the_file():
    # 2025-12-31 in mannheim.txt: TMK -2.1, TXK 2.4, TNK -7.6, RSK 0.0, SDK 0.1
    data = client.get("/day/2025-12-31").json()
    assert data["mean_temperature"] == -2.1
    assert data["max_temperature"] == 2.4
    assert data["min_temperature"] == -7.6
    assert data["precipitation"] == 0.0
    assert data["sunshine"] == 0.1


@pytest.mark.xfail(strict=True, reason="example of the pattern: replace it with a real problem")
def test_example_of_a_known_problem():
    assert client.get("/").json()["message"] == "something the app does not say"
