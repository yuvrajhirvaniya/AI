import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime

# Get the directory of the current script (e.g., app.py)
current_dir = os.path.dirname(__file__)

# Create the full path to model.pkl in the same directory
model_path = os.path.join(current_dir, "model.pkl")

# Open and load the model
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Streamlit UI
st.title("Delivery Time Prediction App 🚀")

# User Inputs
product_category = st.selectbox("Product Category", ["books", "electronics", "fashion", "furniture"])
customer_state = st.selectbox("Customer State", ["SP", "RJ", "MG", "BA", "PR"])
seller_state = st.selectbox("Seller State", ["SP", "RJ", "MG", "BA", "PR"])
freight_value = st.number_input("Freight Value (in currency)", min_value=0.0, value=20.0, step=0.5)
order_date = st.date_input("Order Purchase Date", datetime.today())

# Convert Inputs
product_mapping = {category: idx for idx, category in enumerate(["books", "electronics", "fashion", "furniture"])}
state_mapping = {state: idx for idx, state in enumerate(["SP", "RJ", "MG", "BA", "PR"])}

# Encode Inputs
product_category_encoded = product_mapping[product_category]
customer_state_encoded = state_mapping[customer_state]
seller_state_encoded = state_mapping[seller_state]
order_year = order_date.year
order_month = order_date.month
order_day = order_date.day

# Create DataFrame
new_data = pd.DataFrame({
    'seller_state': [seller_state_encoded],
    'customer_state': [customer_state_encoded],
    'product_category_name_english': [product_category_encoded],
    'freight_value': [freight_value],
    'order_year': [order_year],
    'order_month': [order_month],
    'order_day': [order_day]
})



# Custom CSS for ghost-style button
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: white;
        color: white;
        border: 2px solid white;
        border-radius: 8px;
        padding: 6px 16px;
        font-size: 14px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    div.stButton > button:first-child:hover {
        background-color: black;
        color: white;
        border: 2px solid white;
    }
    </style>
""", unsafe_allow_html=True)



# Predict Delivery Time
if st.button("Predict Delivery Time"):
    delivery_time_prediction = model.predict(new_data)[0]
    st.success(f"📦 Predicted Delivery Time: {round(delivery_time_prediction, 2)} days")
