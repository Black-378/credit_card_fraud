from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class FraudCheckView(APIView):
    def post(self, request):
        # Here you would typically process the transaction data and run it through your fraud detection model
        data = request.data
        # For demonstration, we'll just return a dummy response
        is_fraudulent = False  # Replace with actual model prediction
        return Response({'is_fraudulent': is_fraudulent})