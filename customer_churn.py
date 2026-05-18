import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# ===============================
# Load Dataset
# ===============================
df = pd.read_csv("customer_churn_350_entries.csv")

# ===============================
# Data Cleaning & Feature Engineering
# ===============================
df['Last_Login'] = pd.to_datetime(df['Last_Login'])

df['Days_Since_Last_Login'] = (
    pd.to_datetime('today') - df['Last_Login']
).dt.days

df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

df = pd.get_dummies(
    df,
    columns=['Gender', 'Subscription_Type'],
    drop_first=True
)

df.drop(['Customer_ID', 'Last_Login'], axis=1, inplace=True)

# ===============================
# Features & Target
# ===============================
X = df.drop('Churn', axis=1)
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===============================
# Logistic Regression
# ===============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train_scaled, y_train)

lr_pred = lr_model.predict(X_test_scaled)
lr_prob = lr_model.predict_proba(X_test_scaled)[:, 1]

print("\n===== Logistic Regression Results =====")
print(classification_report(y_test, lr_pred))
print("ROC-AUC:", roc_auc_score(y_test, lr_prob))

# ===============================
# Random Forest
# ===============================
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
print("ROC-AUC:", roc_auc_score(y_test, rf_prob))

# ===============================
# Save Predictions for Power BI
# ===============================
results = X_test.copy()
results['Actual_Churn'] = y_test.values
results['LR_Prediction'] = lr_pred
results['LR_Probability'] = lr_prob
results['RF_Prediction'] = rf_pred
results['RF_Probability'] = rf_prob

results.to_csv("churn_predictions_lr_rf.csv", index=False)

print("\nFile saved: churn_predictions_lr_rf.csv")
