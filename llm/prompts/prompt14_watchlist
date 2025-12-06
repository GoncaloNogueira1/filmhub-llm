ROLE: Senior Django REST Framework developer.

TASK: Implement UC8–10 – watchlist management for FilmHub.

CONSTRAINTS:
- Use a Watchlist model that links User and Movie (one entry per user/movie).
- Endpoints:
  - POST   /api/watchlist/           → add a movie to the user’s watchlist.
  - DELETE /api/watchlist/{movie_id}/ → remove a movie from the user’s watchlist.
  - GET    /api/watchlist/           → list the user’s watchlist.
- JWT authentication required for all endpoints.
- Prevent duplicates: adding the same movie twice should not create duplicate rows.
- Use DRF serializers and views; Django ORM only.

EXAMPLES:
Example 1 – add:
POST /api/watchlist/ with { "movie_id": 1 } → HTTP 201 or 200.

Example 2 – list:
GET /api/watchlist/ → list of movies for that user.

Example 3 – remove:
DELETE /api/watchlist/1/ → HTTP 204 (or 200) and the entry is removed.

OUTPUT:
- models.py: Watchlist model (if not already defined).
- serializers.py: Watchlist serializer(s).
- views.py: add, remove, list endpoints.
- urls.py: routes under /api/watchlist/.
- tests: add, duplicate add, list, remove, auth required.

EVALUATION:
- All tests pass.
- No duplicate watchlist entries per user/movie.
- Auth is enforced correctly.
