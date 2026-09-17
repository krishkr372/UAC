import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

#Load the data from the csv file. You have to download the csv file from the link provided in the README.md file and place it in the same directory as this script.
df = pd.read_csv("sli_hand_landmarks.csv")
X = df.drop('label', axis=1)
y = df['label']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
x_train, x_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# Evaluate the model
accuracy = model.score(x_test, y_test)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the model
joblib.dump(model, "sli_asl_model.pkl")
joblib.dump(scaler, "sli_asl_scaler.pkl")