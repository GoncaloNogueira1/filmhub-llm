import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='logouttest@test.com',
        username='logoutuser',
        password='TestPass123'
    )


@pytest.fixture
def auth_tokens(user):
    """Generate tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


@pytest.fixture
def auth_client(api_client, auth_tokens):
    """Authenticated client"""
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_tokens["access"]}')
    return api_client


@pytest.mark.django_db
class TestLogout:
    """Test logout functionality"""
    
    def test_logout_success_with_refresh_token(self, auth_client, auth_tokens):
        """Test logout with refresh token blacklists it"""
        url = '/api/auth/logout/'
        data = {'refresh': auth_tokens['refresh']}
        
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_205_RESET_CONTENT
        assert 'message' in response.data
        assert response.data['message'] == 'Successfully logged out'
        
        # Verify token is blacklisted
        outstanding_token = OutstandingToken.objects.filter(
            token=auth_tokens['refresh']
        ).first()
        
        assert outstanding_token is not None
        assert BlacklistedToken.objects.filter(
            token=outstanding_token
        ).exists()
    
    def test_logout_without_refresh_token(self, auth_client):
        """Test logout without providing refresh token still succeeds"""
        url = '/api/auth/logout/'
        data = {}
        
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_205_RESET_CONTENT
        assert 'message' in response.data
        assert 'Logged out' in response.data['message']
    
    def test_logout_with_invalid_refresh_token(self, auth_client):
        """Test logout with invalid refresh token returns error"""
        url = '/api/auth/logout/'
        data = {'refresh': 'invalid_token_here'}
        
        response = auth_client.post(url, data, format='json')
        
        # Should still return 205 or handle gracefully
        # Depending on implementation preference
        assert response.status_code in [
            status.HTTP_205_RESET_CONTENT,
            status.HTTP_400_BAD_REQUEST
        ]
    
    def test_logout_requires_authentication(self, api_client, auth_tokens):
        """Test that logout requires authentication"""
        url = '/api/auth/logout/'
        data = {'refresh': auth_tokens['refresh']}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_cannot_use_blacklisted_token(self, auth_client, auth_tokens, user):
        """Test that blacklisted refresh token cannot be used"""
        # Logout to blacklist token
        logout_url = '/api/auth/logout/'
        auth_client.post(logout_url, {'refresh': auth_tokens['refresh']}, format='json')
        
        # Try to refresh with blacklisted token
        refresh_url = '/api/auth/token/refresh/'
        api_client = APIClient()  # New client without auth
        
        response = api_client.post(
            refresh_url,
            {'refresh': auth_tokens['refresh']},
            format='json'
        )
        
        # Should fail because token is blacklisted
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_access_token_still_works_after_logout(self, auth_client, auth_tokens):
        """
        Test that access token still works after logout
        (This is expected JWT behavior - stateless)
        """
        # Logout
        logout_url = '/api/auth/logout/'
        auth_client.post(logout_url, {'refresh': auth_tokens['refresh']}, format='json')
        
        # Try to access protected endpoint with access token
        profile_url = '/api/auth/profile/'
        response = auth_client.get(profile_url)
        
        # Access token should still work until it expires
        # This is normal JWT behavior - they are stateless
        assert response.status_code == status.HTTP_200_OK
    
    def test_multiple_logouts_same_token(self, auth_client, auth_tokens):
        """Test logging out twice with same token"""
        url = '/api/auth/logout/'
        data = {'refresh': auth_tokens['refresh']}
        
        # First logout
        response1 = auth_client.post(url, data, format='json')
        assert response1.status_code == status.HTTP_205_RESET_CONTENT
        
        # Second logout with same token
        response2 = auth_client.post(url, data, format='json')
        
        # Should handle gracefully
        assert response2.status_code in [
            status.HTTP_205_RESET_CONTENT,
            status.HTTP_400_BAD_REQUEST
        ]


@pytest.mark.django_db
class TestLogoutIntegration:
    """Test logout integration with login flow"""
    
    def test_login_logout_login_flow(self, api_client, user):
        """Test complete login -> logout -> login flow"""
        # Login
        login_url = '/api/auth/login/'
        login_data = {'email': user.email, 'password': 'TestPass123'}
        
        login_response = api_client.post(login_url, login_data, format='json')
        assert login_response.status_code == status.HTTP_200_OK
        
        tokens = login_response.data['tokens']
        
        # Authenticate
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        # Logout
        logout_url = '/api/auth/logout/'
        logout_response = api_client.post(
            logout_url,
            {'refresh': tokens['refresh']},
            format='json'
        )
        assert logout_response.status_code == status.HTTP_205_RESET_CONTENT
        
        # Login again
        login_response2 = api_client.post(login_url, login_data, format='json')
        assert login_response2.status_code == status.HTTP_200_OK
        
        # New tokens should be different
        new_tokens = login_response2.data['tokens']
        assert new_tokens['refresh'] != tokens['refresh']
