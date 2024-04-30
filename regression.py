import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy import create_engine
import urllib.parse

# Database connection setup
username = 'root'
password = 'Vsreddy@0830'
host = 'localhost'
port = '3306'
database_name = 'django_db'
password = urllib.parse.quote_plus(password)  # URL encode the password
db_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"
engine = create_engine(db_url)

# Fetch data
query = "SELECT * FROM WeeklyGrades"
data = pd.read_sql(query, engine)

# Function to expand JSON fields into separate dataframe columns
def expand_json(data):
    new_data = pd.DataFrame()
    for idx, row in data.iterrows():
        try:
            result = json.loads(row['categorized_assignment_grades'])
            if isinstance(result, str):
                result = json.loads(result)
            for key, value in result.items():
                row[f"grade_{key}"] = value
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for row {idx}: {e}")
            continue
        new_data = pd.concat([new_data, pd.DataFrame([row])], ignore_index=True)
    return new_data

data = expand_json(data)
data['WeekNumber'] = data['WeekNumber'].apply(lambda x: int(x.split('-')[1].strip()))
training_data = data[data['WeekNumber'] <= 5]

# Prepare data for model
feature_columns = [col for col in training_data.columns if col.startswith('grade_')]
X = training_data[feature_columns]
y = training_data['PercentileGrade'].astype(float)

# Data splitting and scaling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model training
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Prediction and evaluation
y_pred = model.predict(X_test_scaled)


# Predicting for future weeks
future_week_data = np.mean(X_train_scaled, axis=0).reshape(1, -1)
predicted_grade = model.predict(future_week_data)
print(f"Predicted Grade for next Week: {predicted_grade[0]:.2f}")

# Determine risk of failing
failing_threshold = 60  # 60% grade considered failing
risk_of_failing = "High Risk" if predicted_grade[0] < failing_threshold else "Low Risk"
print(f"Risk of Failing: {risk_of_failing}")
