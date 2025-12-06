from django.urls import path
from .views import get_recommendations

urlpatterns = [
    path('', get_recommendations, name='recommendations'),
]
