ROLE: Senior Django REST Framework developer.

TASK: Implement UC6 – movie ratings endpoints for FilmHub.

CONSTRAINTS:
- Use existing User, Movie and Rating models (Rating links a user to a movie, with fields like score 1–5 and optional comment).
- Endpoints:
  - POST /api/movies/{id}/rate/    → create or update the authenticated user’s rating for that movie.
  - GET  /api/movies/{id}/rating/  → return aggregate rating info for that movie (average score and ratings count).
- JWT authentication required for POST; GET may be public.
- A user can have at most one rating per movie; a second POST updates the existing rating.
- Validate score as an integer between 1 and 5.
- Use DRF serializers and views; use Django ORM only.

EXAMPLES:
Example 1 – create rating:
POST /api/movies/1/rate/ with { "score": 5, "comment": "Great movie" }  
→ HTTP 201 or 200 with the rating details.

Example 2 – update rating:
Same user posts { "score": 3 } again for movie 1  
→ HTTP 200 and the existing rating is updated instead of duplicated.

Example 3 – aggregate:
GET /api/movies/1/rating/  
→ { "movie_id": 1, "average_score": 4.2, "ratings_count": 17 }

OUTPUT:
- serializers.py: Rating serializer(s).
- views.py: endpoints for POST rate and GET rating aggregate.
- urls.py: routes for these endpoints.
- tests: at least
  - create rating,
  - update rating,
  - invalid score,
  - aggregate values,
  - auth required for POST.

EVALUATION:
- All tests pass.
- No duplicate ratings per user/movie.
- Aggregates are correct for the test data.
