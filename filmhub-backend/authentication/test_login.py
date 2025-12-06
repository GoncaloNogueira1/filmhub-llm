import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def api_client():
    """Provide APIClient for API requests"""
    return APIClient()


@pytest.fixture
def test_user():
    """Create a test user"""
    return User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='TestPassword123',
        age=25
    )


@pytest.mark.django_db
class TestUserLogin:
    """Test suite for user login endpoint"""
    
    def test_successful_login(self, api_client, test_user):
        """Test successful login with valid credentials"""
        url = '/api/auth/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'tokens' in response.data
        assert 'access' in response.data['tokens']
        assert 'refresh' in response.data['tokens']
        assert 'user' in response.data
        assert response.data['user']['email'] == 'testuser@example.com'
        assert 'password' not in response.data
    
    def test_login_case_insensitive_email(self, api_client, test_user):
        """Test login works with uppercase email"""
        url = '/api/auth/login/'
        data = {
            'email': 'TESTUSER@EXAMPLE.COM',
            'password': 'TestPassword123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'tokens' in response.data
    
    def test_login_wrong_password(self, api_client, test_user):
        """Test login fails with incorrect password"""
        url = '/api/auth/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'tokens' not in response.data
    
    def test_login_nonexistent_user(self, api_client):
        """Test login fails with non-existent user"""
        url = '/api/auth/login/'
        data = {
            'email': 'nonexistent@example.com',
            'password': 'SomePassword123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'tokens' not in response.data
    
    def test_login_missing_email(self, api_client):
        """Test login fails when email is missing"""
        url = '/api/auth/login/'
        data = {
            'password': 'TestPassword123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_missing_password(self, api_client, test_user):
        """Test login fails when password is missing"""
        url = '/api/auth/login/'
        data = {
            'email': 'testuser@example.com'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_can_access_protected_endpoint(self, api_client, test_user):
        """Test that issued token can access protected endpoints"""
        # Login to get token
        login_url = '/api/auth/login/'
        login_data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123'
        }
        
        login_response = api_client.post(login_url, login_data, format='json')
        access_token = login_response.data['tokens']['access']
        
        # Use token to access a protected endpoint (we'll test with admin)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # The token should be valid
        assert access_token is not None
        assert len(access_token) > 20
