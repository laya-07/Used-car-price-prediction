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

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🚗 Used Car Price Prediction System")

col1, col2 = st.columns(2)

with col1:
    year = st.number_input(
        "Manufacturing Year",
        min_value=2000,
        max_value=datetime.now().year,
        value=2018
    )

    present_price = st.number_input(
        "Present Price (Lakhs)",
        min_value=0.0,
        value=5.0
    )

    owner = st.selectbox(
        "Previous Owners",
        [0, 1, 2, 3]
    )

with col2:
    kms_driven = st.number_input(
        "Kilometers Driven",
        min_value=0,
        value=50000
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

if st.button("Predict Price", use_container_width=True):

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

    st.metric(
        "Estimated Market Value",
        f"₹ {prediction:.2f} Lakhs"
    )

    st.session_state.history.append({
        "Year": year,
        "Fuel": fuel_type,
        "Transmission": transmission,
        "Predicted Price (Lakhs)": round(prediction, 2)
    })

if st.button("Show Prediction History"):

    if st.session_state.history:

        st.subheader("Prediction History")

        st.dataframe(
            pd.DataFrame(st.session_state.history),
            use_container_width=True
        )

    else:
        st.info("No predictions made yet.")

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()