from rest_framework import serializers
from .models import Movie


class MovieListSerializer(serializers.ModelSerializer):
    """Serializer for movie list view (minimal fields)"""
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'tmdb_id',
            'title',
            'release_year',
            'poster_url',
            'vote_average',
            'genres',
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer for movie detail view (all fields)"""
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'tmdb_id',
            'title',
            'overview',
            'release_year',
            'poster_url',
            'backdrop_url',
            'genres',
            'vote_average',
            'popularity',
            'created_at',
            'updated_at',
        ]
        
class MovieSearchSerializer(serializers.ModelSerializer):
    """Serializer for search results"""
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'tmdb_id',
            'title',
            'overview',
            'release_year',
            'poster_url',
            'genres',
            'vote_average',
        ]