ROLE: Senior Django REST Framework developer working on the FilmHub project.

TASK: Implement the user registration endpoint for FilmHub using Django and DRF, recreating the same behaviour as in the traditional version of UC1 (Register).

CONSTRAINTS:
- Stack: Django 4.2, Django REST Framework, PostgreSQL
- Endpoint: POST /api/auth/register/
- Request JSON must include at least: email, password, (optionally age)
- Email must be unique
- Password must respect basic validation rules (min length 8)
- Passwords must be stored hashed using Django’s auth system
- On success return HTTP 201 with a simple JSON message or the created user data (without the password)
- On error return HTTP 400 with validation errors
- Use DRF serializers and generic views or APIView
- Include unit tests with pytest + APIClient

EXAMPLES:
Example 1 – successful registration  
Request:
POST /api/auth/register/  
Body: {"email": "user@example.com", "password": "testpass123", "age": 25}  
Expected: HTTP 201 and a JSON body indicating the user was created.

Example 2 – duplicate email  
Request:
POST /api/auth/register/  
Body: {"email": "user@example.com", "password": "anotherpass"}  
Expected: HTTP 400 with an error saying the email is already in use.

OUTPUT:
- serializers.py: Register serializer
- views.py: registration view
- urls.py: route for /api/auth/register/
- tests file (pytest) with 3–5 tests: successful registration, missing fields, weak password, duplicate email

EVALUATION:
- All tests pass with pytest
- Code integrates cleanly into a typical Django project structure
- No passwords or secrets are logged or returned in responses
