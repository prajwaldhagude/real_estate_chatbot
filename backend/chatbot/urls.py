# backend/chatbot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check),
    path('analyze/', views.analyze_locality),
    path('compare/', views.compare_localities),
    path('download-csv/', views.download_csv),
    path('download-pdf/', views.download_pdf),
]
