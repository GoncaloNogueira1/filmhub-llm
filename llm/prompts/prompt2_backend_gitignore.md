ROLE: Senior DevOps engineer with experience in Python and Django projects.

TASK: Create a .gitignore file for the backend of the FilmHub project.

CONSTRAINTS:
- Backend stack: Python 3.11, Django 4.2, Django REST Framework, pytest, virtualenv
- Must ignore:
  - virtual environments (venv/)
  - Python cache and build artifacts (__pycache__, *.pyc, *.pyo, *.pyd, .Python, build/, dist/)
  - coverage and test outputs (.pytest_cache/, .coverage, htmlcov/)
  - IDE/editor files (.vscode/, .idea/, *.iml)
  - OS files (Thumbs.db, .DS_Store)
  - local environment/config files (.env, .env.*, *.sqlite3)
  - logs and temporary files (*.log, tmp/, *.tmp)
- Do NOT ignore: requirements.txt, manage.py, migrations, Dockerfile, ci configs, or source code.

EXAMPLES:
- Typical Django .gitignore entries for venv and __pycache__.

OUTPUT:
- Only the final .gitignore content, ready to be saved as backend/.gitignore.
- No explanations, no comments outside the file.

EVALUATION:
- Running `git status` after this should show only relevant source files and configs, never the virtualenv, caches, or local env