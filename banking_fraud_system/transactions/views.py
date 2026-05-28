from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import pandas as pd
import joblib

from .models import Transaction


# Load trained ML model
model = joblib.load(
    '/Users/abhishekchavan/Downloads/Learning_science /Data_science/creditcard_fraud_detection/banking_fraud_system/models/rf_fraud_detection_model.pkl'
)

# Load scaler
scaler = joblib.load(
    '/Users/abhishekchavan/Downloads/Learning_science /Data_science/creditcard_fraud_detection/banking_fraud_system/models/scaler_model.pkl'
)


@csrf_exempt
def predict_transaction(request):
    try:
        # Only allow POST request
        if request.method == "POST":

            # Convert JSON request into Python dictionary
            df = json.loads(request.body)
            
            # Convert dictionary into DataFrame
            data = pd.DataFrame([df])
            
            # Numerical columns
            numerical_col = [
                'distance_from_home',
                'distance_from_last_transaction',
                'ratio_to_median_purchase_price',
                'repeat_retailer',
                'used_chip',
                'used_pin_number',
                'online_order'
                ]

            # Scale numerical data
            data[numerical_col] = scaler.transform(
                data[numerical_col]
            )

            # Fraud prediction
            prediction = model.predict(data)[0]

            # Fraud probability
            probability = model.predict_proba(data)[0][1]

            # Save transaction into PostgreSQL
            transaction = Transaction.objects.create(

                distance_from_home=data['distance_from_home'],

                distance_from_last_transaction=data['distance_from_last_transaction'],

                ratio_to_median_purchase_price=data['ratio_to_median_purchase_price'],
                repeat_retailer=data['repeat_retailer'],

                used_chip=data['used_chip'],

                used_pin_number=data['used_pin_number'],

                online_order=data['online_order'],

                fraud_prediction=bool(prediction),

                fraud_probability=round(float(probability), 2)
            )

            # Final API response
            response = {

                'transaction_id': transaction.id,

                'fraud_prediction': bool(prediction),

                'fraud_probability': round(float(probability), 2)
            }

            return JsonResponse(response)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)