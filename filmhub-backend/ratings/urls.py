from django.urls import path
from .views import (
    rate_movie,
    get_movie_rating_aggregate,
    get_user_movie_rating
)

urlpatterns = [
    path('<int:movie_id>/rate/', rate_movie, name='rate-movie'),
    path('<int:movie_id>/rating/', get_movie_rating_aggregate, name='movie-rating-aggregate'),
    path('<int:movie_id>/my-rating/', get_user_movie_rating, name='my-movie-rating'),
]
