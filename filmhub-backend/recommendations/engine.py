from collections import defaultdict
from typing import List, Set, Dict, Tuple
from movies.models import Movie
from ratings.models import Rating
from watchlist.models import Watchlist


# Scoring weights
GENRE_WEIGHT = 10.0
KEYWORD_WEIGHT = 5.0
QUALITY_WEIGHT = 10.0
POPULARITY_WEIGHT = 1.0


def parse_comma_separated(value: str) -> Set[str]:
    """
    Parse comma-separated string into set
    Example: "28,12,16" -> {"28", "12", "16"}
    """
    if not value:
        return set()
    return {item.strip() for item in str(value).split(',') if item.strip()}


def build_user_profile(user) -> Dict[str, Set[str]]:
    """
    Build user profile from their highly-rated movies (score >= 3)
    
    Returns:
        Dict with 'genres' and 'keywords' sets
    """
    liked_ratings = Rating.objects.filter(
        user=user,
        score__gte=3  # Consider ratings 3+ as "liked"
    ).select_related('movie')
    
    all_genres = set()
    all_keywords = set()
    
    for rating in liked_ratings:
        # Parse genres (could be array or comma-separated string)
        if isinstance(rating.movie.genres, list):
            all_genres.update(rating.movie.genres)
        else:
            all_genres.update(parse_comma_separated(rating.movie.genres))
        
        # Parse keywords (could be array or comma-separated string)
        if isinstance(rating.movie.keywords, list):
            all_keywords.update(rating.movie.keywords)
        else:
            all_keywords.update(parse_comma_separated(rating.movie.keywords))
    
    return {
        'genres': all_genres,
        'keywords': all_keywords,
        'has_preferences': len(all_genres) > 0 or len(all_keywords) > 0
    }


def calculate_recommendation_score(
    user_profile: Dict[str, Set[str]], 
    movie: Movie
) -> float:
    """
    Calculate recommendation score for a movie based on user profile
    
    Score components:
    - Genre overlap: matches * GENRE_WEIGHT
    - Keyword overlap: matches * KEYWORD_WEIGHT  
    - Quality: vote_average * QUALITY_WEIGHT (only if has some overlap)
    - Popularity: rating_count * POPULARITY_WEIGHT (only if has some overlap)
    
    Args:
        user_profile: Dict with 'genres' and 'keywords' sets
        movie: Movie instance
        
    Returns:
        Float score (higher is better match)
    """
    score = 0.0
    
    # Parse movie genres
    if isinstance(movie.genres, list):
        movie_genres = set(movie.genres)
    else:
        movie_genres = parse_comma_separated(movie.genres)
    
    # Parse movie keywords
    if isinstance(movie.keywords, list):
        movie_keywords = set(movie.keywords)
    else:
        movie_keywords = parse_comma_separated(movie.keywords)
    
    # 1. Genre overlap score
    genre_overlap = len(user_profile['genres'].intersection(movie_genres))
    score += genre_overlap * GENRE_WEIGHT
    
    # 2. Keyword overlap score
    keyword_overlap = len(user_profile['keywords'].intersection(movie_keywords))
    score += keyword_overlap * KEYWORD_WEIGHT
    
    # Only add quality/popularity boosts if there's SOME content overlap
    has_overlap = genre_overlap > 0 or keyword_overlap > 0
    
    if has_overlap:
        # 3. Quality boost (TMDB rating) - only for matching content
        if movie.vote_average:
            score += movie.vote_average * QUALITY_WEIGHT
        
        # 4. Popularity boost (local rating count) - only for matching content
        if movie.rating_count:
            score += movie.rating_count * POPULARITY_WEIGHT
    
    return round(score, 2)


def get_cold_start_recommendations(limit: int = 20) -> List[Tuple[Movie, float]]:
    """
    Fallback recommendations for users with no ratings
    
    Returns most popular movies by TMDB vote_average and popularity
    """
    # Get movies ordered by TMDB metrics (not local ratings)
    popular_movies = Movie.objects.filter(
        vote_average__isnull=False
    ).order_by('-popularity', '-vote_average')[:limit]
    
    # Calculate popularity score
    results = []
    for movie in popular_movies:
        # Score based on TMDB metrics
        popularity_score = (movie.popularity or 0) + (movie.vote_average or 0) * 10.0
        results.append((movie, popularity_score))
    
    return results



def get_content_based_recommendations(user, limit: int = 20) -> List[Tuple[Movie, float]]:
    """
    Generate personalized recommendations using content-based filtering
    
    Algorithm:
    1. Build user profile from liked movies (ratings >= 3)
    2. Get candidate movies (not rated, not in watchlist)
    3. Score each candidate by genre/keyword overlap + quality + popularity
    4. Return top N by score
    
    Args:
        user: User instance
        limit: Number of recommendations
        
    Returns:
        List of (Movie, score) tuples sorted by score DESC
    """
    # Step 1: Build user profile
    user_profile = build_user_profile(user)
    
    # Cold-start check
    if not user_profile['has_preferences']:
        return get_cold_start_recommendations(limit)
    
    # Step 2: Get candidate movies (exclude rated and watchlist)
    rated_movie_ids = Rating.objects.filter(
        user=user
    ).values_list('movie_id', flat=True)
    
    watchlist_movie_ids = Watchlist.objects.filter(
        user=user
    ).values_list('movie_id', flat=True)
    
    excluded_ids = set(rated_movie_ids) | set(watchlist_movie_ids)
    
    candidates = Movie.objects.exclude(
        id__in=excluded_ids
    )
    
    # Step 3: Score each candidate
    scored_movies = []
    for movie in candidates:
        score = calculate_recommendation_score(user_profile, movie)
        if score > 0:  # Only include movies with some match
            scored_movies.append((movie, score))
    
    # Step 4: Sort by score and return top N
    scored_movies.sort(key=lambda x: x[1], reverse=True)
    
    return scored_movies[:limit]
