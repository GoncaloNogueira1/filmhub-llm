ROLE: Senior Django REST Framework developer.

TASK: Implement the login endpoint for FilmHub that issues JWT tokens.

CONSTRAINTS:
- Stack: Django 4.2, DRF, djangorestframework-simplejwt (or equivalent)
- Endpoint: POST /api/auth/login/
- Request JSON: email, password
- On success return HTTP 200 with access and refresh tokens
- On invalid credentials return HTTP 401 with an error message
- Use Django’s authentication system and SimpleJWT
- Include unit tests with pytest + APIClient

EXAMPLES:
Example 1 – valid login  
Request: {"email": "user@example.com", "password": "testpass123"}  
Expected: HTTP 200 with {"access": "...", "refresh": "..."}

Example 2 – wrong password  
Request: {"email": "user@example.com", "password": "wrong"}  
Expected: HTTP 401 with an error message.

OUTPUT:
- serializers.py: Login serializer
- views.py: login view
- urls.py: /api/auth/login/
- tests: at least 3 tests (valid login, wrong password, non-existing user)

EVALUATION:
- All tests pass
- Issued tokens work with DRF authenticated endpoints
- No sensitive data leaked in responses
