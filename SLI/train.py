import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

#Load the data from the csv file
df = pd.read_csv("sli_hand_landmarks.csv")
X = df.drop('label', axis=1)
y = df['label']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the model
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_scaled, y)

# Save the model
joblib.dump(model, "sli_model.pkl")
joblib.dump(scaler, "sli_scaler.pkl")