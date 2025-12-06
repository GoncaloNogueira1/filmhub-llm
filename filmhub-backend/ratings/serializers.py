from rest_framework import serializers
from .models import Rating
from movies.models import Movie


class RatingCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating ratings"""
    
    class Meta:
        model = Rating
        fields = ['score', 'comment']
    
    def validate_score(self, value):
        """Validate score is between 1 and 5"""
        if not isinstance(value, int):
            raise serializers.ValidationError("Score must be an integer.")
        if value < 1 or value > 5:
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value
    
    def create(self, validated_data):
        """Create rating with user and movie from context"""
        user = self.context['request'].user
        movie = self.context['movie']
        
        rating, created = Rating.objects.update_or_create(
            user=user,
            movie=movie,
            defaults=validated_data
        )
        return rating


class RatingDetailSerializer(serializers.ModelSerializer):
    """Serializer for rating details including user info"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    
    class Meta:
        model = Rating
        fields = [
            'id',
            'user_email',
            'movie_title',
            'score',
            'comment',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MovieRatingAggregateSerializer(serializers.Serializer):
    """Serializer for movie rating aggregates"""
    movie_id = serializers.IntegerField()
    average_score = serializers.FloatField()
    ratings_count = serializers.IntegerField()
