ROLE: Senior frontend engineer experienced with React, Vite and DevOps for student projects.

TASK: Design the initial frontend setup for the FilmHub project and provide the .gitignore for the frontend folder. Do NOT implement any application pages or business logic yet, only the project scaffolding.

CONSTRAINTS:
- Tech stack: React 18 + Vite + JavaScript (no TypeScript), npm
- The frontend lives in a folder called `frontend/` inside a monorepo
- Use Vite’s React template as base
- Do not create any complex components yet (no Search, Login, etc.)
- We only want:
  - The commands to create and initialize the project
  - A reasonable folder structure under `src/` (pages, components, api, styles, hooks)
  - A `.env.example` with `VITE_API_BASE_URL=http://localhost:8000/api`
  - A good `.gitignore` for this frontend
- The .gitignore must ignore:
  - node_modules/
  - build artifacts (dist/, .vite/)
  - log files (npm-debug.log*, yarn-debug.log*, yarn-error.log*)
  - environment files (.env, .env.*, .env.local)
  - editor/IDE folders (.vscode/, .idea/, *.iml)
  - OS files (.DS_Store, Thumbs.db)
- The .gitignore must NOT ignore:
  - package.json, package-lock.json
  - vite.config.*
  - src/, public/
  - Dockerfile or CI/CD files

EXAMPLES:
- Show the exact npm command to scaffold the Vite React app inside the existing `frontend/` folder.
- Show how to create the subfolders `src/pages`, `src/components`, `src/api`, `src/styles`, `src/hooks`.

OUTPUT:
1. A short ordered list of terminal commands to:
   - initialize the Vite React app in `frontend/`
   - install dependencies (React, Vite, axios, any basic state management if you recommend it)
   - create the src subfolders
   - create `.env.example` with the correct variable
2. The complete content of the `frontend/.gitignore` file, ready to save.
3. A brief note (1–2 sentences) explaining how this setup prepares us for later integration with the Django backend.

EVALUATION:
- After following the commands, `npm run dev` from `frontend/` must start the app without errors.
- `git status` in `frontend/` must not show node_modules, build artifacts, env files or editor/OS files.
