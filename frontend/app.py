
import streamlit as st
import pandas as pd
import requests


# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Streamlit UI for Boston Housing Price Prediction
st.title("Super Kart Prediction App")
st.write("This app predicts the total sales.")

Product_Id = st.text_input("Product_Id")
Product_Weight = st.text_input("Product_Weight")
Product_Allocated_Area = st.text_input("Product_Allocated_Area")
Product_MRP = st.text_input("Product_MRP")
Store_Establishment_Year = st.text_input("Store_Establishment_Year")

# Categorical feature
# Product Sugar Content
Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

# Product Type
Product_Type = st.selectbox(
    "Product Type",
    [
        "Baking Goods",
        "Breads",
        "Breakfast",
        "Canned",
        "Dairy",
        "Frozen Foods",
        "Fruits and Vegetables",
        "Hard Drinks",
        "Health and Hygiene",
        "Household",
        "Meat",
        "Others",
        "Seafood",
        "Snack Foods",
        "Soft Drinks",
        "Starchy Foods"
    ]
)

# Store ID
Store_Id = st.selectbox(
    "Store ID",
    ["OUT001", "OUT002", "OUT003", "OUT004"]
)

# Store Size
Store_Size = st.selectbox(
    "Store Size",
    ["High", "Medium", "Small"]
)

# Store Location City Type
Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

# Store Type
Store_Type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Food Mart",
        "Supermarket Type1",
        "Supermarket Type2"
    ]
)

# Create input DataFrame
input_data = {
    'Product_Id': Product_Id,
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Type': Product_Type,
    'Product_MRP': Product_MRP,
    'Store_Id': Store_Id,
    'Store_Establishment_Year': Store_Establishment_Year,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
}

if st.button("Predict", type='primary'):
    # Replace with your deployed backend URL
    response = requests.post(
        # "https://{BACKEND_URL}/v1/house",
        f"{BACKEND_URL}/v1/predict",
        json=input_data
    )

    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Product_Store_Sales_Total"]
        st.success(f"Predicted Sales Value: **${predicted_sales * 1000:.2f}**")
    else:
        st.error("Error in API request")


# Batch Prediction
st.subheader("Batch Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    if st.button("Predict for Batch", type='primary'):
        response = requests.post(
            f"{BACKEND_URL}/v1/predictbatch",
            files={"file": file}
        )

        if response.status_code == 200:
            result = response.json()
            st.header("Batch Prediction Results")
            st.write(result)
        else:
            st.error("Error in API request")
