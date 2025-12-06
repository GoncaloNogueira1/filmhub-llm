ROLE: Senior Django REST Framework developer for FilmHub.

TASK: Implement UC5 – the GET /api/search endpoint for movie search with autocomplete, using the local Movie table.

CONSTRAINTS:
- Use the Movie model already populated by the TMDB import.
- Endpoint: GET /api/search
- Query parameter: `q` (search term).
- Response JSON:
  {
    "count": integer,
    "results": [ { movie fields... } ],
    "suggestions": [ "string", ... ]
  }
- JWT authentication required (only logged-in users can search).
- Pagination via `page` and `page_size` (page_size with max 50).
- Search across title and overview (and optionally genres) with case-insensitive matching.
- `q` must be between 2 and 100 characters; shorter or longer queries should return HTTP 400 with a clear error message.
- Handle empty results gracefully.
- Use Django ORM only; no raw SQL.

EXAMPLES:
Example 1 – valid search:
GET /api/search?q=matrix&page=1&page_size=10  
Expected: HTTP 200 with:
- `results` containing movies whose title/overview contains “matrix”,
- `suggestions` containing top matching titles.

Example 2 – query too short:
GET /api/search?q=a  
Expected: HTTP 400 with an error explaining that the query is too short.

OUTPUT:
- views.py: search view or ViewSet.
- serializers.py: serializer for search result items.
- urls.py: route for /api/search.
- tests (pytest) covering:
  - valid search with results,
  - search with no results,
  - short query (400),
  - pagination,
  - missing/invalid JWT (401).

EVALUATION:
- All tests pass.
- No critical Bandit findings.
- Performance is acceptable for typical query sizes.
