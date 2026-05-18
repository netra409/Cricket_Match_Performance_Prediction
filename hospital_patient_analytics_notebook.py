# %% [markdown]
# # Case Study 3: Hospital Patient Analytics
#
# **Problem Statement:**  
# A hospital wants to monitor patients’ vital records and predict risk of readmission.
#
# **Tasks:**
# - Create patient dataset with vitals and readmission info.
# - Derive BP Ratio.
# - Perform EDA (cholesterol by diabetes, readmission counts, age distribution).
# - Predict readmission likelihood with Logistic Regression.
# - Provide MySQL, Excel, and Power BI integration notes.

# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import seaborn as sns
import matplotlib.pyplot as plt


# Create output folder
out_dir = "hospital_patient_outputs"
os.makedirs(out_dir, exist_ok=True)

# %% [markdown]
# ## Step 1: Create Dataset

# %%
data = [
    ["P001",45,"M",3,140,90,220,1,"Yes"],
    ["P002",32,"F",1,120,80,180,0,"No"],
    ["P003",60,"M",4,150,95,250,1,"Yes"],
    ["P004",29,"F",2,118,78,170,0,"No"],
    ["P005",55,"M",5,160,100,260,1,"Yes"],
    ["P006",40,"F",1,125,82,200,0,"No"],
    ["P007",50,"M",2,145,92,230,1,"Yes"],
    ["P008",35,"F",3,130,85,190,0,"No"],
    ["P009",70,"M",6,170,110,280,1,"Yes"],
    ["P010",42,"F",2,128,84,210,0,"No"],
    ["P011",65,"M",4,155,98,240,1,"Yes"],
    ["P012",38,"F",2,122,80,185,0,"No"],
    ["P013",48,"M",3,135,88,205,1,"Yes"],
    ["P014",30,"F",1,118,76,175,0,"No"],
    ["P015",53,"M",5,162,102,265,1,"Yes"],
    ["P016",41,"F",2,126,82,195,0,"No"],
    ["P017",58,"M",4,150,95,250,1,"Yes"],
    ["P018",36,"F",2,124,80,185,0,"No"],
    ["P019",62,"M",5,168,105,270,1,"Yes"],
    ["P020",33,"F",1,119,77,178,0,"No"]
]

cols = ["PatientID","Age","Gender","Visits","BP_Systolic","BP_Diastolic","Cholesterol","Diabetes","Readmitted"]
patients = pd.DataFrame(data,columns=cols)

# Derived column
patients['BP_Ratio'] = patients['BP_Systolic']/patients['BP_Diastolic']

# Save CSV
csv_path = os.path.join(out_dir,'patients.csv')
patients.to_csv(csv_path,index=False)
print("Dataset saved to:",csv_path)
patients.head()

# %% [markdown]
# ## Step 2: Exploratory Data Analysis (EDA)

# %%
"""print("Average cholesterol by diabetes status:\n",patients.groupby('Diabetes')['Cholesterol'].mean())

print("\nReadmission counts:\n",patients['Readmitted'].value_counts())

patients['Age'].hist(bins=5)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()"""

# %% [markdown]
# ## Step 3: Logistic Regression – Predict Readmission

# %%
# Convert target variable to binary
"""patients['Readmitted_bin'] = patients['Readmitted'].map({'Yes':1,'No':0})

X = patients[['Age','Visits','Cholesterol','Diabetes']]
y = patients['Readmitted_bin']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

log_model = LogisticRegression(max_iter=200)
log_model.fit(X_train,y_train)
y_pred = log_model.predict(X_test)

print(classification_report(y_test,y_pred))"""

# %% [markdown]
# ## Step 4: Integration Notes
#
# **MySQL:**
# ```sql
# CREATE TABLE patients (
  #  patient_id VARCHAR(10) PRIMARY KEY,
   # age INT,
   #gender CHAR(1),
   # visits INT,
   # bp_systolic INT,
   # bp_diastolic INT,
   # cholesterol INT,
   # diabetes TINYINT,
#readmitted VARCHAR(3)
#);
# ```
# Load CSV using `LOAD DATA` or `mysql.connector` in Python.
#
# **Excel:**
# - Import `patients.csv`
# - Pivot: Diabetes vs Average Cholesterol
# - Pie Chart: Readmission distribution
#
# **Power BI:**
# - Import `patients.csv`
# - KPI: % readmitted with diabetes
# - Bar chart: Readmission by Age Group
# - Scatter: BP_Systolic vs Cholesterol

"""from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Features (independent variables)
X = patients[['Age','Visits','BP_Systolic','BP_Diastolic','Diabetes']]

# Target (dependent variable)
y = patients['Cholesterol']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train model
lin_model = LinearRegression()
lin_model.fit(X_train, y_train)

# Predictions
y_pred = lin_model.predict(X_test)

# Evaluation
print("Coefficients:", lin_model.coef_)
print("Intercept:", lin_model.intercept_)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))

#Pivot – Diabetes vs Average Cholesterol
pivot_table = patients.groupby('Diabetes')['Cholesterol'].mean().reset_index()

plt.figure(figsize=(6,4))
sns.barplot(x="Diabetes", y="Cholesterol", data=pivot_table, palette="Set2")
plt.title("Average Cholesterol by Diabetes Status")
plt.xlabel("Diabetes (0=No, 1=Yes)")
plt.ylabel("Average Cholesterol")
plt.show()

# Pie Chart – Readmission Distribution
readmission_counts = patients['Readmitted'].value_counts()

plt.figure(figsize=(5,5))
plt.pie(readmission_counts, labels=readmission_counts.index,
        autopct='%1.1f%%', colors=sns.color_palette("Set2"))
plt.title("Readmission Distribution")
plt.show()"""

import pandas as pd
import mysql.connector
#mysql

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='system'
)
mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS Hospital")
db.close()

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='system',
    database='hospital_data'
)
mycursor = db.cursor()

mycursor.execute("Drop table if exists Patients")
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Patients (
        PatientID VARCHAR(10) PRIMARY KEY,
        Age INT,
        Gender CHAR(1),
        Visits INT,
        BP_Systolic INT,
        BP_Diastolic INT,
        Cholesterol INT,
        Diabetes INT,
        Readmitted VARCHAR(3)
    )
""")

#insert data from DataFrame
for _, row in patients.iterrows():
    mycursor.execute("""
        INSERT IGNORE INTO Patients (PatientID, Age, Gender, Visits, BP_Systolic, BP_Diastolic, Cholesterol, Diabetes, Readmitted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['PatientID'], row['Age'], row['Gender'], row['Visits'],
        row['BP_Systolic'], row['BP_Diastolic'], row['Cholesterol'],
        row['Diabetes'], row['Readmitted']
    ))

db.commit()

