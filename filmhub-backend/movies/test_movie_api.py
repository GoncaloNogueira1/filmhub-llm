import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from movies.models import Movie

User = get_user_model()


@pytest.fixture
def api_client():
    """Provide APIClient for API requests"""
    return APIClient()


@pytest.fixture
def sample_movies():
    """Create sample movies for testing"""
    movies = [
        Movie.objects.create(
            tmdb_id=1001,
            title="The Matrix",
            overview="A computer hacker learns about the true nature of reality.",
            release_year=1999,
            poster_url="https://image.tmdb.org/t/p/w500/poster1.jpg",
            genres=["Action", "Science Fiction"],
            vote_average=8.7,
            popularity=85.5
        ),
        Movie.objects.create(
            tmdb_id=1002,
            title="The Matrix Reloaded",
            overview="Neo and the rebel leaders face the Machine Army.",
            release_year=2003,
            poster_url="https://image.tmdb.org/t/p/w500/poster2.jpg",
            genres=["Action", "Science Fiction"],
            vote_average=7.2,
            popularity=65.3
        ),
        Movie.objects.create(
            tmdb_id=1003,
            title="Inception",
            overview="A thief who steals corporate secrets through dream-sharing.",
            release_year=2010,
            poster_url="https://image.tmdb.org/t/p/w500/poster3.jpg",
            genres=["Action", "Thriller", "Science Fiction"],
            vote_average=8.8,
            popularity=90.2
        ),
        Movie.objects.create(
            tmdb_id=1004,
            title="Interstellar",
            overview="A team of explorers travel through a wormhole in space.",
            release_year=2014,
            poster_url="https://image.tmdb.org/t/p/w500/poster4.jpg",
            genres=["Drama", "Science Fiction"],
            vote_average=8.6,
            popularity=88.7
        ),
    ]
    return movies


@pytest.mark.django_db
class TestMovieList:
    """Test suite for movie list endpoint"""
    
    def test_list_movies_success(self, api_client, sample_movies):
        """Test getting list of movies"""
        url = '/api/movies/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data
        assert 'next' in response.data
        assert 'previous' in response.data
        assert response.data['count'] == 4
        assert len(response.data['results']) == 4
    
    def test_list_movies_empty(self, api_client):
        """Test getting empty movie list"""
        url = '/api/movies/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
        assert len(response.data['results']) == 0
    
    def test_list_movies_pagination(self, api_client, sample_movies):
        """Test pagination works correctly"""
        url = '/api/movies/?page_size=2'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        assert response.data['count'] == 4
        assert response.data['next'] is not None
        assert response.data['previous'] is None
    
    def test_list_movies_second_page(self, api_client, sample_movies):
        """Test getting second page"""
        url = '/api/movies/?page=2&page_size=2'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        assert response.data['previous'] is not None
    
    def test_list_movies_page_size_limit(self, api_client, sample_movies):
        """Test that page_size has a maximum limit"""
        url = '/api/movies/?page_size=1000'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Max page_size is 100, so should return all 4 movies
        assert len(response.data['results']) == 4
    
    def test_search_movies_by_title(self, api_client, sample_movies):
        """Test searching movies by title"""
        url = '/api/movies/?q=Matrix'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        titles = [movie['title'] for movie in response.data['results']]
        assert 'The Matrix' in titles
        assert 'The Matrix Reloaded' in titles
    
    def test_search_movies_case_insensitive(self, api_client, sample_movies):
        """Test search is case-insensitive"""
        url = '/api/movies/?q=inception'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Inception'
    
    def test_search_movies_no_results(self, api_client, sample_movies):
        """Test search with no matching results"""
        url = '/api/movies/?q=NonExistentMovie'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
    
    def test_filter_by_genre(self, api_client, sample_movies):
        """Test filtering by genre"""
        url = '/api/movies/?genre=Thriller'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Inception'
    
    def test_filter_by_year(self, api_client, sample_movies):
        """Test filtering by release year"""
        url = '/api/movies/?year=2010'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Inception'


@pytest.mark.django_db
class TestMovieDetail:
    """Test suite for movie detail endpoint"""
    
    def test_get_movie_detail_success(self, api_client, sample_movies):
        """Test getting details of a single movie"""
        movie = sample_movies[0]
        url = f'/api/movies/{movie.id}/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == movie.id
        assert response.data['title'] == movie.title
        assert response.data['overview'] == movie.overview
        assert response.data['release_year'] == movie.release_year
        assert response.data['tmdb_id'] == movie.tmdb_id
        assert 'genres' in response.data
        assert 'poster_url' in response.data
        assert 'backdrop_url' in response.data
        assert 'vote_average' in response.data
    
    def test_get_movie_detail_not_found(self, api_client):
        """Test getting details of non-existent movie returns 404"""
        url = '/api/movies/99999/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_movie_detail_has_more_fields_than_list(self, api_client, sample_movies):
        """Test that detail view returns more fields than list view"""
        movie = sample_movies[0]
        
        # Get list
        list_response = api_client.get('/api/movies/')
        list_fields = set(list_response.data['results'][0].keys())
        
        # Get detail
        detail_response = api_client.get(f'/api/movies/{movie.id}/')
        detail_fields = set(detail_response.data.keys())
        
        # Detail should have more fields
        assert len(detail_fields) > len(list_fields)
        assert 'overview' in detail_fields
        assert 'backdrop_url' in detail_fields


@pytest.mark.django_db
class TestMoviePermissions:
    """Test that movie endpoints are public"""
    
    def test_list_movies_no_auth_required(self, api_client, sample_movies):
        """Test that authentication is not required for list"""
        url = '/api/movies/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_detail_movies_no_auth_required(self, api_client, sample_movies):
        """Test that authentication is not required for detail"""
        movie = sample_movies[0]
        url = f'/api/movies/{movie.id}/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
