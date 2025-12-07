from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with profile fields"""
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    
    # Profile fields
    bio = models.TextField(blank=True, max_length=500)
    favorite_genres = models.JSONField(default=dict, blank=True)  # {"28": 0.9, "18": 0.6}
    profile_picture = models.URLField(blank=True, max_length=500)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Get user's full name or username"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
