from django.urls import path
from .views import user_profile

urlpatterns = [
    path('profile/<int:user_id>/', user_profile, name='user_profile'),
]
