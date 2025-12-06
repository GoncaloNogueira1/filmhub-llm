from rest_framework import serializers
from .models import Watchlist
from movies.models import Movie
from movies.serializers import MovieListSerializer


class WatchlistAddSerializer(serializers.Serializer):
    """Serializer for adding a movie to watchlist"""
    movie_id = serializers.IntegerField()
    
    def validate_movie_id(self, value):
        """Validate that movie exists"""
        try:
            Movie.objects.get(id=value)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("Movie does not exist.")
        return value
    
    def create(self, validated_data):
        """Add movie to user's watchlist (get_or_create to prevent duplicates)"""
        user = self.context['request'].user
        movie_id = validated_data['movie_id']
        movie = Movie.objects.get(id=movie_id)
        
        watchlist_item, created = Watchlist.objects.get_or_create(
            user=user,
            movie=movie
        )
        
        return watchlist_item


class WatchlistItemSerializer(serializers.ModelSerializer):
    """Serializer for watchlist items with movie details"""
    movie = MovieListSerializer(read_only=True)
    
    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'added_at']
        read_only_fields = ['id', 'added_at']
