import mysql.connector
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from flask_cors import CORS
import bcrypt
import os

# ✅ DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="priyakrishna06",
    database="bp_system"
)
cursor = db.cursor()

app = Flask(__name__)
CORS(app)

# ✅ Load model & scaler
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ====================================================
# ✅ FRONTEND ROUTES (VERY IMPORTANT)
# ====================================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ====================================================
# ✅ AUTHENTICATION
# ====================================================

# Register
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    query = "INSERT INTO users (email, password) VALUES (%s, %s)"
    cursor.execute(query, (data["email"], hashed))
    db.commit()

    return {"message": "User registered successfully"}

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    query = "SELECT password FROM users WHERE email=%s"
    cursor.execute(query, (data["email"],))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]

        # Fix byte/string issue
        if isinstance(stored_password, str):
            stored_password = stored_password.encode()

        if bcrypt.checkpw(data["password"].encode(), stored_password):
            return {"message": "Login success"}

    return {"message": "Invalid credentials"}, 401

# ====================================================
# ✅ PREDICTION
# ====================================================

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    age = data["age"]
    height = data["height"]
    weight = data["weight"]
    ap_hi = data["ap_hi"]
    ap_lo = data["ap_lo"]

    # Convert to model input
    features = np.array([[age, height, weight, ap_hi, ap_lo]])
    features = scaler.transform(features)

    pred = model.predict(features)[0]
    result = ["Normal", "Elevated", "Hypertension"][pred]

    # Save to DB
    query = """
    INSERT INTO patients (age, height, weight, ap_hi, ap_lo, prediction)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (age, height, weight, ap_hi, ap_lo, result))
    db.commit()

    return jsonify({"prediction": result})

# ====================================================
# ✅ PATIENT HISTORY
# ====================================================

@app.route("/patients", methods=["GET"])
def get_patients():
    cursor.execute("""
        SELECT age, height, weight, ap_hi, ap_lo, prediction 
        FROM patients ORDER BY id DESC
    """)
    data = cursor.fetchall()

    result = []
    for row in data:
        result.append({
            "age": row[0],
            "height": row[1],
            "weight": row[2],
            "ap_hi": row[3],
            "ap_lo": row[4],
            "prediction": row[5]
        })

    return jsonify(result)

# ====================================================
# ✅ AI CHATBOT
# ====================================================

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data["message"]

    msg = user_msg.lower()

    if "bp" in msg or "blood pressure" in msg:
        reply = "Normal BP is around 120/80 mmHg. Regular monitoring is important."

    elif "high" in msg or "hypertension" in msg:
        reply = "High BP can be controlled with exercise, low salt diet, stress management, and proper medication."

    elif "low" in msg:
        reply = "Low BP may cause dizziness or fainting. Drink fluids and consult a doctor if symptoms persist."

    elif "symptoms" in msg:
        reply = "High BP often has no symptoms, but severe cases may include headaches, chest pain, or dizziness."

    elif "diet" in msg or "food" in msg:
        reply = "Eat fruits, vegetables, whole grains, and reduce salt, sugar, and fried foods."

    elif "exercise" in msg or "workout" in msg:
        reply = "Regular exercise like walking, jogging, or yoga for 30 minutes daily helps control BP."

    elif "salt" in msg:
        reply = "Reducing salt intake is very important to control high blood pressure."

    elif "stress" in msg:
        reply = "Manage stress through meditation, deep breathing, and proper sleep."

    elif "weight" in msg:
        reply = "Maintaining a healthy weight helps reduce the risk of high blood pressure."

    elif "smoking" in msg:
        reply = "Avoid smoking as it increases blood pressure and damages blood vessels."

    elif "alcohol" in msg:
        reply = "Limit alcohol consumption as it can increase blood pressure."

    elif "medicine" in msg or "treatment" in msg:
        reply = "Consult a doctor for proper medication if lifestyle changes are not enough."

    elif "prevention" in msg:
        reply = "Healthy diet, regular exercise, low salt intake, and stress control help prevent BP issues."

    elif "normal range" in msg:
        reply = "Normal BP: 120/80 mmHg, Elevated: 120-129/<80, Hypertension: 130/80 or higher."

    elif "age" in msg:
        reply = "Blood pressure risk increases with age, so regular check-ups are important."

    elif "water" in msg:
        reply = "Drinking enough water helps maintain overall health and stable blood pressure."

    elif "sleep" in msg:
        reply = "Good sleep (7–8 hours) is essential for maintaining healthy blood pressure."

    elif "heart" in msg:
        reply = "High BP increases the risk of heart disease, so early control is important."

    elif "hello" in msg or "hi" in msg:
        reply = "Hello! 😊 I am your BP Health Assistant. Ask me anything about blood pressure."

    elif "thank" in msg:
        reply = "You're welcome! Stay healthy 😊"

    else:
        reply = "I can help with BP, diet, exercise, and health tips. Please ask something related 😊"

    return {"reply": reply}

# ====================================================
# ✅ RUN APP
# ====================================================

if __name__ == "__main__":
    app.run(debug=True)
    
