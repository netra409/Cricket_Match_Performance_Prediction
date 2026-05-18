# ==========================================
# Import Libraries
# ==========================================
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# ==========================================
# Load Dataset
# ==========================================
df = pd.read_csv("customer_churn_350_entries.csv")

print("\nDataset Loaded Successfully")

# ==========================================
# Dataset Overview
# ==========================================
print("\nFirst 5 Rows")
print(df.head())

print("\nDataset Info")
print(df.info())

print("\nStatistical Summary")
print(df.describe())

print("\nMissing Values")
print(df.isnull().sum())

# ==========================================
# Data Cleaning & Feature Engineering
# ==========================================

# Convert date column
df['Last_Login'] = pd.to_datetime(df['Last_Login'])

# Create new feature
df['Days_Since_Last_Login'] = (
    pd.to_datetime('today') - df['Last_Login']
).dt.days

# Convert churn to numeric
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Encode categorical variables
df = pd.get_dummies(
    df,
    columns=['Gender', 'Subscription_Type'],
    drop_first=True
)

# Remove unnecessary columns
df.drop(['Customer_ID', 'Last_Login'], axis=1, inplace=True)

print("\nColumns after preprocessing")
print(df.columns)

# ==========================================
# Features & Target
# ==========================================
X = df.drop('Churn', axis=1)
y = df['Churn']

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Data Size:", X_train.shape)
print("Testing Data Size:", X_test.shape)

# ==========================================
# Logistic Regression Model
# ==========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train_scaled, y_train)

lr_pred = lr_model.predict(X_test_scaled)
lr_prob = lr_model.predict_proba(X_test_scaled)[:, 1]

print("\n===== Logistic Regression Results =====")
print(classification_report(y_test, lr_pred))
print("ROC-AUC Score:", roc_auc_score(y_test, lr_prob))

print("\nConfusion Matrix (Logistic Regression)")
print(confusion_matrix(y_test, lr_pred))

# ==========================================
# Random Forest Model
# ==========================================

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
rf_prob = rf_model.predict_proba(X_test)[:, 1]

print("\n===== Random Forest Results =====")
print(classification_report(y_test, rf_pred))
print("ROC-AUC Score:", roc_auc_score(y_test, rf_prob))

print("\nConfusion Matrix (Random Forest)")
print(confusion_matrix(y_test, rf_pred))

# ==========================================
# Feature Importance (Random Forest)
# ==========================================

importance = rf_model.feature_importances_
features = X.columns

plt.figure()
plt.barh(features, importance)
plt.xlabel("Importance Score")
plt.title("Feature Importance (Random Forest)")
plt.show()

# ==========================================
# Model Comparison
# ==========================================

lr_auc = roc_auc_score(y_test, lr_prob)
rf_auc = roc_auc_score(y_test, rf_prob)

print("\n===== Model Comparison =====")
print("Logistic Regression ROC-AUC:", lr_auc)
print("Random Forest ROC-AUC:", rf_auc)

# ==========================================
# Save Predictions for Power BI
# ==========================================

results = X_test.copy()

results['Actual_Churn'] = y_test.values
results['LR_Prediction'] = lr_pred
results['LR_Probability'] = lr_prob
results['RF_Prediction'] = rf_pred
results['RF_Probability'] = rf_prob

results.to_csv("churn_predictions_lr_rf.csv", index=False)

print("\nCSV File saved: churn_predictions_lr_rf.csv")


import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="system",
    database="churn_db"
)

cursor = conn.cursor()

print("Connected to MySQL")

insert_query = """
INSERT INTO churn_predictions (
Age,
Monthly_Charges,
Tenure_Months,
Total_Spend,
Days_Since_Last_Login,
Gender_Male,
Subscription_Type_Premium,
Subscription_Type_Standard,
Actual_Churn,
LR_Prediction,
LR_Probability,
RF_Prediction,
RF_Probability
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

for i, row in results.iterrows():

    values = (
        row['Age'],
        row['Monthly_Charges'],
        row['Tenure_Months'],
        row['Total_Spend'],
        row['Days_Since_Last_Login'],
        row['Gender_Male'],
        row['Subscription_Type_Premium'],
        row['Subscription_Type_Standard'],
        row['Actual_Churn'],
        row['LR_Prediction'],
        row['LR_Probability'],
        row['RF_Prediction'],
        row['RF_Probability']
    )

    cursor.execute(insert_query, values)

conn.commit()

print("Data inserted successfully")

cursor.close()
conn.close()