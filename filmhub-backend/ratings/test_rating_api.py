import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from movies.models import Movie
from ratings.models import Rating

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user1():
    return User.objects.create_user(
        email='user1@test.com',
        username='user1',
        password='TestPass123'
    )


@pytest.fixture
def user2():
    return User.objects.create_user(
        email='user2@test.com',
        username='user2',
        password='TestPass123'
    )


@pytest.fixture
def auth_client1(user1):
    """Create authenticated client for user1"""
    client = APIClient()
    refresh = RefreshToken.for_user(user1)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def auth_client2(user2):
    """Create authenticated client for user2"""
    client = APIClient()  # ← Nova instância separada
    refresh = RefreshToken.for_user(user2)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

@pytest.fixture
def sample_movie():
    """Create a sample movie for testing"""
    return Movie.objects.create(
        tmdb_id=5001,
        title="Test Movie",
        overview="A great test movie",
        release_year=2024,
        vote_average=8.5,
        popularity=100.0
    )

@pytest.mark.django_db
class TestRateMovie:
    """Test creating and updating ratings"""
    
    def test_create_rating_success(self, auth_client1, sample_movie, user1):
        """Test creating a new rating"""
        url = f'/api/movies/{sample_movie.id}/rate/'
        data = {'score': 5, 'comment': 'Excellent movie!'}
        
        response = auth_client1.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['score'] == 5
        assert response.data['comment'] == 'Excellent movie!'
        assert Rating.objects.filter(user=user1, movie=sample_movie).count() == 1
    
    def test_create_rating_without_comment(self, auth_client1, sample_movie):
        """Test creating rating without optional comment"""
        url = f'/api/movies/{sample_movie.id}/rate/'
        data = {'score': 4}
        
        response = auth_client1.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['score'] == 4
        assert response.data['comment'] == ''
    
    def test_update_existing_rating(self, auth_client1, sample_movie, user1):
        """Test updating an existing rating"""
        url = f'/api/movies/{sample_movie.id}/rate/'
        
        # Create initial rating
        response1 = auth_client1.post(url, {'score': 3}, format='json')
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Update rating
        response2 = auth_client1.post(url, {'score': 5, 'comment': 'Changed my mind!'}, format='json')
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data['score'] == 5
        assert response2.data['comment'] == 'Changed my mind!'
        
        # Verify only one rating exists
        assert Rating.objects.filter(user=user1, movie=sample_movie).count() == 1
    
    def test_rating_requires_authentication(self, api_client, sample_movie):
        """Test that rating requires authentication"""
        url = f'/api/movies/{sample_movie.id}/rate/'
        data = {'score': 5}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_invalid_score_too_low(self, auth_client1, sample_movie):
        """Test score below 1 is rejected"""
        url = f'/api/movies/{sample_movie.id}/rate/'
        data = {'score': 0}
        
        response = auth_client1.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'score' in response.data
    
    def test_invalid_score_too_high(self, auth_client1, sample_movie):
        """Test score above 5 is rejected"""
        url = f'/api/movies/{sample_movie.id}/rate/'
        data = {'score': 6}
        
        response = auth_client1.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'score' in response.data
    
    def test_missing_score(self, auth_client1, sample_movie):
        """Test missing score field"""
        url = f'/api/movies/{sample_movie.id}/rate/'
        data = {'comment': 'Great!'}
        
        response = auth_client1.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'score' in response.data
    
    def test_rating_nonexistent_movie(self, auth_client1):
        """Test rating a non-existent movie returns 404"""
        url = '/api/movies/99999/rate/'
        data = {'score': 5}
        
        response = auth_client1.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_multiple_users_can_rate_same_movie(self, auth_client1, auth_client2, sample_movie, user1, user2):
        """Test different users can rate the same movie"""
        url = f'/api/movies/{sample_movie.id}/rate/'
        
        response1 = auth_client1.post(url, {'score': 5}, format='json')
        response2 = auth_client2.post(url, {'score': 3}, format='json')
        
        assert response1.status_code == status.HTTP_201_CREATED
        assert response2.status_code == status.HTTP_201_CREATED
        assert Rating.objects.filter(movie=sample_movie).count() == 2


@pytest.mark.django_db
class TestMovieRatingAggregate:
    """Test aggregate rating endpoint"""
    
    def test_get_aggregate_with_ratings(self, api_client, sample_movie, user1, user2):
        """Test getting aggregate ratings"""
        # Create ratings
        Rating.objects.create(user=user1, movie=sample_movie, score=5)
        Rating.objects.create(user=user2, movie=sample_movie, score=3)
        
        url = f'/api/movies/{sample_movie.id}/rating/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['movie_id'] == sample_movie.id
        assert response.data['average_score'] == 4.0  # (5+3)/2
        assert response.data['ratings_count'] == 2
    
    def test_get_aggregate_no_ratings(self, api_client, sample_movie):
        """Test aggregate for movie with no ratings"""
        url = f'/api/movies/{sample_movie.id}/rating/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['average_score'] == 0.0
        assert response.data['ratings_count'] == 0
    
    def test_aggregate_no_auth_required(self, api_client, sample_movie):
        """Test aggregate endpoint is public"""
        url = f'/api/movies/{sample_movie.id}/rating/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_aggregate_nonexistent_movie(self, api_client):
        """Test aggregate for non-existent movie returns 404"""
        url = '/api/movies/99999/rating/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_aggregate_rounds_to_one_decimal(self, api_client, sample_movie, user1, user2):
        """Test average is rounded to 1 decimal place"""
        # Create test user
        user3 = User.objects.create_user(email='user3@test.com', username='user3', password='pass')
        
        # Ratings: 5, 4, 3 → average = 4.0
        Rating.objects.create(user=user1, movie=sample_movie, score=5)
        Rating.objects.create(user=user2, movie=sample_movie, score=4)
        Rating.objects.create(user=user3, movie=sample_movie, score=3)
        
        url = f'/api/movies/{sample_movie.id}/rating/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['average_score'] == 4.0
