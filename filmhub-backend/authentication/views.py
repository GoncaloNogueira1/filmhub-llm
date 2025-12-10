from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import models, connection
from django.http import JsonResponse
from django.utils import timezone
import logging
from .serializers import (
    RegisterSerializer, 
    LoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    LogoutSerializer  # ← Add this import
)

class RegisterView(APIView):
    """API endpoint for user registration"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'User created successfully',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'age': user.age
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """API endpoint for user login"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )


# ========== PROFILE VIEWS ==========

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    GET: Retrieve current user's profile
    PATCH: Update current user's profile
    
    GET /api/auth/profile/
    PATCH /api/auth/profile/
    Body: {
        "first_name": "John",
        "last_name": "Doe",
        "age": 25,
        "bio": "Movie enthusiast",
        "favorite_genres": {"28": 0.9, "18": 0.6},
        "email_notifications": true
    }
    """
    user = request.user
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        serializer = UserProfileUpdateSerializer(
            user,
            data=request.data,
            partial=True,  # Allow partial updates
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # Return updated profile
            response_serializer = UserProfileSerializer(user)
            return Response({
                'message': 'Profile updated successfully',
                'profile': response_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_statistics(request):
    """
    Get user's movie statistics
    
    GET /api/auth/profile/stats/
    """
    from ratings.models import Rating
    from watchlist.models import Watchlist
    from collections import Counter
    
    user = request.user
    
    # Get statistics
    total_ratings = Rating.objects.filter(user=user).count()
    avg_rating = Rating.objects.filter(user=user).aggregate(
        avg=models.Avg('score')
    )['avg'] or 0
    
    watchlist_count = Watchlist.objects.filter(user=user).count()
    
    # Get favorite genres from ratings
    rated_movies = Rating.objects.filter(
        user=user,
        score__gte=4
    ).select_related('movie')
    
    genre_counts = Counter()
    for rating in rated_movies:
        for genre in rating.movie.genres:
            genre_counts[genre] += 1
    
    top_genres = [
        {'genre': genre, 'count': count}
        for genre, count in genre_counts.most_common(5)
    ]
    
    return Response({
        'total_ratings': total_ratings,
        'average_rating': round(avg_rating, 2),
        'watchlist_count': watchlist_count,
        'top_genres': top_genres,
    }, status=status.HTTP_200_OK)


# Legacy function-based views for compatibility
def register_user(request):
    """Wrapper for RegisterView"""
    return RegisterView.as_view()(request)


def login_user(request):
    """Wrapper for LoginView"""
    return LoginView.as_view()(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user by blacklisting refresh token
    
    POST /api/auth/logout/
    Body (optional): {"refresh": "refresh_token_here"}
    
    Returns:
        205 Reset Content - Standard logout response
    
    Note:
        - Blacklists the refresh token if provided
        - Access token remains valid until expiration (stateless JWT)
        - Frontend should delete both access and refresh tokens
    """
    serializer = LogoutSerializer(data=request.data)
    
    if serializer.is_valid():
        refresh_token = request.data.get('refresh')
        serializer.save()
        
        # Check if refresh token was provided
        if refresh_token:
            return Response(
                {
                    'message': 'Successfully logged out',
                    'detail': 'Refresh token has been blacklisted. Please remove tokens from client storage.'
                },
                status=status.HTTP_205_RESET_CONTENT
            )
        else:
            # If no refresh token provided, still return success
            # (user deleted tokens on frontend)
            return Response(
                {
                    'message': 'Logged out',
                    'detail': 'No refresh token provided. Ensure tokens are removed from client.'
                },
                status=status.HTTP_205_RESET_CONTENT
            )
    
    # If serializer is invalid, still return success
    # (user deleted tokens on frontend)
    return Response(
        {
            'message': 'Logged out',
            'detail': 'No refresh token provided. Ensure tokens are removed from client.'
        },
        status=status.HTTP_205_RESET_CONTENT
    )


logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        response_data = {
            "status": "healthy",
            "database": "connected",
            "timestamp": timezone.now().isoformat()
        }
        logger.info("Health check passed")
        return JsonResponse(response_data, status=200)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        response_data = {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": timezone.now().isoformat()
        }
        return JsonResponse(response_data, status=503)