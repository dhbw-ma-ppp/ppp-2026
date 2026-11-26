"""The Titanic data as an interactive dashboard (Streamlit).

Start it from the repository folder with:
    uv run streamlit run lectures/web/titanic_streamlit.py
It opens in the browser (http://localhost:8501).

Streamlit runs this whole script from top to bottom again every time someone moves a slider
or clicks something. Watch the terminal.
"""

import pickle

import streamlit as st

from titanic_features import MODEL_FILE, encode_one, load_passengers

print("script runs")


@st.cache_data  # load once, not on every rerun
def get_passengers():
    print("loading the CSV")
    return load_passengers()


@st.cache_resource
def get_model():
    with open(MODEL_FILE, "rb") as file:
        return pickle.load(file)


passengers = get_passengers()
model = get_model()

st.title("Titanic")

st.sidebar.header("Filter")
classes = st.sidebar.multiselect("Class", [1, 2, 3], default=[1, 2, 3])
youngest, oldest = st.sidebar.slider("Age", 0, 80, (0, 80))

selected = passengers.query("Pclass in @classes and @youngest <= Age <= @oldest")

left, right = st.columns(2)
left.metric("Passengers", len(selected))
if len(selected) > 0:
    right.metric("Survived", f"{selected['Survived'].mean():.0%}")

st.subheader("Survival rate by class and sex")
st.bar_chart(selected.pivot_table("Survived", index="Pclass", columns="Sex"))

st.subheader("Would you have survived?")
sex = st.radio("Sex", ["female", "male"], horizontal=True)
pclass = st.selectbox("Class", [1, 2, 3], index=2)
age = st.number_input("Age", min_value=0, max_value=100, value=25)
survives = model.predict(encode_one(sex, pclass, age))[0]
st.write("**survives**" if survives else "**does not survive**")
