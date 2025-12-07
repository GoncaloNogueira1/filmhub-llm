from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    user_profile,
    user_statistics,
    logout_view  # ← Add this import
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),  # ← Add this
    path('profile/', user_profile, name='profile'),
    path('profile/stats/', user_statistics, name='profile-stats'),
]
