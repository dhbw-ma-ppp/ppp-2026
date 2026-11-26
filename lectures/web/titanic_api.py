"""The Titanic passengers as a web service (FastAPI).

Start it from the repository folder with:
    uv run fastapi dev lectures/web/titanic_api.py
then open http://127.0.0.1:8000/docs in the browser. `dev` restarts the server whenever you
save this file. Stop it with Ctrl+C.
"""

import pickle
from typing import Literal

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from titanic_features import MODEL_FILE, encode_one, load_passengers

# Runs once, when the server starts, not for every request.
passengers = load_passengers()
with open(MODEL_FILE, "rb") as file:
    model = pickle.load(file)  # remember: only ever load pickles you made yourself

app = FastAPI(title="Titanic")


# What the endpoints answer. A return type that is a Pydantic class tells FastAPI the shape of
# the answer: /docs shows it, and FastAPI checks every answer against it before sending it.


class Home(BaseModel):
    passenger_count: int
    examples: list[str]


class PassengerFeatures(BaseModel):
    """What the model needs to know about a passenger: its three features, nothing else."""

    sex: Literal["female", "male"]
    pclass: int = Field(ge=1, le=3)
    age: float | None = Field(default=None, ge=0, le=100)


class PassengerInfo(PassengerFeatures):
    """A passenger from the data: the features, plus these."""

    id: int
    name: str
    survived: bool


class Survival(BaseModel):
    sex: str | None
    pclass: int | None
    passenger_count: int
    survival_rate: float


class Prediction(BaseModel):
    features: PassengerFeatures
    survives: bool


@app.get("/")
def home() -> Home:
    return Home(passenger_count=len(passengers), examples=["/passengers/1", "/survival", "/docs"])


@app.get("/passengers/{passenger_id}")
def get_passenger(passenger_id: int) -> PassengerInfo:
    if passenger_id not in passengers.index:
        raise HTTPException(status_code=404, detail=f"no passenger with id {passenger_id}")
    row = passengers.loc[passenger_id]
    return PassengerInfo(
        id=passenger_id,
        name=row["Name"],
        sex=row["Sex"],
        pclass=int(row["Pclass"]),
        age=None if pd.isna(row["Age"]) else float(row["Age"]),
        survived=bool(row["Survived"]),
    )


@app.get("/survival")
def survival(sex: str | None = None, pclass: int | None = None) -> Survival:
    selected = passengers
    if sex is not None:
        selected = selected.query("Sex == @sex")  # @sex: the Python variable sex
    if pclass is not None:
        selected = selected.query("Pclass == @pclass")
    if selected.empty:
        raise HTTPException(status_code=404, detail="no passengers match")
    return Survival(
        sex=sex,
        pclass=pclass,
        passenger_count=len(selected),
        survival_rate=round(float(selected["Survived"].mean()), 3),
    )


@app.post("/predict")
def predict(features: PassengerFeatures) -> Prediction:
    encoded = encode_one(features.sex, features.pclass, features.age)
    return Prediction(features=features, survives=bool(model.predict(encoded)[0]))
