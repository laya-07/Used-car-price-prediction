import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load Model
model = joblib.load("src/best_car_price_model.pkl")

st.title("Used Car Price Prediction")

st.write("Enter Car Details")

year = st.number_input("Year", min_value=2000, max_value=2025, value=2018)

present_price = st.number_input(
    "Present Price (Lakhs)",
    min_value=0.0,
    value=5.0
)

kms_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=50000
)

owner = st.selectbox(
    "Number of Previous Owners",
    [0, 1, 2, 3]
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

if st.button("Predict Price"):

    car_age = 2025 - year

    mileage_per_year = kms_driven / max(car_age, 1)

    log_kms_driven = np.log1p(kms_driven)

    fuel_type_diesel = 1 if fuel_type == "Diesel" else 0
    fuel_type_petrol = 1 if fuel_type == "Petrol" else 0

    seller_type_individual = 1 if seller_type == "Individual" else 0

    transmission_manual = 1 if transmission == "Manual" else 0

    age_group_old = 1 if car_age > 10 else 0

    input_data = pd.DataFrame({
        "Year":[year],
        "Present_Price":[present_price],
        "Kms_Driven":[kms_driven],
        "Owner":[owner],
        "Car_Age":[car_age],
        "Mileage_per_Year":[mileage_per_year],
        "Log_Kms_Driven":[log_kms_driven],
        "Fuel_Type_Diesel":[fuel_type_diesel],
        "Fuel_Type_Petrol":[fuel_type_petrol],
        "Seller_Type_Individual":[seller_type_individual],
        "Transmission_Manual":[transmission_manual],
        "Age_Group_Old":[age_group_old]
    })

    prediction = model.predict(input_data)

    st.success(
        f"Predicted Selling Price: ₹ {prediction[0]:.2f} Lakhs"
    )