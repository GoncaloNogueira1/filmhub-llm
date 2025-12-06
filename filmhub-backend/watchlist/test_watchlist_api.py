import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from movies.models import Movie
from watchlist.models import Watchlist

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='watchuser@test.com',
        username='watchuser',
        password='TestPass123'
    )


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def sample_movies():
    return [
        Movie.objects.create(
            tmdb_id=9001,
            title="Test Movie 1",
            genres=["Action"],
            keywords=["test"],
            vote_average=8.0,
            popularity=100
        ),
        Movie.objects.create(
            tmdb_id=9002,
            title="Test Movie 2",
            genres=["Comedy"],
            keywords=["funny"],
            vote_average=7.5,
            popularity=80
        ),
        Movie.objects.create(
            tmdb_id=9003,
            title="Test Movie 3",
            genres=["Drama"],
            keywords=["sad"],
            vote_average=8.5,
            popularity=90
        ),
    ]


@pytest.mark.django_db
class TestAddToWatchlist:
    """Test adding movies to watchlist"""
    
    def test_add_to_watchlist_success(self, auth_client, user, sample_movies):
        """Test adding a movie to watchlist"""
        url = '/api/watchlist/add/'
        data = {'movie_id': sample_movies[0].id}
        
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'watchlist_item' in response.data
        assert response.data['message'] == 'Movie added to watchlist'
        
        # Verify in database
        assert Watchlist.objects.filter(
            user=user,
            movie=sample_movies[0]
        ).exists()
    
    def test_add_duplicate_returns_200(self, auth_client, user, sample_movies):
        """Test adding same movie twice doesn't create duplicate"""
        url = '/api/watchlist/add/'
        data = {'movie_id': sample_movies[0].id}
        
        # Add first time
        response1 = auth_client.post(url, data, format='json')
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Add second time
        response2 = auth_client.post(url, data, format='json')
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data['message'] == 'Movie already in watchlist'
        
        # Verify only one entry exists
        assert Watchlist.objects.filter(
            user=user,
            movie=sample_movies[0]
        ).count() == 1
    
    def test_add_nonexistent_movie_returns_400(self, auth_client):
        """Test adding non-existent movie returns error"""
        url = '/api/watchlist/add/'
        data = {'movie_id': 99999}
        
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'movie_id' in response.data
    
    def test_add_requires_authentication(self, api_client, sample_movies):
        """Test that authentication is required"""
        url = '/api/watchlist/add/'
        data = {'movie_id': sample_movies[0].id}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_add_missing_movie_id(self, auth_client):
        """Test adding without movie_id returns error"""
        url = '/api/watchlist/add/'
        data = {}
        
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'movie_id' in response.data


@pytest.mark.django_db
class TestRemoveFromWatchlist:
    """Test removing movies from watchlist"""
    
    def test_remove_from_watchlist_success(self, auth_client, user, sample_movies):
        """Test removing a movie from watchlist"""
        # Add movie first
        Watchlist.objects.create(user=user, movie=sample_movies[0])
        
        url = f'/api/watchlist/{sample_movies[0].id}/'
        response = auth_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify removed from database
        assert not Watchlist.objects.filter(
            user=user,
            movie=sample_movies[0]
        ).exists()
    
    def test_remove_nonexistent_returns_404(self, auth_client, sample_movies):
        """Test removing movie not in watchlist returns 404"""
        url = f'/api/watchlist/{sample_movies[0].id}/'
        response = auth_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_remove_requires_authentication(self, api_client, sample_movies):
        """Test that authentication is required"""
        url = f'/api/watchlist/{sample_movies[0].id}/'
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_user_can_only_remove_own_watchlist(self, auth_client, sample_movies):
        """Test user cannot remove other user's watchlist items"""
        # Create another user with watchlist
        other_user = User.objects.create_user(
            email='other@test.com',
            username='other',
            password='pass'
        )
        Watchlist.objects.create(user=other_user, movie=sample_movies[0])
        
        # Try to remove other user's watchlist item
        url = f'/api/watchlist/{sample_movies[0].id}/'
        response = auth_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify other user's item still exists
        assert Watchlist.objects.filter(
            user=other_user,
            movie=sample_movies[0]
        ).exists()


@pytest.mark.django_db
class TestGetWatchlist:
    """Test getting user's watchlist"""
    
    def test_get_watchlist_success(self, auth_client, user, sample_movies):
        """Test getting user's watchlist"""
        # Add movies to watchlist
        Watchlist.objects.create(user=user, movie=sample_movies[0])
        Watchlist.objects.create(user=user, movie=sample_movies[1])
        
        url = '/api/watchlist/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'watchlist' in response.data
        assert 'count' in response.data
        assert response.data['count'] == 2
        assert len(response.data['watchlist']) == 2
    
    def test_get_empty_watchlist(self, auth_client):
        """Test getting empty watchlist"""
        url = '/api/watchlist/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
        assert len(response.data['watchlist']) == 0
    
    def test_get_watchlist_requires_authentication(self, api_client):
        """Test that authentication is required"""
        url = '/api/watchlist/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_watchlist_ordered_by_date(self, auth_client, user, sample_movies):
        """Test watchlist is ordered by most recently added"""
        import time
        
        # Add movies with slight delay
        w1 = Watchlist.objects.create(user=user, movie=sample_movies[0])
        time.sleep(0.01)
        w2 = Watchlist.objects.create(user=user, movie=sample_movies[1])
        time.sleep(0.01)
        w3 = Watchlist.objects.create(user=user, movie=sample_movies[2])
        
        url = '/api/watchlist/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Most recent should be first
        titles = [item['movie']['title'] for item in response.data['watchlist']]
        assert titles[0] == sample_movies[2].title
        assert titles[2] == sample_movies[0].title
    
    def test_user_only_sees_own_watchlist(self, auth_client, user, sample_movies):
        """Test user only sees their own watchlist items"""
        # Add to current user's watchlist
        Watchlist.objects.create(user=user, movie=sample_movies[0])
        
        # Create other user with different watchlist
        other_user = User.objects.create_user(
            email='other@test.com',
            username='other',
            password='pass'
        )
        Watchlist.objects.create(user=other_user, movie=sample_movies[1])
        Watchlist.objects.create(user=other_user, movie=sample_movies[2])
        
        url = '/api/watchlist/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1  # Only current user's item
        assert response.data['watchlist'][0]['movie']['title'] == sample_movies[0].title
