from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .engine import get_content_based_recommendations
from .serializers import RecommendationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    """
    Get personalized movie recommendations for authenticated user
    
    GET /api/recommendations/?limit=20
    
    Returns:
        - recommendations: List of movies with predicted_score
        - strategy: 'content-based' or 'cold-start'
        - count: Number of recommendations returned
    
    Algorithm:
    - If user has ratings >= 3: content-based filtering (genre + keyword overlap)
    - If user has no ratings: popular movies (cold-start fallback)
    - Excludes movies user already rated or has in watchlist
    """
    user = request.user
    limit = int(request.query_params.get('limit', 20))
    
    # Validate limit
    if limit < 1 or limit > 100:
        return Response(
            {'error': 'Limit must be between 1 and 100'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get recommendations
    scored_movies = get_content_based_recommendations(user, limit)
    
    # Determine strategy used
    from ratings.models import Rating
    user_rating_count = Rating.objects.filter(user=user).count()
    strategy = 'content-based' if user_rating_count > 0 else 'cold-start'
    
    # Attach predicted_score to each movie
    movies_with_scores = []
    for movie, score in scored_movies:
        movie.predicted_score = score
        movies_with_scores.append(movie)
    
    # Serialize
    serializer = RecommendationSerializer(movies_with_scores, many=True)
    
    return Response({
        'recommendations': serializer.data,
        'strategy': strategy,
        'count': len(serializer.data),
        'user_ratings_count': user_rating_count
    }, status=status.HTTP_200_OK)
