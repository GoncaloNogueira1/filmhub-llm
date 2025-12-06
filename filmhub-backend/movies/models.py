from django.db import models
from django.contrib.postgres.fields import ArrayField


class Movie(models.Model):
    """Movie model with TMDB integration"""
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    poster_url = models.URLField(max_length=500, blank=True)
    backdrop_url = models.URLField(max_length=500, blank=True)
    
    # Content-based filtering fields
    genres = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )
    keywords = ArrayField(  # ← ADICIONAR ESTE CAMPO
        models.CharField(max_length=100),
        default=list,
        blank=True
    )
    
    # Quality/popularity metrics
    vote_average = models.FloatField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(default=0)  # ← ADICIONAR ESTE CAMPO (local ratings)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity', '-vote_average']
        indexes = [
            models.Index(fields=['tmdb_id']),
            models.Index(fields=['-popularity']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
