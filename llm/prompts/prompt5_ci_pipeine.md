ROLE: CI/CD specialist with strong experience in GitHub Actions, Docker, Django and React.

TASK: Create a GitHub Actions workflow file `.github/workflows/ci.yml` for the FilmHub project that builds and tests both backend (Django) and frontend (React + Vite). For now deployment is optional; focus on build + tests and making it easy to extend later.

CONSTRAINTS:
- Monorepo layout:
  - backend/ → Django 4.2 + DRF, pytest, Bandit, Pylint
  - frontend/ → React 18 + Vite + JavaScript (npm)
- Use PostgreSQL service for backend tests
- Workflow requirements:
  - Trigger on push and pull_request to `main`
  - Jobs:
    - Backend: install deps, run migrations (if needed), run pytest, run Bandit, run Pylint
    - Frontend: install deps, run `npm run build` and optionally `npm test` if defined
  - Use cache for pip and npm where reasonable
- No secrets hard-coded; database password etc. should use default test values or GitHub Secrets placeholders
- Must be compatible with a future “deploy” job that will only run on `main` after tests succeed (you can leave a placeholder comment for that stage)

FEW-SHOT EXAMPLES:
Example backend build/test step:
