import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

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
"""csv_path = os.path.join(out_dir,'patients.csv')
patients.to_csv(csv_path,index=False)
print("Dataset saved to:",csv_path)
patients.head()"""
# Convert target variable to binary
"""patients['Readmitted_bin'] = patients['Readmitted'].map({'Yes':1,'No':0})

X = patients[['Age','Visits','Cholesterol','Diabetes']]
y = patients['Readmitted_bin']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

log_model = LogisticRegression(max_iter=200)
log_model.fit(X_train,y_train)
y_pred = log_model.predict(X_test)

print(classification_report(y_test,y_pred))"""
#Load CSV using `LOAD DATA` or `mysql.connector` in Python.
import pandas as pd
import mysql.connector

# Read CSV
df = pd.read_csv("hospital_patient_outputs/patients.csv")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="system",
    database="hospital_db"
)
cursor = conn.cursor()

# Insert rows
for _, row in df.iterrows():
    sql = """INSERT INTO patients
             (patient_id, age, gender, visits, bp_systolic, bp_diastolic, cholesterol, diabetes, readmitted, bp_ratio)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, tuple(row))

conn.commit()
cursor.close()
conn.close()
print("Data inserted into MySQL database.")