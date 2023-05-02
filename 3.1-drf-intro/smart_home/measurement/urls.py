from django.urls import path
from .views import SensorAPIView, SensorUpdateAPIView, MeasurementAddAPIView

urlpatterns = [
    path('sensors/', SensorAPIView.as_view()),
    path('sensors/<int:pk>/', SensorUpdateAPIView.as_view()),
    path('measurements/', MeasurementAddAPIView.as_view()),
]
