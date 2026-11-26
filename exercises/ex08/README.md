# Exercise 08: review an AI's pull request

|  |  |
|---|---|
| **AI level** | **0**: no AI, by hand. You review the AI's work yourself; that's the point of the exercise. Inline completion off. The FastAPI and pandas documentation are always fine. |
| **Handed out** | Fri Nov 27, in class |
| **Due** | Thu Dec 3, 17:00, as a pull request |
| **Review** | none: this exercise *is* a review, and it counts as your review for the week |
| **Discussed** | Fri Dec 4, in the morning, before the project work starts |

Someone on your team asked an AI coding assistant for a small web service on the Mannheim
weather data you know from Exercise 7. The code in `weather-service/` is what came back, and the
author wants to merge it. Your job: review it as you would review a colleague's PR. Does it do
what was asked, and does it get the data right?

The code is **unedited**. Only the packaging files (`pyproject.toml`, `uv.lock`) were left out,
because our repository already has the libraries. Nothing was planted: every problem you find
is one the AI made itself. The code passes all of its own tests.

## The task the AI was given

This is the complete prompt:

> Build a small web service with FastAPI for the weather data in mannheim.txt. It's the DWD
> daily climate data for station 5906 (Mannheim), semicolon-separated. Columns we care about:
> MESS_DATUM (date as YYYYMMDD), TMK (daily mean temperature, °C), TXK (daily max temperature),
> TNK (daily min temperature), RSK (precipitation, mm), SDK (sunshine, hours).
>
> Endpoints:
> - GET /day/{date} with date as YYYY-MM-DD: the weather on that day
> - GET /year/{year}: summary for a year: mean temperature, total precipitation, number of hot
>   days (max temperature at least 30 °C), and the sunniest day
> - GET /compare?year1=...&year2=...: the same summary for two years side by side, plus the
>   differences
> - GET /records: hottest day, coldest day and wettest day ever
>
> Use pandas for the data. Write tests with pytest and FastAPI's TestClient. Use uv for the
> project (Python 3.14). Keep it simple, this is for a university course project.

## Getting started

```
git checkout main
git pull
uv sync
git checkout -b ex08-<login>
```

Copy the folder `exercises/ex08` to `students/<login>/ex08`, and copy the data file next to the
AI's code:

```
cp exercises/ex07/mannheim.txt students/<login>/ex08/weather-service/
```

Git ignores that copy, as in Exercise 7. (When you run the tests, `conftest.py` copies it for
you if it's missing, so CI works without it.)

Run the tests, the AI's and yours:

```
uv run pytest students/<login>/ex08
```

Start the service and try it in the browser (http://127.0.0.1:8000/docs):

```
cd students/<login>/ex08/weather-service
uv run fastapi dev weather_service/app.py
```

## What to do

1. **Read the code** (`weather_service/app.py`) and the tests (`tests/test_app.py`). Run the
   service and send it requests: dates and years you know something about from Exercise 7.
2. **Write tests that break it** in `tests/test_review.py`. A test that shows a problem fails on
   the AI's code: mark it with `@pytest.mark.xfail(strict=True, reason="...")`, so CI stays green
   and the problem stays visible. The file has an example of each kind.
3. **Write the review** in `REVIEW.md`, along these questions:
   - Which input gives a wrong answer or an error?
   - Where is the same thing done twice?
   - What did it assume that the task doesn't say?
   - Which of its own tests could never fail?
   - Would you merge it?
4. **Optional:** fix what you found. Your xfail tests then pass, `strict=True` makes pytest
   report that, and you remove the marker.

Your PR contains `REVIEW.md` and your tests (and your fixes, if you made any). It counts as done
if `REVIEW.md` answers every question, and `tests/test_review.py` has at least **two tests that
fail on the AI's code**, each for a different problem.


## Data

The data is from the Deutscher Wetterdienst (DWD), Climate Data Center, licensed under
CC BY 4.0, as in Exercise 7.
