# from django.shortcuts import render

# # Create your views here.
# import joblib
# import numpy as np
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# model = joblib.load('performance/model.pkl')

# @api_view(['POST'])
# def predict_performance(request):
    
#     data = request.data
    
#     if data['sleep_hours']==0:
#         return Response({'Message':'They can\'t do the exam due to stress'})
    
#     if data['sleep_hours']==24 or data['hours_studied']==0 :
#         return Response({'Message':'They didn\'t study'})
    
#     features = np.array([[
#         data['hours_studied'],
#         data['previous_scores'],
#         1 if data['extracurricular'] else 0,
#         data['sleep_hours'],
#         data['sample_papers'],
#     ]])
#     prediction = model.predict(features)[0]
    
#     return Response({
#     'predicted_performance_index': round(float(prediction),2)
#     })

from django.shortcuts import render
import joblib
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Load your model
model = joblib.load('performance/model.pkl')

# Function to determine category (based on your Excel formula)
def get_student_category(hours_studied, sleep_hours):
    if 7 <= sleep_hours <= 8 and 4 <= hours_studied <= 6:
        return "Optimal Balance"
    elif sleep_hours < 6 and hours_studied > 6:
        return "Stressed Burnout"
    elif sleep_hours > 9 and hours_studied < 3:
        return "Underengaged"
    elif 6 <= sleep_hours <= 7 and hours_studied > 8:
        return "Inefficient High Effort"
    elif sleep_hours > 9 and hours_studied >= 3:
        return "Recovery Needed"
    else:
        return "Moderate"

# List of categories that need intervention (no performance prediction)
INTERVENTION_CATEGORIES = [
    'Stressed Burnout', 
    'Underengaged', 
    'Inefficient High Effort', 
    'Recovery Needed'
]

@api_view(['POST'])
def predict_performance(request):
    data = request.data
    
    # Get input values
    hours_studied = data['hours_studied']
    sleep_hours = data['sleep_hours']
    
    # Your existing special cases
    if sleep_hours == 0:
        return Response({
            'category': 'Extreme Stress',
            'message': 'Student cannot take exam due to extreme stress',
            'predicted_performance_index': None,
            'needs_intervention': True
        })
    
    if sleep_hours == 24 or hours_studied == 0:
        return Response({
            'category': 'Not Studied',
            'message': 'Student did not study at all',
            'predicted_performance_index': None,
            'needs_intervention': True
        })
    
    # Determine student category
    category = get_student_category(hours_studied, sleep_hours)
    
    # Check if category needs intervention
    if category in INTERVENTION_CATEGORIES:
        return Response({
            'category': category,
            'message': f'Student is {category}. Needs intervention before academic focus.',
            'predicted_performance_index': None,
            'needs_intervention': True
        })
    
    # Only predict performance for "good" categories
    features = np.array([[
        hours_studied,
        data['previous_scores'],
        1 if data['extracurricular'] else 0,
        sleep_hours,
        data['sample_papers'],
    ]])
    
    prediction = model.predict(features)[0]
    
    return Response({
        'category': category,
        'message': f'Student is {category}. Performance predicted.',
        'predicted_performance_index': round(float(prediction), 2),
        'needs_intervention': False
    })