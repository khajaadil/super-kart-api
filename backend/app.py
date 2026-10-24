import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask("Super Kart Predictor")

# Load the trained model
model = joblib.load(saved_model_path)



# Define a route for the home page
@app.get('/')
def home():
    return "Welcome to the Super Kart Sales Prediction API!"

# Define an endpoint to predict sales for a single item
@app.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()

sample = {
        'Product_Id': data['Product_Id'],
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_Type': data['Product_Type'],
        'Product_MRP': data['Product_MRP'],     
        'Store_Id': data['Store_Id'],
        'Store_Establishment_Year': data['Store_Establishment_Year'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
    }
    # Convert the input data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Predicted_Sales': prediction})

# Define an endpoint to predict sales for a batch of items
@app.post('/v1/predictbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Add predictions to the DataFrame
    input_data['Product_Store_Sales_Total'] = predictions

    # Convert results to dictionary
    result = input_data.to_dict(orient="records")

    return jsonify(result)

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
