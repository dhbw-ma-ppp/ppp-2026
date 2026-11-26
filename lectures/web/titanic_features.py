"""The features the Titanic model uses, in one place.

Training (`train_model.py`) and all three apps import this, so the model always gets its
input in the same form it was trained on (the features from the Nov 20 lecture).
"""

from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).parent.parent / "titanic.csv"
MODEL_FILE = Path(__file__).parent / "model.pickle"


def load_passengers() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE, index_col="PassengerId")


def encode(sex: pd.Series, pclass: pd.Series, age: pd.Series) -> pd.DataFrame:
    """Turn sex, class and age into the numbers the tree was trained on."""
    return pd.DataFrame(
        {
            "female": (sex == "female").astype(int),
            "pclass": pclass,
            "age": age.fillna(-1),  # -1: age unknown
        }
    )


def encode_one(sex: str, pclass: int, age: float | None) -> pd.DataFrame:
    """`encode` for a single passenger, e.g. from a web form."""
    return encode(pd.Series([sex]), pd.Series([pclass]), pd.Series([age], dtype=float))
