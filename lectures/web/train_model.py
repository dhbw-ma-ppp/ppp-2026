"""Train the Titanic decision tree once and save it with pickle.

Run:  uv run python lectures/web/train_model.py
The apps only load the saved model; they never train.
"""

import pickle

from sklearn.tree import DecisionTreeClassifier

from titanic_features import MODEL_FILE, load_passengers, encode

passengers = load_passengers()
features = encode(passengers["Sex"], passengers["Pclass"], passengers["Age"])
model = DecisionTreeClassifier(max_depth=3, random_state=1)
model.fit(features, passengers["Survived"])
print("accuracy on the training data:", round(model.score(features, passengers["Survived"]), 3))

with open(MODEL_FILE, "wb") as file:
    pickle.dump(model, file)
print("saved to", MODEL_FILE)
