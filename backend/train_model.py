from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from preprocess import load_and_preprocess

# Load data
X, y, scaler = load_and_preprocess()

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("Model trained successfully ✅")