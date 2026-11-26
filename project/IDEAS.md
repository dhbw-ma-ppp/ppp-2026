# Project ideas

Your team (3–4 people) builds a small web app (FastAPI, Flask or Streamlit) on a real dataset.
Pandas does the data work; one simple scikit-learn model is welcome but not required. Below are
suggestions. You can take one as it is, change it, or bring your own idea (see the checklist at
the end). Dates and rules are in [README.md](README.md).

Whatever you pick, every team member must be able to explain and change any part of the code,
and your team should be able to say **what your data reflects**: who collected it, what's missing,
and what your app can't tell you.

Each idea lists a possible split into work packages. These are suggestions; make your own in your
team's GitHub Project.

## Close to home (German open data)

### 1. How unusual is today? (weather)

- **Data:** DWD daily climate data, any station (you know the format from Ex 7).
  `opendata.dwd.de`, CC BY 4.0.
- **App:** pick a station and a date; the app says how today's temperature and rain compare with
  the same date in all earlier years ("warmest 24 Nov since 1953"). A chart of the year so far
  against the long-term range.
- **Model (optional):** rain tomorrow, against the baselines from Ex 7; or compare stations.
- **Work packages:** download and parse several stations; statistics per day of year; API
  endpoints; chart endpoint or HTML page; model.
- **Watch out:** stations move and change instruments; old years have gaps.

### 2. When is electricity green? (energy)

- **Data:** SMARD (Bundesnetzagentur), hourly generation by source, consumption and day-ahead
  prices. `smard.de` → Download centre, CC BY 4.0, credit "Bundesnetzagentur | SMARD.de".
- **App:** "When should I run my washing machine?" Share of renewables and price by hour of day,
  weekday and season; a page for any chosen week.
- **Model (optional):** predict tomorrow's renewable share or price from hour, weekday, month
  (and DWD wind/sun data, if you dare to join two sources).
- **Work packages:** loading and cleaning (German number format, time change in March and
  October!); aggregations; API; charts; model.
- **Watch out:** daylight saving time gives days with 23 and 25 hours.

### 3. Bikes and weather (mobility)

- **Data:** automatic bike counters, daily or hourly counts per counter. Many cities and regions
  publish them, e.g. MobiData BW for all of Baden-Württemberg (`mobidata-bw.de`, dataset
  "Fahrradzähler", with a historical API; the CSV files there only cover the last 7 days),
  Munich (`opendata.muenchen.de`) or Bonn (`opendata.bonn.de`). Check the licence of the one
  you pick.
- **App:** counts per counter and weekday; comparing counters or cities; "how many cyclists
  would you expect tomorrow?" for a chosen temperature and rain.
- **Model:** regression of daily counts on temperature, rain, weekday, holidays.
- **Work packages:** bike data; weather data (DWD); joining on date; model; API and pages.
- **Watch out:** counters fail (zeros that aren't real), construction sites, school holidays.

### 4. Cheapest time to fill up (fuel prices)

- **Data:** Tankerkönig, every price change at every German petrol station since June 2014
  (from the Markttransparenzstelle), `creativecommons.tankerkoenig.de`, CC BY-NC-SA 4.0. A free
  API key gives current prices as well.
- **App:** cheapest hour and weekday to fill up, for a station or an area; how far prices differ
  between nearby stations; brands compared; prices over the years.
- **Model (optional):** predict a station's price in the next hours from the time of day,
  weekday and its recent prices.
- **Work packages:** stations data; price data; turning price changes into prices per hour;
  statistics; API; charts.
- **Watch out:** the data lists price *changes*, not prices at fixed times, and there are a lot
  of them (several per station and day). ShareAlike: whatever you publish from the data goes
  under the same licence.

### 5. Election map without a map (politics)

- **Data:** Bundestag election 2025 results per constituency and the structural data per
  constituency (Strukturdaten: age, income, unemployment, ...), both from
  `bundeswahlleiterin.de`, Datenlizenz Deutschland (check the exact terms).
- **App:** look up a constituency; compare it with Germany and with "similar" constituencies;
  which structural figures go together with which party's share.
- **Model (optional):** linear regression of a party's share on a few structural figures, and
  an honest page about what it does *not* show (correlation, not why people vote).
- **Work packages:** results file (multi-row headers, first and second votes); structural data;
  joining via constituency number; similarity search; API.
- **Watch out:** constituencies changed for 2025, so 2021 numbers don't line up directly.

### 6. Air in Mannheim (environment)

- **Data:** Umweltbundesamt air quality data (NO₂, PM10, ozone) per station, via their API or
  downloads (`umweltbundesamt.de`, Datenlizenz Deutschland, check terms). Optionally DWD wind.
- **App:** values for a station over time, limit exceedances per year, weekday vs. weekend
  ("is it traffic?"), effect of wind.
- **Model (optional):** predict tomorrow's PM10 class from today's values and the weather.
- **Work packages:** getting the data; cleaning; statistics; charts; model.
- **Watch out:** measurements are hourly and stations measure different things.

## Classic datasets with a twist

### 7. Movie recommender

- **Data:** MovieLens "small" (100k ratings, ~9k movies), `grouplens.org/datasets/movielens`.
  Free for research and teaching; the licence doesn't allow redistributing the files.
- **App:** search movies; "people who liked this also liked"; enter a few ratings and get
  recommendations.
- **Model:** some measure of which movies are rated alike.
- **Work packages:** loading and genre parsing; statistics; similarity; API; front end.
- **Watch out:** a movie with one 5-star rating is not the best movie.

### 8. Is this food healthy? (Open Food Facts)

- **Data:** Open Food Facts product database, `world.openfoodfacts.org/data`, ODbL. The full CSV
  is several GB.
- **App:** look up a product by barcode or name; compare products in a category; the nutrients
  that matter most for the Nutri-Score.
- **Model:** predict the Nutri-Score grade (A–E) from nutrients, compare with the real one, and
  explain where it's wrong.
- **Work packages:** getting the dump down to what you need; cleaning; search; model; API.
- **Watch out:** crowd-sourced data: sugar 300 g per 100 g exists.

### 9. Wine quality

- **Data:** UCI Wine Quality (red and white Vinho Verde, ~6,500 wines), `archive.ics.uci.edu`,
  CC BY 4.0. Small and clean: a good choice if your team wants to spend the time on the app.
- **App:** enter the chemical values of a wine and get a predicted quality; which values matter;
  compare red and white.
- **Model:** classification or regression (decide and explain why); baseline "always predict 6".
- **Work packages:** analysis and charts; model and evaluation; input validation; API; front end.
- **Watch out:** most wines are 5 or 6. Accuracy alone will flatter you.

### 10. Football results and a home advantage

- **Data:** `github.com/openfootball` (public domain), Bundesliga and other leagues, many seasons,
  as text files (parsing practice!) or the CSV exports.
- **App:** table for any season and matchday; head-to-head between two clubs; size of home
  advantage over the years (and in the 2020/21 seasons without spectators).
- **Model (optional):** Elo ratings computed from the results, then win/draw/loss probabilities
  for a match; compare with "home team always wins".
- **Work packages:** parsing; table computation (points, goal difference, tie rules); Elo;
  API; pages.
- **Watch out:** club names are spelled differently across seasons.

## Something different

### 11. Chess puzzle trainer

- **Data:** Lichess puzzle database (~5 million puzzles with rating, themes, popularity),
  `database.lichess.org`, CC0.
- **App:** serve a puzzle of a chosen rating and theme; check the user's move; track a simple
  session score.
- **Data work:** themes per rating range, how popularity relates to rating, which themes are
  hardest.
- **Model (optional):** predict a puzzle's rating from its themes and the number of moves.
- **Work packages:** loading the data; puzzle selection; move checking; drawing the board; API;
  statistics page.
- **Watch out:** a running puzzle has state that lives between requests.

### 12. Who wrote this? (text)

- **Data:** public-domain books from Project Gutenberg (`gutenberg.org`), e.g. 5–10 books by
  3–4 authors, English or German.
- **App:** paste a paragraph; the app guesses the author and shows why (typical words, sentence
  length). Word statistics per book.
- **Model:** a classifier on word counts.
- **Work packages:** getting and cleaning the texts; splitting into paragraphs; statistics;
  model; API.
- **Watch out:** if training and test paragraphs come from the same chapter, the model looks
  better than it is (same idea as testing on the last ten years in Ex 7).

## Bringing your own idea

Good, as long as:

- [ ] The data is real, freely available, and its licence allows use in a course project. Write
      the source and licence in your README.
- [ ] You can work with it on a laptop.
- [ ] There's something to compute with pandas, not just to display.
- [ ] The app does something a user would ask: a question goes in, an answer comes out.
- [ ] It splits into at least as many work packages as you have team members, plus a few small ones.
- [ ] You can say what the data reflects and what it doesn't.
- [ ] No personal data about real people beyond what's already public and needed.

Kaggle (`kaggle.com/datasets`), UCI (`archive.ics.uci.edu`), GovData (`govdata.de`) and the
scikit-learn toy datasets are good places to look. Check the licence on Kaggle: many datasets
there were copied from somewhere else.
