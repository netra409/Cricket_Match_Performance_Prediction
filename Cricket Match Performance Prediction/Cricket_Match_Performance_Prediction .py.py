# --------------------------------
# Import Libraries
# --------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# --------------------------------
# Connect to MySQL
# --------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="system",
    database="cricket_db"
)

cursor = conn.cursor()

print("Connected to MySQL")

# --------------------------------
# Load Dataset
# --------------------------------
df = pd.read_csv("ball_300_entries.csv")

cols = [
    'runs','wickets','overs','economy','fours','sixes',
    'zeros','order','run_rate','run_conceded',
    'maidens','wides','no_balls'
]

df = df[cols].fillna(0)

# --------------------------------
# Exploratory Data Analysis
# --------------------------------

plt.figure()
plt.hist(df['runs'], bins=20)
plt.title("Distribution of Runs")
plt.xlabel("Runs")
plt.ylabel("Frequency")
plt.show()

plt.figure()
plt.hist(df['wickets'], bins=10)
plt.title("Distribution of Wickets")
plt.xlabel("Wickets")
plt.ylabel("Frequency")
plt.show()

# --------------------------------
# Runs Prediction Model
# --------------------------------

X_runs = df[['order','fours','sixes','zeros','run_rate']]
y_runs = df['runs']

Xr_train, Xr_test, yr_train, yr_test = train_test_split(
    X_runs, y_runs, test_size=0.2, random_state=42
)

runs_model = RandomForestRegressor(n_estimators=100, random_state=42)

runs_model.fit(Xr_train, yr_train)

runs_pred = runs_model.predict(Xr_test)

print("Runs Prediction R2 Score:", round(r2_score(yr_test, runs_pred),3))

# --------------------------------
# Wickets Prediction Model
# --------------------------------

X_wkts = df[['overs','run_conceded','economy','maidens','wides','no_balls']]
y_wkts = df['wickets']

Xw_train, Xw_test, yw_train, yw_test = train_test_split(
    X_wkts, y_wkts, test_size=0.2, random_state=42
)

wickets_model = RandomForestRegressor(n_estimators=100, random_state=42)

wickets_model.fit(Xw_train, yw_train)

wickets_pred = wickets_model.predict(Xw_test)

print("Wickets Prediction R2 Score:", round(r2_score(yw_test, wickets_pred),3))

# --------------------------------
# Save Predictions to MySQL
# --------------------------------

for i in range(len(runs_pred)):

    sql = """
    INSERT INTO ball_predictions
    (actual_runs, predicted_runs, actual_wickets, predicted_wickets)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        float(yr_test.iloc[i]),
        float(runs_pred[i]),
        float(yw_test.iloc[i]),
        float(wickets_pred[i])
    )

    cursor.execute(sql, values)

conn.commit()

print("Predictions inserted into MySQL")

cursor.close()
conn.close()