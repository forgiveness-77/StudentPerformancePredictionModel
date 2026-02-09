from django.urls import path
from .views import predict_performance, student_form

urlpatterns = [
    path('', student_form, name='performance-home'),
    path('predict/', predict_performance),
]