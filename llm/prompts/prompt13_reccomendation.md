ROLE: Senior Django developer specializing in local recommendation systems for FilmHub.

TASK: Implement UC7 – GET /api/recommendations endpoint that works 100% offline using only the local Movie, Rating, and Watchlist tables, replicating the content-based logic from the traditional version but without TMDB API calls.

CONSTRAINTS:
- Models: User, Movie (fields: id, title, genres="28,12,16", keywords="action,space,aliens", average_rating, rating_count), Rating (user, movie, score 1-5), Watchlist (user, movie).
- Endpoint: GET /api/recommendations (JWT authentication required).
- Return top 20 movies the user has NOT rated AND NOT in watchlist.
- Each recommendation includes: id, title, genres, keywords, predicted_score.
- Cold-start: if user has 0 ratings, return top 20 movies by rating_count + average_rating.
- Use Django ORM only (no external APIs, no raw SQL).

REASONING STEPS (Chain-of-Thought):
1. Get authenticated user ratings with score >= 3.
2. From liked movies, extract genres (split comma-separated string → set) and keywords (split → set) → build user profile.
3. Query candidate movies: exclude movies already rated by user OR in user's watchlist.
4. For each candidate movie:
   - Calculate genre overlap: len(user_liked_genres.intersection(movie_genres)) * GENRE_POINTS (e.g. 10)
   - Calculate keyword overlap: len(user_liked_keywords.intersection(movie_keywords)) * KEYWORD_POINTS (e.g. 5)  
   - Add popularity boost: (average_rating * 10) + rating_count
   - Total score = genre_score + keyword_score + popularity_score
5. Sort candidates by total score DESC → take top 20.
6. Cold-start fallback: if no liked ratings, sort all movies by (rating_count * 10 + average_rating * 100) DESC → top 20.
7. Return JSON: [{"id": 123, "title": "...", "genres": "...", "keywords": "...", "predicted_score": 85.5}, ...]

EXAMPLES:
Example 1 – user liked action/sci-fi movies:
User profile: genres={"28","878"}, keywords={"action","space"}
Movie1: genres="28,12", keywords="action,robots" → high genre+keyword score
Movie2: genres="99", keywords="romance" → low score

Example 2 – cold-start user:
No ratings → return globally most popular movies (high rating_count + average_rating).

OUTPUT:
- views.py: GET recommendations view with JWT authentication.
- Helper function: calculate_recommendation_score(user_profile, movie) → float score.
- serializers.py: RecommendationSerializer.
- urls.py: route for /api/recommendations.
- tests (pytest + APIClient):
  - User with ratings → correct genre/keyword scoring
  - User with no ratings → cold-start fallback works  
  - Already rated/watchlist movies excluded
  - Unauthenticated → 401

EVALUATION:
- All tests pass with pytest.
- 100% offline (no external API calls).
- Same content-based logic as traditional version but local/fast.
- predicted_score values make sense (higher = better match).
