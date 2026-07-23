import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Cotton Remedy Dashboard",
    page_icon="🌿",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main {background-color:#f8fff8;}
.block-container {padding-top:2rem; padding-bottom:2rem;}
h1,h2,h3 {color:#14532d;}
.stButton>button {
    background: linear-gradient(90deg,#16a34a,#22c55e);
    color:white;
    border:none;
    border-radius:10px;
    padding:0.6rem 1rem;
    font-weight:bold;
}
.stMetric {
    background:#ffffff;
    padding:10px;
    border-radius:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

possible_dirs = [
    BASE_DIR / "Remedy v2",
    BASE_DIR / "Remedy v2 ",
    BASE_DIR,
]

MODEL_DIR = None
for folder in possible_dirs:
    if (folder / "remedy_model.pkl").exists():
        MODEL_DIR = folder
        break

if MODEL_DIR is None:
    st.error("Model file not found. Check remedy_model.pkl location.")
    st.stop()

model = joblib.load(MODEL_DIR / "remedy_model.pkl")
label_encoder = joblib.load(MODEL_DIR / "remedy_label_encoder.pkl")

# -----------------------------
# HEADER
# -----------------------------
st.title("🌿 Smart Cotton Remedy Recommendation")
st.caption("AI-powered dashboard for cotton crop health management")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("📌 About Project")
st.sidebar.write("Enter soil and environmental values to get the recommended remedy step instantly.")
st.sidebar.success("Model: Random Forest Classifier")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.subheader("📥 Enter Sensor / Soil Values")

col1, col2 = st.columns(2)

with col1:
    nitrogen = st.number_input("Nitrogen (N)", min_value=0.0, max_value=500.0, value=90.0)
    phosphorus = st.number_input("Phosphorus (P)", min_value=0.0, max_value=500.0, value=40.0)
    potassium = st.number_input("Potassium (K)", min_value=0.0, max_value=500.0, value=60.0)
    soil_moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=45.0)

with col2:
    light_intensity = st.number_input("Light Intensity", min_value=0.0, max_value=200000.0, value=50000.0)
    temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=70.0, value=30.0)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=65.0)

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("🔍 Predict Remedy"):
    input_df = pd.DataFrame([[nitrogen, phosphorus, potassium, soil_moisture,
                              light_intensity, temperature, humidity]],
        columns=["Nitrogen","Phosphorus","Potassium","Soil_Moisture",
                 "Light_Intensity","Temperature","Humidity"])

    pred = model.predict(input_df)
    remedy = label_encoder.inverse_transform(pred)[0]

    st.markdown("---")
    st.subheader("✅ Recommended Remedy Step")
    st.success(remedy)

    st.info("Use this recommendation as a decision-support output for crop care.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Developed for College Presentation | Smart Agriculture Dashboard")