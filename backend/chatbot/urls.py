from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_locality, name='analyze_locality'),
    path('health/', views.health_check, name='health_check'),
]
