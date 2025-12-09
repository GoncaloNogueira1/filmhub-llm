I need to deploy FilmHub to Render.com. I have Django backend and React frontend, but the Dockerfiles are configured for development. I need to adapt them for production.

**Current situation:**
- Backend: Dockerfile uses `runserver` (dev only)
- Frontend: Dockerfile uses `npm run dev` (dev only)
- Health check already exists at `/api/health/`
- Settings already uses environment variables

**What to do:**

1. **Backend Dockerfile:**
   - Add `gunicorn` to requirements.txt
   - Change CMD from `runserver` to `gunicorn filmhub.wsgi:application --bind 0.0.0.0:8000 --workers 2`
   - Keep entrypoint.sh (already runs migrations)

2. **Frontend Dockerfile:**
   - Build: `npm run build` (creates `dist/` folder)
   - Serve with `serve -s dist -l 3000` (or nginx)
   - Important: `VITE_API_BASE_URL` must be defined BEFORE build

3. **Settings.py:**
   - `DEBUG = config('DEBUG', default=False, cast=bool)`
   - `ALLOWED_HOSTS` with Render backend URL
   - `CORS_ALLOWED_ORIGINS` with Render frontend URL
   - `SECRET_KEY` via env var (required)

4. **Environment variables in Render:**
   Backend: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`
   Frontend: `VITE_API_BASE_URL` (at build time!)

5. **DEPLOYMENT.md:**
   - Step-by-step guide for Render
   - List of env vars
   - How to create PostgreSQL, Backend and Frontend services

**Reminders:**
- Render free tier can "sleep" (normal)
- Health check: `/api/health/`
- `VITE_API_BASE_URL` at build time, not after

Generate the modified files and DEPLOYMENT.md.

