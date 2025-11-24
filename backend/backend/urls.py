# backend/urls.py (project urls)
from django.urls import path, include

urlpatterns = [
    path('api/', include('chatbot.urls')),  # adjust path/app name based on your structure
]
