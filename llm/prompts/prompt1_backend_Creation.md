ROLE: DevOps engineer and Django expert helping with project setup.

TASK: Propose the minimal but robust backend setup for the FilmHub project using Django and PostgreSQL, without writing full application logic for the use cases yet.

CONSTRAINTS:
- Use Django 4.2 and Django REST Framework
- Database: PostgreSQL (to be used later via Docker)
- Project name: filmhub
- Create separate Django apps for: auth, movies, ratings, recommendations, watchlist
- Only include configuration needed to run the project locally (INSTALLED_APPS, middleware for CORS, REST_FRAMEWORK settings, basic database config)
- Do NOT implement any endpoints, models or business logic yet
- Output should be focused on commands and configuration snippets, not full production code

EXAMPLES:
- Show the shell commands to create the virtual environment, install dependencies and start the Django project
- Show how INSTALLED_APPS and MIDDLEWARE should look after adding rest_framework and corsheaders

OUTPUT:
- A step-by-step list of terminal commands to:
  - create the virtualenv
  - install the required backend packages
  - create the Django project and the 5 apps
- The minimal settings.py snippets to:
  - register the apps
  - configure CORS
  - add REST_FRAMEWORK defaults
  - define a PostgreSQL DATABASES block with placeholders for env vars
- A short note about when we will later integrate Docker and CI/CD

EVALUATION:
- Following the steps must result in a Django project that starts with `python manage.py runserver`
- No application-specific logic is introduced yet (only setup)
- Configuration is compatible with later Docker and CI/CD integration
