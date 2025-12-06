from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q
from .models import Movie
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    MovieSearchSerializer
)
class MoviePagination(PageNumberPagination):
    """Custom pagination for movies"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class SearchPagination(PageNumberPagination):
    """Custom pagination for search results"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing movies.
    
    GET /api/movies/ - List all movies (paginated)
    GET /api/movies/{id}/ - Get movie details
    
    Query parameters:
    - page: Page number (default: 1)
    - page_size: Items per page (default: 20, max: 100)
    - q: Search by title (case-insensitive)
    """
    queryset = Movie.objects.all().order_by('-popularity', '-vote_average')
    permission_classes = [AllowAny]
    pagination_class = MoviePagination
    
    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieListSerializer
    
    def get_queryset(self):
        """
        Optionally filter movies by title using ?q= parameter
        """
        queryset = super().get_queryset()
        
        # Search by title
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(overview__icontains=search_query)
            )
        
        # Filter by genre
        genre = self.request.query_params.get('genre', None)
        if genre:
            queryset = queryset.filter(genres__contains=[genre])
        
        # Filter by year
        year = self.request.query_params.get('year', None)
        if year:
            try:
                queryset = queryset.filter(release_year=int(year))
            except ValueError:
                pass
        
        return queryset

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movies(request):
    """
    Search movies by title, overview, or genres.
    
    Requires JWT authentication.
    
    Query parameters:
    - q: Search query (required, 2-100 characters)
    - page: Page number (default: 1)
    - page_size: Items per page (default: 20, max: 50)
    
    Returns:
    {
        "count": total number of results,
        "next": next page URL or null,
        "previous": previous page URL or null,
        "results": list of matching movies,
        "suggestions": list of top matching titles (max 5)
    }
    """
    # Get and validate search query
    query = request.query_params.get('q', '').strip()
    
    if not query:
        return Response(
            {'error': 'Search query parameter "q" is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(query) < 2:
        return Response(
            {'error': 'Search query must be at least 2 characters long.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(query) > 100:
        return Response(
            {'error': 'Search query must not exceed 100 characters.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Build search query
    queryset = Movie.objects.filter(
        Q(title__icontains=query) |
        Q(overview__icontains=query) |
        Q(genres__icontains=query)
    ).distinct().order_by('-vote_average', '-popularity')
    
    # Get suggestions (top 5 matching titles)
    suggestions = list(
        queryset.values_list('title', flat=True)[:5]
    )
    
    # Apply pagination
    paginator = SearchPagination()
    paginated_results = paginator.paginate_queryset(queryset, request)
    
    # Serialize results
    serializer = MovieSearchSerializer(paginated_results, many=True)
    
    # Build paginated response with suggestions
    response_data = paginator.get_paginated_response(serializer.data).data
    response_data['suggestions'] = suggestions
    
    return Response(response_data, status=status.HTTP_200_OK)