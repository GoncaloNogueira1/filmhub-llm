from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'age', 'username')
        extra_kwargs = {
            'username': {'required': False},
            'age': {'required': False}
        }
    
    def validate_email(self, value):
        """Check that email is unique"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
    
    def validate_password(self, value):
        """Validate password using Django's password validators"""
        validate_password(value)
        return value
    
    def create(self, validated_data):
        """Create user with hashed password"""
        # Generate username from email if not provided
        if 'username' not in validated_data or not validated_data['username']:
            validated_data['username'] = validated_data['email'].split('@')[0]
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            age=validated_data.get('age', None)
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login with email and password"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        email = attrs.get('email', '').lower()
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError({
                'non_field_errors': ['Must include "email" and "password".']
            })
        
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        
        if not user:
            raise serializers.ValidationError({
                'non_field_errors': ['Invalid email or password.']
            })
        
        if not user.is_active:
            raise serializers.ValidationError({
                'non_field_errors': ['User account is disabled.']
            })
        
        attrs['user'] = user
        return attrs
    
    def create(self, validated_data):
        """Generate JWT tokens for authenticated user"""
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }


# ========== PROFILE SERIALIZERS ==========

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'age',
            'bio',
            'favorite_genres',
            'profile_picture',
            'email_notifications',
            'date_joined',
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'full_name']
    
    def validate_age(self, value):
        """Validate age is reasonable"""
        if value is not None:
            if value < 13:
                raise serializers.ValidationError("You must be at least 13 years old.")
            if value > 120:
                raise serializers.ValidationError("Please enter a valid age.")
        return value
    
    def validate_favorite_genres(self, value):
        """Validate favorite_genres format"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("favorite_genres must be a dictionary.")
        
        # Validate values are between 0 and 1
        for genre_id, weight in value.items():
            if not isinstance(weight, (int, float)):
                raise serializers.ValidationError(
                    f"Genre weight for '{genre_id}' must be a number."
                )
            if not 0 <= weight <= 1:
                raise serializers.ValidationError(
                    f"Genre weight for '{genre_id}' must be between 0 and 1."
                )
        
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile (excludes read-only fields)"""
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'age',
            'bio',
            'favorite_genres',
            'profile_picture',
            'email_notifications',
        ]
    
    def validate_age(self, value):
        """Validate age is reasonable"""
        if value is not None:
            if value < 13:
                raise serializers.ValidationError("You must be at least 13 years old.")
            if value > 120:
                raise serializers.ValidationError("Please enter a valid age.")
        return value
    
    def validate_favorite_genres(self, value):
        """Validate favorite_genres format"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("favorite_genres must be a dictionary.")
        
        for genre_id, weight in value.items():
            if not isinstance(weight, (int, float)):
                raise serializers.ValidationError(
                    f"Genre weight for '{genre_id}' must be a number."
                )
            if not 0 <= weight <= 1:
                raise serializers.ValidationError(
                    f"Genre weight for '{genre_id}' must be between 0 and 1."
                )
        
        return value
    
    def validate_username(self, value):
        """Ensure username is unique (excluding current user)"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

class LogoutSerializer(serializers.Serializer):
    """Serializer for logout - blacklists refresh token"""
    refresh = serializers.CharField(required=False)
    
    def validate(self, attrs):
        """Validate and blacklist refresh token if provided"""
        self.token = attrs.get('refresh')
        return attrs
    
    def save(self, **kwargs):
        """Blacklist the refresh token"""
        if self.token:
            try:
                token = RefreshToken(self.token)
                token.blacklist()
            except TokenError:
                raise serializers.ValidationError('Invalid or expired token')
        return {}