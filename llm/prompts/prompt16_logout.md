ROLE: Senior Django REST Framework developer.

TASK: Implement UC11 – logout endpoint for FilmHub.

CONSTRAINTS:
- POST /api/auth/logout/ → invalidate JWT tokens
- Use djangorestframework-simplejwt
- Request body optional: {"refresh": "refresh_token"}
- Response: HTTP 205 Reset Content (standard for logout)
- Blacklist refresh token (SimpleJWT blacklist)
- JWT auth required.
- Clear frontend token storage (note only).

EXAMPLES:
POST /api/auth/logout/ {"refresh": "..."} → 205
POST /api/auth/logout/ → 205 (no refresh token)

OUTPUT:
- views.py: logout view
- urls.py: /api/auth/logout/
- tests: logout success, invalid token, no refresh token

EVALUATION:
- Tests pass, refresh tokens blacklisted.
