ROLE: Senior React developer for FilmHub.

TASK: Implement ProfilePage for UC3 that updates user profile.

CONSTRAINTS:
- GET /api/auth/profile/ → current profile data
- PATCH /api/auth/profile/ → {name, genre_preferences JSON, age}
- JWT Authorization header (from authStore)
- genre_preferences: {"28": 0.9, "18": 0.6, ...} (sliders 0-1)
- **CSS SEPARADO**: Use CSS files, NOT Tailwind classes in className
- Responsive design with CSS media queries
- Protected route (redirect /login if not authenticated)

EXAMPLES:
GET profile → form pre-filled with current data
PATCH name="John" genre_preferences={"28":1.0} → success message + refresh
Invalid genre_preferences → validation error

OUTPUT:
1. src/pages/ProfilePage.jsx + ProfilePage.css
2. src/api/auth.js → add getProfile, updateProfile methods (or create src/api/profile.js)
3. Update src/App.jsx → add /profile route (protected)
4. Update authStore.js → add user profile data

**NOTE**: Profile endpoints are in /api/auth/profile/, not /api/profile/

**IMPORTANT**: All styling in separate .css files. NO Tailwind classes in className attributes.

EVALUATION:
- Form reflects current profile on load
- Updates save to backend and refresh
- Genre sliders work (0-1 values)
- Protected route redirects unauthenticated users
