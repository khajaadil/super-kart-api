
import streamlit as st
import pandas as pd
import requests


# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Streamlit UI for Boston Housing Price Prediction
st.title("Super Kart Prediction App")
st.write("This app predicts the total sales.")

# Collect user input using sliders
Product_Id = st.slider("Product_Id")
Product_Weight = st.slider("Product_Weight")
Product_Sugar_Content = st.slider("Product_Sugar_Content")
Product_Allocated_Area = st.slider("Product_Allocated_Area")
Product_Type = st.slider("Product_Type")
Product_MRP = st.slider("Product_MRP")
Store_Id = st.slider("Store_Id")
Store_Establishment_Year = st.slider("Store_Establishment_Year")
Store_Size = st.slider("Store_Size")
Store_Location_City_Type = st.slider("Store_Location_City_Type")
Store_Type = st.slider("Store_Type")

# Categorical feature


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
        st.success(f"🏡 Predicted Median House Value: **${predicted_sales * 1000:.2f}**")
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
