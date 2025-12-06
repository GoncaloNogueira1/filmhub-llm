from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Watchlist
from .serializers import WatchlistAddSerializer, WatchlistItemSerializer
from movies.models import Movie


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watchlist_view(request):
    """
    GET: List user's watchlist
    POST: Add movie to watchlist
    """
    if request.method == 'GET':
        # List watchlist
        watchlist_items = Watchlist.objects.filter(
            user=request.user
        ).select_related('movie')
        
        serializer = WatchlistItemSerializer(watchlist_items, many=True)
        
        return Response({
            'watchlist': serializer.data,
            'count': watchlist_items.count()
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Add to watchlist
        serializer = WatchlistAddSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            movie_id = serializer.validated_data['movie_id']
            movie = Movie.objects.get(id=movie_id)
            
            watchlist_item, created = Watchlist.objects.get_or_create(
                user=request.user,
                movie=movie
            )
            
            response_serializer = WatchlistItemSerializer(watchlist_item)
            response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            
            return Response(
                {
                    'message': 'Movie added to watchlist' if created else 'Movie already in watchlist',
                    'watchlist_item': response_serializer.data
                },
                status=response_status
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_watchlist(request, movie_id):
    """Remove movie from watchlist"""
    watchlist_item = get_object_or_404(
        Watchlist,
        user=request.user,
        movie_id=movie_id
    )
    
    watchlist_item.delete()
    
    return Response(
        {'message': 'Movie removed from watchlist'},
        status=status.HTTP_204_NO_CONTENT
    )
