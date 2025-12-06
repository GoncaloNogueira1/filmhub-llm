from rest_framework import serializers
from movies.models import Movie


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for recommendation results with predicted score"""
    predicted_score = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'genres',
            'keywords',
            'vote_average',
            'poster_url',
            'release_year',
            'predicted_score'
        ]
