from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from movies.models import Movie
from .models import Rating
from .serializers import (
    RatingCreateUpdateSerializer,
    RatingDetailSerializer,
    MovieRatingAggregateSerializer
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_movie(request, movie_id):
    """
    Create or update a rating for a movie.
    
    Requires JWT authentication.
    
    POST /api/movies/{id}/rate/
    Body: {
        "score": 1-5 (required),
        "comment": "text" (optional)
    }
    
    Returns the created/updated rating.
    """
    # Get movie or 404
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Check if rating already exists
    try:
        existing_rating = Rating.objects.get(user=request.user, movie=movie)
        is_update = True
    except Rating.DoesNotExist:
        existing_rating = None
        is_update = False
    
    # Serialize and validate
    serializer = RatingCreateUpdateSerializer(
        data=request.data,
        context={'request': request, 'movie': movie}
    )
    
    if serializer.is_valid():
        rating = serializer.save()
        
        # Determine response status
        response_status = status.HTTP_200_OK if is_update else status.HTTP_201_CREATED
        
        # Return detailed rating info
        response_serializer = RatingDetailSerializer(rating)
        return Response(response_serializer.data, status=response_status)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_movie_rating_aggregate(request, movie_id):
    """
    Get aggregate rating information for a movie.
    
    Public endpoint (no auth required).
    
    GET /api/movies/{id}/rating/
    
    Returns:
    {
        "movie_id": int,
        "average_score": float,
        "ratings_count": int
    }
    """
    # Get movie or 404
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Calculate aggregates
    aggregates = Rating.objects.filter(movie=movie).aggregate(
        average_score=Avg('score'),
        ratings_count=Count('id')
    )
    
    # Handle case where movie has no ratings
    average_score = aggregates['average_score']
    if average_score is not None:
        average_score = round(average_score, 1)
    else:
        average_score = 0.0
    
    data = {
        'movie_id': movie.id,
        'average_score': average_score,
        'ratings_count': aggregates['ratings_count'] or 0
    }
    
    serializer = MovieRatingAggregateSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_movie_rating(request, movie_id):
    """
    Get the authenticated user's rating for a specific movie.
    
    GET /api/movies/{id}/my-rating/
    
    Returns 404 if user hasn't rated the movie.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    
    try:
        rating = Rating.objects.get(user=request.user, movie=movie)
        serializer = RatingDetailSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Rating.DoesNotExist:
        return Response(
            {'detail': 'You have not rated this movie yet.'},
            status=status.HTTP_404_NOT_FOUND
        )
