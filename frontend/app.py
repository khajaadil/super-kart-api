
import os
import streamlit as st
import pandas as pd
import requests


# Base URL of the Flask backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://172.18.0.1:7860").rstrip("/")

# Streamlit UI for Boston Housing Price Prediction
st.title("Super Kart Prediction App")
st.write("This app predicts the total sales.")

Product_Weight = st.text_input("Product_Weight")
Product_Allocated_Area = st.text_input("Product_Allocated_Area")
Product_MRP = st.text_input("Product_MRP")
Store_Age_Years = st.text_input("Store_Age_Years")


# Categorical feature
Product_Id_char = st.selectbox(
    "Product Id Char",
    ['FD', 'NC', 'DR']
)
# Product Sugar Content
Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

# Product Type
Product_Type_Category = st.selectbox(
    "Product_Type_Category",
    [
        "Perishables",
        "Non Perishables",
        "Others"
        
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
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Id_char': Product_Id_char,
    'Product_MRP': Product_MRP,
    'Store_Id': Store_Id,
    'Store_Age_Years': Store_Age_Years,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Product_Type_Category':Product_Type_Category
}

if st.button("Predict", type='primary'):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=input_data,
            timeout=30,
        )
        

        response.raise_for_status()
        result = response.json()


        predicted_sales = result["Predicted_Sales"]
        st.success(f"Predicted Sales Value: **{predicted_sales * 1000:.2f}**")
    except requests.exceptions.RequestException as error:
        st.error(f"Could not reach the prediction API at {BACKEND_URL}: {error}")
    except (KeyError, ValueError) as error:
        st.error(f"Invalid response from the prediction API: {error}")


# Batch Prediction
st.subheader("Batch Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    if st.button("Predict for Batch", type='primary'):
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files={"file": file},
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            st.header("Batch Prediction Results")
            st.write(result)
        except requests.exceptions.RequestException as error:
            st.error(f"Could not reach the prediction API at {BACKEND_URL}: {error}")
        except ValueError as error:
            st.error(f"Invalid response from the prediction API: {error}")
