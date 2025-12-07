ROLE: Senior React developer for FilmHub.

TASK: Implement authentication frontend (Login + Register pages).

CONSTRAINTS:
- POST /api/auth/register/ → {email, username, password}
- POST /api/auth/login/ → {email, password} → returns {access, refresh}
- JWT tokens stored in localStorage + Zustand store
- Protected routes redirect to /login if not authenticated
- **CSS SEPARADO**: Use CSS files, NOT Tailwind classes in className
- Responsive design with CSS media queries

EXAMPLES:
Register → success → redirect to /login
Login → success → store tokens → redirect to /movies
Invalid credentials → show error message
Protected route access without token → redirect to /login

OUTPUT:
1. src/pages/LoginPage.jsx + LoginPage.css
2. src/pages/RegisterPage.jsx + RegisterPage.css
3. src/api/auth.js (register, login, logout)
4. src/stores/authStore.js (user, tokens, isAuthenticated, login, logout)
5. src/components/ProtectedRoute.jsx
6. Update App.jsx → add /login, /register routes

**IMPORTANT**: All styling in separate .css files. NO Tailwind classes in className attributes.

EVALUATION:
- Registration creates account and redirects
- Login stores tokens and redirects
- Protected routes redirect unauthenticated users
- Logout clears tokens and redirects to login
- Responsive layout works on mobile/desktop

