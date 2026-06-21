import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

st.set_page_config(
    page_title="Used Car Price Prediction System",
    page_icon="🚗",
    layout="wide"
)

model = joblib.load("src/best_car_price_model.pkl")

st.markdown("""
<div style="
padding:25px;
border-radius:15px;
background:linear-gradient(90deg,#0f172a,#2563eb);
text-align:center;
margin-bottom:20px;
box-shadow:0px 4px 15px rgba(0,0,0,0.2);
">
<h1 style="
color:white;
font-size:42px;
font-weight:bold;
margin-bottom:10px;
">
🚗 Used Car Price Prediction System
</h1>

<p style="
color:#dbeafe;
font-size:18px;
margin:0;
">
Estimate the resale value of your vehicle instantly
</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    year = st.number_input(
        "Manufacturing Year",
        min_value=2000,
        max_value=datetime.now().year,
        value=2020
    )

    present_price = st.number_input(
        "Present Price (Lakhs)",
        min_value=0.0,
        value=8.0
    )

    owner = st.selectbox(
        "Previous Owners",
        [0, 1, 2, 3]
    )

with col2:
    kms_driven = st.number_input(
        "Kilometers Driven",
        min_value=0,
        value=30000
    )

    fuel_type = st.selectbox(
        "Fuel Type",
        ["Petrol", "Diesel"]
    )

    seller_type = st.selectbox(
        "Seller Type",
        ["Dealer", "Individual"]
    )

    transmission = st.selectbox(
        "Transmission",
        ["Manual", "Automatic"]
    )
car_age = datetime.now().year - year

st.divider()
st.markdown("""
<style>
div.stButton > button {
    background-color: #bfdbfe;
    }
</style>
""", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])

if st.button("🚗 Predict Price",use_container_width=True):

    car_age = datetime.now().year - year
    mileage_per_year = kms_driven / max(car_age, 1)
    log_kms_driven = np.log1p(kms_driven)

    input_data = pd.DataFrame({
        "Year": [year],
        "Present_Price": [present_price],
        "Kms_Driven": [kms_driven],
        "Owner": [owner],
        "Car_Age": [car_age],
        "Mileage_per_Year": [mileage_per_year],
        "Log_Kms_Driven": [log_kms_driven],
        "Fuel_Type_Diesel": [1 if fuel_type == "Diesel" else 0],
        "Fuel_Type_Petrol": [1 if fuel_type == "Petrol" else 0],
        "Seller_Type_Individual": [1 if seller_type == "Individual" else 0],
        "Transmission_Manual": [1 if transmission == "Manual" else 0],
        "Age_Group_Old": [1 if car_age > 10 else 0]
    })

    prediction = model.predict(input_data)[0]

    st.toast("Prediction Completed Successfully 🚗")

    st.markdown(f"""
    <div style="
    padding:20px;
    border-radius:15px;
    background:#f8fafc;
    border:2px solid #60a5fa;
    text-align:center;
    margin-top:15px;
    ">
    <h3 style="color:#1e40af;">Estimated Market Value</h3>
    <h1 style="color:#2563eb;">₹ {prediction:.2f} Lakhs</h1>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        f"Expected Market Range: ₹ {max(prediction-0.5,0):.2f} - ₹ {prediction+0.5:.2f} Lakhs"
    )

    if car_age <= 5 and kms_driven <= 50000:
        st.success("⭐⭐⭐⭐⭐ Excellent Condition")
    elif car_age <= 8 and kms_driven <= 80000:
        st.info("⭐⭐⭐⭐ Good Condition")
    else:
        st.warning("⭐⭐⭐ Average Condition")

    st.subheader("📋 Vehicle Summary")

    summary = pd.DataFrame({
        "Feature": [
           "Manufacturing Year",
           "Fuel Type",
           "Transmission",
           "Previous Owners",
           "Vehicle Age"
       ],
       "Value": [
            year,
            fuel_type,
            transmission,
            owner,
            f"{car_age} Years"
       ]
    })

    st.table(summary)