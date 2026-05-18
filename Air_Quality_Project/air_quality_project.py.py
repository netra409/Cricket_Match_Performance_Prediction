# ------------------------------------
# 1 Import Libraries
# ------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

from sqlalchemy import create_engine
import pymysql


# ------------------------------------
# 2 Load Dataset
# ------------------------------------
df = pd.read_csv("real_time_air_quality_20k.csv")

print("Dataset Loaded")
print(df.head())


# ------------------------------------
# 3 Fix Column Names (important for MySQL)
# ------------------------------------
df = df.rename(columns={
    'PM2.5(Fine particulate matter)': 'PM25',
    'PM10(Coarse particulate matter)': 'PM10'
})


# ------------------------------------
# 4 Data Cleaning
# ------------------------------------
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)

df = df.drop_duplicates()

print("\nMissing Values:")
print(df.isnull().sum())


# ------------------------------------
# 5 Feature Engineering
# ------------------------------------
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month


# ------------------------------------
# 6 Exploratory Data Analysis
# ------------------------------------

# AQI Distribution
plt.figure()
plt.hist(df['AQI'], bins=30)
plt.title("AQI Distribution")
plt.xlabel("AQI")
plt.ylabel("Frequency")
plt.show()

# Average AQI by Hour
plt.figure()
df.groupby("hour")["AQI"].mean().plot()
plt.title("Average AQI by Hour")
plt.xlabel("Hour")
plt.ylabel("AQI")
plt.show()


# ------------------------------------
# 7 Machine Learning Model
# ------------------------------------

features = [
    'PM25',
    'PM10',
    'NO2',
    'SO2',
    'CO',
    'O3',
    'hour',
    'day',
    'month'
]

X = df[features]
y = df['AQI']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestRegressor(n_estimators=100, random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


# ------------------------------------
# 8 Model Evaluation
# ------------------------------------
print("\nModel Performance")

print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R2 Score:", r2_score(y_test, y_pred))


# ------------------------------------
# 9 Pollution Alert Detection
# ------------------------------------
AQI_THRESHOLD = 150

df['pollution_alert'] = df['AQI'].apply(
    lambda x: "High Pollution" if x > AQI_THRESHOLD else "Normal"
)

print(df[['AQI','pollution_alert']].head())


# ------------------------------------
# 10 Feature Importance
# ------------------------------------
importance = pd.Series(
    model.feature_importances_,
    index=features
).sort_values(ascending=False)

plt.figure()
importance.plot(kind='bar')
plt.title("Feature Importance")
plt.show()


# ------------------------------------
# 11 Export Clean Dataset for Power BI
# ------------------------------------
df.to_csv("real_time_air_quality_clean.csv", index=False)

print("\nClean dataset exported for Power BI")


# ------------------------------------
# 12 Python → MySQL Integration
# ------------------------------------
print("Rows to insert:", len(df))
engine = create_engine("mysql+pymysql://root:system@localhost/air_quality_db")

df.to_sql(
    name="air_quality",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data inserted into MySQL successfully")
    