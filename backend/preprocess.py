import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_preprocess():
    df = pd.read_csv("../dataset/data.csv", sep=";")

    # Keep only required columns
    df = df[["age", "height", "weight", "ap_hi", "ap_lo"]]

    # Convert age from days to years if needed
    if df["age"].max() > 200:
        df["age"] = df["age"] // 365

    # Create BP category (target)
    df["bp_level"] = df["ap_hi"].apply(
        lambda x: 0 if x < 120 else (1 if x < 140 else 2)
    )

    # Features & target
    X = df[["age", "height", "weight", "ap_hi", "ap_lo"]]
    y = df["bp_level"]

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler