"""The Titanic model behind an HTML form (Flask).

Start it from the repository folder with:
    uv run flask --app lectures/web/titanic_flask.py run --debug
then open http://127.0.0.1:5000 in the browser.
"""

import pickle

from flask import Flask, render_template_string, request

from titanic_features import MODEL_FILE, encode_one, load_passengers

passengers = load_passengers()
with open(MODEL_FILE, "rb") as file:
    model = pickle.load(file)

app = Flask(__name__)

# A Jinja template: HTML with {{ value }} and {% if %} ... {% endif %} filled in by Flask.
PAGE = """
<!doctype html>
<title>Titanic</title>
<h1>Would you have survived?</h1>
<form method="post">
  <label>Sex
    <select name="sex">
      <option value="female">female</option>
      <option value="male">male</option>
    </select>
  </label>
  <label>Class <input name="pclass" type="number" min="1" max="3" value="3"></label>
  <label>Age <input name="age" type="number" min="0" max="100"></label>
  <button>Predict</button>
</form>
{% if result is not none %}
  <p>A {{ age or "?" }}-year-old {{ sex }} passenger in class {{ pclass }}:
     <strong>{{ "survives" if result else "does not survive" }}</strong>.</p>
{% endif %}
<h2>Survival rate by class</h2>
{{ table | safe }}
"""


@app.route("/", methods=["GET", "POST"])
def home():
    table = passengers.pivot_table("Survived", index="Pclass", columns="Sex").round(2).to_html()
    if request.method == "GET":
        return render_template_string(PAGE, result=None, table=table)

    sex = request.form["sex"]
    pclass = int(request.form["pclass"])
    age = float(request.form["age"]) if request.form["age"] else None
    result = bool(model.predict(encode_one(sex, pclass, age))[0])
    return render_template_string(PAGE, result=result, sex=sex, pclass=pclass, age=age, table=table)
