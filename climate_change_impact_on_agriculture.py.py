#1. Import Libraries & Load Data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector   # ← ADD THIS LINE

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# Load dataset
df = pd.read_csv("climate_change_impact_on_agriculture_350_entries.csv")
# 2. Data Overview

print("First 5 rows:")
print(df.head())

print("\nShape of dataset:", df.shape)

print("\nDataset info:")
print(df.info())

print("\nStatistical summary:")
print(df.describe())

#3. Data Cleaning & Preparation

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Handle missing values
numeric_cols = df.select_dtypes(include=np.number).columns
categorical_cols = df.select_dtypes(include='object').columns

df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# Encode categorical columns
le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])
# 4. Exploratory Data Analysis (EDA)
# Average Temperature Distribution
sns.histplot(df['Average_Temperature_C'], kde=True)
plt.title("Average Temperature Distribution")
plt.show()
# Rainfall vs Crop Yield
sns.scatterplot(
    x=df['Total_Precipitation_mm'],
    y=df['Crop_Yield_MT_per_HA']
)
plt.title("Rainfall vs Crop Yield")
plt.xlabel("Total Precipitation (mm)")
plt.ylabel("Crop Yield (MT/HA)")
plt.show()
# Correlation Heatmap

plt.figure(figsize=(12,8))
sns.heatmap(df.corr(), cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
#5. Machine Learning – Prediction Models
# Target Variable

X = df.drop('Crop_Yield_MT_per_HA', axis=1)
y = df['Crop_Yield_MT_per_HA']
#Train–Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
#Model 1: Linear Regression

lr = LinearRegression()
lr.fit(X_train, y_train)

lr_pred = lr.predict(X_test)

print("Linear Regression R2:", r2_score(y_test, lr_pred))
# Model 2: Random Forest Regressor (Best)
rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

print("Random Forest R2:", r2_score(y_test, rf_pred))
print("Random Forest RMSE:", np.sqrt(mean_squared_error(y_test, rf_pred)))
# 6. Actual vs Predicted Plot
plt.scatter(y_test, rf_pred)
plt.xlabel("Actual Crop Yield")
plt.ylabel("Predicted Crop Yield")
plt.title("Actual vs Predicted Crop Yield")
plt.show()


# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="system",   # your mysql password
    database="agriculture_db"
)

cursor = conn.cursor()

print("Connected to MySQL")

for actual, pred in zip(y_test, rf_pred):
    cursor.execute("""
        INSERT INTO crop_yield_predictions
        (actual_yield, predicted_yield)
        VALUES (%s, %s)
    """, (float(actual), float(pred)))

conn.commit()

print("Data inserted into MySQL")
cursor.close()
conn.close()