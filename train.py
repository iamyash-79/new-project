import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load dataset
df = pd.read_csv("fuel_data.csv")

# Required columns
required_cols = {
    'Engine_Size(L)',
    'Cylinders',
    'Transmission',
    'Fuel Type',
    'Fuel Consumption(Comb (mpg))'
}

missing_cols = required_cols - set(df.columns)
if missing_cols:
    raise ValueError(f"🚫 Error: columns are missing: {missing_cols}")

# Drop rows where target is NaN
df = df.dropna(subset=['Fuel Consumption(Comb (mpg))'])

# Features and Target
X = df[['Engine_Size(L)', 'Cylinders', 'Transmission', 'Fuel Type']]
y = df['Fuel Consumption(Comb (mpg))']

# Preprocessing: One-hot encode categorical columns
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), ['Transmission', 'Fuel Type'])
], remainder='passthrough')

# Full Pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("✅ model.pkl created successfully.")
