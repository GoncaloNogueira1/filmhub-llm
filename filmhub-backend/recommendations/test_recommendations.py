import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from movies.models import Movie
from ratings.models import Rating
from watchlist.models import Watchlist
from recommendations.engine import (
    build_user_profile,
    calculate_recommendation_score,
    parse_comma_separated
)

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='testuser@test.com',
        username='testuser',
        password='TestPass123'
    )


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def sample_movies():
    """Create diverse sample movies"""
    movies = [
        Movie.objects.create(
            tmdb_id=1001,
            title="Action Sci-Fi Movie",
            genres=["Action", "Science Fiction"],
            keywords=["space", "aliens", "war"],
            vote_average=8.5,
            rating_count=100
        ),
        Movie.objects.create(
            tmdb_id=1002,
            title="Another Action Movie",
            genres=["Action", "Thriller"],
            keywords=["revenge", "martial arts"],
            vote_average=7.8,
            rating_count=50
        ),
        Movie.objects.create(
            tmdb_id=1003,
            title="Romance Drama",
            genres=["Romance", "Drama"],
            keywords=["love", "heartbreak"],
            vote_average=6.5,
            rating_count=30
        ),
        Movie.objects.create(
            tmdb_id=1004,
            title="Space Adventure",
            genres=["Science Fiction", "Adventure"],
            keywords=["space", "exploration", "future"],
            vote_average=8.0,
            rating_count=80
        ),
        Movie.objects.create(
            tmdb_id=1005,
            title="Comedy Movie",
            genres=["Comedy"],
            keywords=["funny", "humor"],
            vote_average=7.0,
            rating_count=40
        ),
    ]
    return movies


@pytest.mark.django_db
class TestRecommendationEngine:
    """Test core recommendation engine functions"""
    
    def test_parse_comma_separated(self):
        """Test parsing comma-separated strings"""
        assert parse_comma_separated("28,12,16") == {"28", "12", "16"}
        assert parse_comma_separated("action, space, aliens") == {"action", "space", "aliens"}
        assert parse_comma_separated("") == set()
        assert parse_comma_separated(None) == set()
    
    def test_build_user_profile_with_ratings(self, user, sample_movies):
        """Test building user profile from ratings"""
        # User likes action and sci-fi
        Rating.objects.create(user=user, movie=sample_movies[0], score=5)
        Rating.objects.create(user=user, movie=sample_movies[1], score=4)
        
        profile = build_user_profile(user)
        
        assert profile['has_preferences'] is True
        assert "Action" in profile['genres']
        assert "Science Fiction" in profile['genres']
        assert "space" in profile['keywords'] or "aliens" in profile['keywords']
    
    def test_build_user_profile_no_ratings(self, user):
        """Test building profile for user with no ratings"""
        profile = build_user_profile(user)
        
        assert profile['has_preferences'] is False
        assert len(profile['genres']) == 0
        assert len(profile['keywords']) == 0
    
    def test_calculate_recommendation_score(self, sample_movies):
        """Test recommendation scoring calculation"""
        user_profile = {
            'genres': {"Action", "Science Fiction"},
            'keywords': {"space", "aliens"}
        }
        
        # Movie with high overlap
        score1 = calculate_recommendation_score(user_profile, sample_movies[0])
        
        # Movie with partial overlap
        score2 = calculate_recommendation_score(user_profile, sample_movies[1])
        
        # Movie with no overlap
        score3 = calculate_recommendation_score(user_profile, sample_movies[2])
        
        # Scores should decrease as overlap decreases
        assert score1 > score2
        assert score2 > score3
        assert score1 > 0


@pytest.mark.django_db
class TestRecommendationsAPI:
    """Test recommendations API endpoint"""
    
    def test_get_recommendations_unauthenticated(self, api_client):
        """Test that authentication is required"""
        url = '/api/recommendations/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_recommendations_cold_start(self, auth_client, sample_movies):
        """Test recommendations for user with no ratings (cold-start)"""
        url = '/api/recommendations/'
        
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['strategy'] == 'cold-start'
        assert response.data['count'] > 0
        assert len(response.data['recommendations']) > 0
        
        # Should return popular movies
        first_rec = response.data['recommendations'][0]
        assert 'id' in first_rec
        assert 'title' in first_rec
        assert 'predicted_score' in first_rec
    
    def test_get_recommendations_with_ratings(self, auth_client, user, sample_movies):
        """Test personalized recommendations based on user ratings"""
        # User likes action/sci-fi movies
        Rating.objects.create(user=user, movie=sample_movies[0], score=5)
        Rating.objects.create(user=user, movie=sample_movies[1], score=4)
        
        url = '/api/recommendations/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['strategy'] == 'content-based'
        assert response.data['count'] > 0
        
        recommendations = response.data['recommendations']
        assert len(recommendations) > 0
        
        # Space Adventure should score high (matches genres + keywords)
        titles = [r['title'] for r in recommendations]
        assert "Space Adventure" in titles
        
        # Romance should score lower or not appear in top results
        top_titles = titles[:3]
        assert "Romance Drama" not in top_titles
    
    def test_excludes_rated_movies(self, auth_client, user, sample_movies):
        """Test that already rated movies are excluded"""
        # Rate all but one movie
        for movie in sample_movies[:4]:
            Rating.objects.create(user=user, movie=movie, score=4)
        
        url = '/api/recommendations/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Rated movies should not appear
        recommended_ids = [r['id'] for r in response.data['recommendations']]
        for movie in sample_movies[:4]:
            assert movie.id not in recommended_ids
    
    def test_excludes_watchlist_movies(self, auth_client, user, sample_movies):
        """Test that watchlist movies are excluded"""
        # Add to watchlist
        Watchlist.objects.create(user=user, movie=sample_movies[0])
        
        # Rate another to trigger content-based
        Rating.objects.create(user=user, movie=sample_movies[1], score=5)
        
        url = '/api/recommendations/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Watchlist movie should not appear
        recommended_ids = [r['id'] for r in response.data['recommendations']]
        assert sample_movies[0].id not in recommended_ids
    
    def test_custom_limit(self, auth_client, sample_movies):
        """Test custom limit parameter"""
        url = '/api/recommendations/?limit=3'
        
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['recommendations']) <= 3
    
    def test_invalid_limit(self, auth_client):
        """Test invalid limit returns 400"""
        url = '/api/recommendations/?limit=500'
        
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_recommendation_score_ordering(self, auth_client, user, sample_movies):
        """Test that recommendations are ordered by score DESC"""
        # User likes action
        Rating.objects.create(user=user, movie=sample_movies[0], score=5)
        
        url = '/api/recommendations/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        recommendations = response.data['recommendations']
        scores = [r['predicted_score'] for r in recommendations]
        
        # Scores should be descending
        assert scores == sorted(scores, reverse=True)
