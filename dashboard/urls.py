from django.urls import path
from .views import dashboard_home, profile, teams, targets, campaigns

urlpatterns = [
    path('', dashboard_home, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('teams/', teams, name='teams'),
    path('targets/', targets, name='targets'),
    path('campaigns/', campaigns, name='campaigns'),
]