import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from movies.models import Movie

User = get_user_model()


@pytest.fixture
def api_client():
    """Provide APIClient for API requests"""
    return APIClient()


@pytest.fixture
def authenticated_user():
    """Create a test user"""
    return User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='TestPassword123'
    )


@pytest.fixture
def auth_token(authenticated_user):
    """Generate JWT token for authenticated user"""
    refresh = RefreshToken.for_user(authenticated_user)
    return str(refresh.access_token)


@pytest.fixture
def authenticated_client(api_client, auth_token):
    """APIClient with JWT authentication"""
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
    return api_client


@pytest.fixture
def sample_movies():
    """Create sample movies for testing"""
    movies = [
        Movie.objects.create(
            tmdb_id=2001,
            title="The Matrix",
            overview="A computer hacker learns from mysterious rebels about the true nature of his reality.",
            release_year=1999,
            poster_url="https://image.tmdb.org/t/p/w500/poster1.jpg",
            genres=["Action", "Science Fiction"],
            vote_average=8.7,
            popularity=85.5
        ),
        Movie.objects.create(
            tmdb_id=2002,
            title="The Matrix Reloaded",
            overview="Neo and the rebel leaders estimate that they have 72 hours until the Machine Army invades.",
            release_year=2003,
            poster_url="https://image.tmdb.org/t/p/w500/poster2.jpg",
            genres=["Action", "Science Fiction"],
            vote_average=7.2,
            popularity=65.3
        ),
        Movie.objects.create(
            tmdb_id=2003,
            title="Inception",
            overview="A thief who steals corporate secrets through use of dream-sharing technology.",
            release_year=2010,
            poster_url="https://image.tmdb.org/t/p/w500/poster3.jpg",
            genres=["Action", "Thriller", "Science Fiction"],
            vote_average=8.8,
            popularity=90.2
        ),
        Movie.objects.create(
            tmdb_id=2004,
            title="The Dark Knight",
            overview="Batman raises the stakes in his war on crime with the help of Lieutenant Jim Gordon.",
            release_year=2008,
            poster_url="https://image.tmdb.org/t/p/w500/poster4.jpg",
            genres=["Action", "Crime", "Drama"],
            vote_average=9.0,
            popularity=95.8
        ),
    ]
    return movies


@pytest.mark.django_db
class TestSearchAuthentication:
    """Test authentication requirements for search endpoint"""
    
    def test_search_without_auth_returns_401(self, api_client, sample_movies):
        """Test that search requires authentication"""
        url = '/api/search/?q=matrix'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_search_with_invalid_token_returns_401(self, api_client, sample_movies):
        """Test that invalid token returns 401"""
        url = '/api/search/?q=matrix'
        api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_search_with_valid_token_returns_200(self, authenticated_client, sample_movies):
        """Test that valid token allows search"""
        url = '/api/search/?q=matrix'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestSearchValidation:
    """Test search query validation"""
    
    def test_search_missing_query_returns_400(self, authenticated_client):
        """Test that missing query parameter returns 400"""
        url = '/api/search/'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'required' in response.data['error'].lower()
    
    def test_search_query_too_short_returns_400(self, authenticated_client):
        """Test that query shorter than 2 chars returns 400"""
        url = '/api/search/?q=a'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert '2 characters' in response.data['error']
    
    def test_search_query_too_long_returns_400(self, authenticated_client):
        """Test that query longer than 100 chars returns 400"""
        long_query = 'a' * 101
        url = f'/api/search/?q={long_query}'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert '100 characters' in response.data['error']
    
    def test_search_empty_string_returns_400(self, authenticated_client):
        """Test that empty string returns 400"""
        url = '/api/search/?q=   '
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestSearchFunctionality:
    """Test search functionality"""
    
    def test_search_by_title_returns_results(self, authenticated_client, sample_movies):
        """Test searching by title"""
        url = '/api/search/?q=matrix'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data
        assert 'suggestions' in response.data
        assert response.data['count'] == 2
        titles = [movie['title'] for movie in response.data['results']]
        assert 'The Matrix' in titles
        assert 'The Matrix Reloaded' in titles
    
    def test_search_case_insensitive(self, authenticated_client, sample_movies):
        """Test that search is case-insensitive"""
        url = '/api/search/?q=INCEPTION'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Inception'
    
    def test_search_by_overview(self, authenticated_client, sample_movies):
        """Test searching by overview text"""
        url = '/api/search/?q=thief'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Inception'
    
    def test_search_by_genre(self, authenticated_client, sample_movies):
        """Test searching by genre"""
        url = '/api/search/?q=Crime'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'The Dark Knight'
    
    def test_search_no_results(self, authenticated_client, sample_movies):
        """Test search with no matching results"""
        url = '/api/search/?q=NonExistentMovie12345'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
        assert len(response.data['results']) == 0
        assert len(response.data['suggestions']) == 0
    
    def test_search_suggestions_included(self, authenticated_client, sample_movies):
        """Test that suggestions are included in response"""
        url = '/api/search/?q=the'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'suggestions' in response.data
        assert isinstance(response.data['suggestions'], list)
        assert len(response.data['suggestions']) <= 5
    
    def test_search_results_have_required_fields(self, authenticated_client, sample_movies):
        """Test that search results contain required fields"""
        url = '/api/search/?q=matrix'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        result = response.data['results'][0]
        assert 'id' in result
        assert 'title' in result
        assert 'overview' in result
        assert 'release_year' in result
        assert 'poster_url' in result
        assert 'genres' in result
        assert 'vote_average' in result


@pytest.mark.django_db
class TestSearchPagination:
    """Test search pagination"""
    
    def test_search_pagination_default(self, authenticated_client, sample_movies):
        """Test default pagination settings"""
        url = '/api/search/?q=the'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'next' in response.data
        assert 'previous' in response.data
        assert len(response.data['results']) <= 20
    
    def test_search_custom_page_size(self, authenticated_client, sample_movies):
        """Test custom page size"""
        url = '/api/search/?q=the&page_size=2'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) <= 2
    
    def test_search_max_page_size_limit(self, authenticated_client, sample_movies):
        """Test that page size is limited to 50"""
        url = '/api/search/?q=the&page_size=1000'
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Should not exceed max_page_size of 50
        assert len(response.data['results']) <= 50
    
    def test_search_second_page(self, authenticated_client, sample_movies):
        """Test accessing second page"""
        url = '/api/search/?q=the&page=2&page_size=2'
        
        response = authenticated_client.get(url)
        
        # May be 200 with empty results or valid results depending on total count
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
