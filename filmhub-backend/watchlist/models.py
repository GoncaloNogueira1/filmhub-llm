from django.db import models
from django.contrib.auth import get_user_model
from movies.models import Movie

User = get_user_model()


class Watchlist(models.Model):
    """User's movie watchlist"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='watchlist'
    )
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE, 
        related_name='watchlisted_by'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie')  # Prevent duplicates
        ordering = ['-added_at']
        indexes = [
            models.Index(fields=['user', '-added_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.movie.title}"
