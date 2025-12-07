ROLE: Senior Django REST Framework developer.

TASK: Implement UC3 – user profile management for FilmHub.

CONSTRAINTS:
- PATCH /api/profile/ → update user profile (name, genre_preferences JSON, age, etc.)
- GET /api/profile/ → return current user profile
- JWT authentication required.
- Use Django User model + custom UserProfile model (if needed).
- genre_preferences as JSON field: {"action": 0.8, "drama": 0.3, ...}
- Django ORM only.

EXAMPLES:
PATCH /api/profile/ {"name": "John Doe", "genre_preferences": {"28": 0.9, "18": 0.6}} → 200 updated profile
GET /api/profile/ → current user data

OUTPUT:
- models.py: UserProfile (if needed)
- serializers.py: ProfileSerializer
- views.py: profile viewset
- urls.py: /api/profile/
- tests: GET profile, PATCH update, invalid data

EVALUATION:
- Tests pass, profile updates correctly.
