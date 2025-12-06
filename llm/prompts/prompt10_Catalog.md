ROLE: Senior Django REST Framework developer.

TASK: Implement UC4 – movie catalog endpoints for FilmHub that read from the local Movie table populated by the TMDB import command.

CONSTRAINTS:
- Use the existing Movie model with fields such as: id, tmdb_id, title, overview, release_year, genres, poster_url, average_rating.
- Endpoints:
  - GET /api/movies/        → paginated list of movies
  - GET /api/movies/{id}/   → details of a single movie
- Endpoints are public read-only (no auth required).
- Pagination via `page` and `page_size` query parameters (page_size with a safe upper limit).
- Optional filtering by title substring using `?q=` (case-insensitive).
- Use DRF generic views or a ViewSet with routers.
- Use Django ORM only (no raw SQL).
- Include unit tests with pytest + APIClient.

EXAMPLES:
Example 1 – list:
Request: GET /api/movies/?page=1&page_size=10  
Expected: HTTP 200 with JSON containing `count`, `next`, `previous`, and a `results` list of movies.

Example 2 – detail:
Request: GET /api/movies/1/  
Expected: HTTP 200 with JSON for that movie; if the id does not exist, HTTP 404.

OUTPUT:
- serializers.py: Movie serializer.
- views.py: list + detail views or a ViewSet.
- urls.py: routes under /api/movies/.
- tests: at least
  - list movies,
  - movie detail,
  - 404 for non-existing id,
  - pagination behaviour,
  - optional title filter.

EVALUATION:
- All tests pass with pytest.
- Pagination and filtering work as expected.
- The code integrates cleanly into the existing Django project.
