from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing'),  # This will map the landing page to the root URL
]
