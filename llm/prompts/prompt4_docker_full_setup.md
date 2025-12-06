ROLE: Senior DevOps engineer experienced with Docker Compose, Django and React (Vite).

TASK: Review and redesign the docker-compose.yml for the FilmHub project so that backend, frontend and PostgreSQL work correctly together in development mode.

CONSTRAINTS:
- Monorepo layout:
  - backend/ → Django app (run with `python manage.py runserver 0.0.0.0:8000`)
  - frontend/ → React + Vite app (run with `npm run dev -- --host 0.0.0.0 --port 5173`)
- Database: PostgreSQL service in Docker
- Goals:
  - Access Django API from host at http://localhost:8000
  - Access React dev server from host at http://localhost:5173 (or 3000 if you recommend mapping)
  - Frontend must be able to call the backend using an ENV like VITE_API_BASE_URL
- Use simple dev setup (no nginx, no gunicorn yet)
- Enable live reload:
  - Mount backend code into the backend container
  - Mount frontend code into the frontend container
- Keep environment variables in .env files, not hard-coded
- Keep configuration compatible with future production setup (where we can later add gunicorn/nginx, but NOT now)

EXAMPLES:
- Service names: `backend`, `frontend`, `db`
- Postgres image: `postgres:15-alpine`
- Backend depends_on: db
- Frontend should NOT fail if backend is still starting (best-effort only)

OUTPUT:
1. A clean docker-compose.yml file that:
   - defines services: db, backend, frontend
   - sets correct build contexts and commands for each service
   - exposes ports 5432, 8000 and 5173 to the host
   - mounts local source code for backend and frontend
2. A short note on:
   - which URLs to use in the browser for backend and frontend
   - what value to set in VITE_API_BASE_URL for dev
3. A short list of commands to:
   - start the stack
   - rebuild if Dockerfile or dependencies change

EVALUATION:
- After following your instructions, `docker-compose up --build` must start all three services.
- Backend must be reachable from the host and from the frontend container.
- Frontend must load in the browser and be able to make requests to the backend API.
