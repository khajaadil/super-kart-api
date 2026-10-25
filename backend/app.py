import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize Flask app
app = Flask("Super Kart Predictor")

# Load the trained model
saved_model_path = os.path.join(os.path.dirname(__file__), 'super_kart_model_v3_0.joblib')
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
    app.logger.info("3333333")
    app.logger.info(data)
    sample = {
        'Product_Id_char': data['Product_Id_char'],
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_Type_Category': data['Product_Type_Category'],
        'Product_MRP': data['Product_MRP'],     
        'Store_Id': data['Store_Id'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
    }
    # Convert the input data into a DataFrame
    input_data = pd.DataFrame([sample])
    app.logger.info("*********")
    app.logger.info(input_data.iloc[0])
    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]
    app.logger.info("Prediction completed: %s", prediction)
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
