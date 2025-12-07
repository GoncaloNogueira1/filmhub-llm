import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='profiletest@test.com',
        username='profileuser',
        password='TestPass123',
        age=25,
        bio='Test bio'
    )


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.mark.django_db
class TestUserProfile:
    """Test user profile endpoints"""
    
    def test_get_profile_success(self, auth_client, user):
        """Test retrieving user profile"""
        url = '/api/auth/profile/'
        
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['username'] == user.username
        assert response.data['age'] == 25
        assert response.data['bio'] == 'Test bio'
        assert 'id' in response.data
        assert 'date_joined' in response.data
    
    def test_get_profile_requires_auth(self, api_client):
        """Test that authentication is required"""
        url = '/api/auth/profile/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_profile_success(self, auth_client, user):
        """Test updating user profile"""
        url = '/api/auth/profile/'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'bio': 'Updated bio',
            'favorite_genres': {'28': 0.9, '18': 0.6},
            'email_notifications': False
        }
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Profile updated successfully'
        assert response.data['profile']['first_name'] == 'John'
        assert response.data['profile']['last_name'] == 'Doe'
        assert response.data['profile']['age'] == 30
        assert response.data['profile']['bio'] == 'Updated bio'
        assert response.data['profile']['favorite_genres'] == {'28': 0.9, '18': 0.6}
        assert response.data['profile']['email_notifications'] is False
        
        # Verify in database
        user.refresh_from_db()
        assert user.first_name == 'John'
        assert user.age == 30
    
    def test_partial_update_profile(self, auth_client, user):
        """Test partial update (only some fields)"""
        url = '/api/auth/profile/'
        data = {'bio': 'New bio only'}
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['profile']['bio'] == 'New bio only'
        
        # Other fields unchanged
        assert response.data['profile']['age'] == 25
    
    def test_update_favorite_genres(self, auth_client):
        """Test updating favorite genres"""
        url = '/api/auth/profile/'
        data = {
            'favorite_genres': {
                '28': 0.9,  # Action
                '18': 0.7,  # Drama
                '878': 0.8  # Sci-Fi
            }
        }
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['profile']['favorite_genres'] == data['favorite_genres']
    
    def test_invalid_age_too_young(self, auth_client):
        """Test age validation (too young)"""
        url = '/api/auth/profile/'
        data = {'age': 10}
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'age' in response.data
    
    def test_invalid_age_too_old(self, auth_client):
        """Test age validation (too old)"""
        url = '/api/auth/profile/'
        data = {'age': 150}
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'age' in response.data
    
    def test_invalid_genre_preferences_format(self, auth_client):
        """Test favorite_genres validation (invalid format)"""
        url = '/api/auth/profile/'
        data = {'favorite_genres': 'invalid'}
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'favorite_genres' in response.data
    
    def test_invalid_genre_weight_out_of_range(self, auth_client):
        """Test genre weight validation (out of range)"""
        url = '/api/auth/profile/'
        data = {'favorite_genres': {'28': 1.5}}
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'favorite_genres' in response.data
    
    def test_cannot_update_email(self, auth_client, user):
        """Test that email cannot be updated"""
        url = '/api/auth/profile/'
        data = {'email': 'newemail@test.com'}
        
        response = auth_client.patch(url, data, format='json')
        
        # Email should not change
        user.refresh_from_db()
        assert user.email == 'profiletest@test.com'
    
    def test_update_username_success(self, auth_client, user):
        """Test updating username"""
        url = '/api/auth/profile/'
        data = {'username': 'newusername'}
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['profile']['username'] == 'newusername'
    
    def test_update_username_duplicate(self, auth_client, user):
        """Test updating to existing username fails"""
        # Create another user
        User.objects.create_user(
            email='other@test.com',
            username='existinguser',
            password='pass'
        )
        
        url = '/api/auth/profile/'
        data = {'username': 'existinguser'}
        
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data


@pytest.mark.django_db
class TestUserStatistics:
    """Test user statistics endpoint"""
    
    def test_get_statistics(self, auth_client, user):
        """Test getting user statistics"""
        from movies.models import Movie
        from ratings.models import Rating
        
        # Create movies and ratings
        movie1 = Movie.objects.create(
            tmdb_id=8001,
            title="Action Movie",
            genres=["Action", "Thriller"],
            vote_average=8.0
        )
        movie2 = Movie.objects.create(
            tmdb_id=8002,
            title="Action Movie 2",
            genres=["Action", "Adventure"],
            vote_average=7.5
        )
        
        Rating.objects.create(user=user, movie=movie1, score=5)
        Rating.objects.create(user=user, movie=movie2, score=4)
        
        url = '/api/auth/profile/stats/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_ratings'] == 2
        assert response.data['average_rating'] == 4.5
        assert len(response.data['top_genres']) > 0
    
    def test_statistics_requires_auth(self, api_client):
        """Test that authentication is required"""
        url = '/api/auth/profile/stats/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
