import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# 1. Load dataset
df = pd.read_csv("cotton_remedy_dataset.csv")

# 2. Features & Target
X = df[[
    "Nitrogen",
    "Phosphorus",
    "Potassium",
    "Soil_Moisture",
    "Light_Intensity",
    "Temperature",
    "Humidity"
]]

y = df["Remedy"]

# 3. Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 4. Train / Val / Test split (70 / 15 / 15)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y_encoded, test_size=0.15, random_state=42, stratify=y_encoded
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.176, random_state=42, stratify=y_temp
)
# (0.176 of 85% ≈ 15%)

# 5. Model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

# 6. Train
model.fit(X_train, y_train)

# 7. Predictions
train_pred = model.predict(X_train)
val_pred = model.predict(X_val)
test_pred = model.predict(X_test)

# 8. Accuracy
train_acc = accuracy_score(y_train, train_pred)
val_acc = accuracy_score(y_val, val_pred)
test_acc = accuracy_score(y_test, test_pred)

print("\nTrain Accuracy:", train_acc)
print("Validation Accuracy:", val_acc)
print("Test Accuracy:", test_acc)

# 9. Save model
joblib.dump(model, "remedy_model.pkl")
joblib.dump(label_encoder, "remedy_label_encoder.pkl")

# 10. Plot Accuracy

labels = ["Train", "Validation", "Test"]
values = [train_acc, val_acc, test_acc]

plt.figure()
plt.bar(labels, values)
plt.title("Model Accuracy Comparison")
plt.xlabel("Dataset")
plt.ylabel("Accuracy")
plt.ylim(0, 1)

plt.show()