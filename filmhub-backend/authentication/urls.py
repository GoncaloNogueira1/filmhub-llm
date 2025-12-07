from django.urls import path
from .views import (
    register_user,
    login_user,
    user_profile,
    user_statistics,
    logout_view
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('profile/stats/', user_statistics, name='profile-stats'),
]
