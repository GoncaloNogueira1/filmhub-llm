from django.urls import path
from .views import watchlist_view, remove_from_watchlist

urlpatterns = [
    path('', watchlist_view, name='watchlist'),
    path('<int:movie_id>/', remove_from_watchlist, name='remove-from-watchlist'),
]
