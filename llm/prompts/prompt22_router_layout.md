ROLE: Senior React developer architect for FilmHub.

TASK: Complete App with full routing, layout and protected routes.

CONSTRAINTS:
- react-router-dom v6
- ProtectedRoute component (redirect /login if no token)
- Layout: Navbar (logo, movies, watchlist, recommendations, profile, logout)
- Responsive mobile menu
- ErrorBoundary
- **CSS SEPARADO**: Use CSS files, NOT Tailwind classes in className
- Responsive design with CSS media queries
- 404 page

OUTPUT:
1. src/App.jsx (complete router)
2. src/components/Layout.jsx + Layout.css
3. src/components/ProtectedRoute.jsx
4. src/components/Navbar.jsx + Navbar.css (already exists)
5. src/pages/NotFound.jsx + NotFound.css
6. src/components/ErrorBoundary.jsx + ErrorBoundary.css
7. Update all stores → persist token to localStorage

**IMPORTANT**: All styling in separate .css files. NO Tailwind classes in className attributes.

ROUTES:
Public: /login, /register
Protected: /movies, /movies/:id, /profile, /recommendations, /watchlist

EVALUATION:
- All routes work and protected correctly
- Navbar shows correct links + logout
- Mobile responsive
- Token persists across refreshes
- All components use CSS files, not inline Tailwind classes

