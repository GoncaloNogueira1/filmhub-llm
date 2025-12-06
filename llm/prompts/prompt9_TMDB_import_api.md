ROLE: Senior Django backend developer experienced with external API integration.

TASK: Implement a Django management command that imports movies from the TMDB API into the local Movie model for FilmHub.

CONSTRAINTS:
- Use environment variable TMDB_API_KEY for authentication (do NOT hard-code the key).
- Use TMDB v3 API.
- Fetch a limited number of movies (for example the first N pages of the “popular” endpoint, or results for a fixed list of keywords).
- Map TMDB fields to the Movie model:
  - tmdb_id      ← TMDB id
  - title        ← title
  - overview     ← overview
  - release_year ← year part of release_date
  - poster_url   ← full URL built from poster_path
  - genres       ← list of genre IDs or names
- Avoid duplicates: if a movie with the same tmdb_id already exists, update it instead of creating a new row.
- Handle API errors and rate limits gracefully (log and skip without crashing).
- Command name: `import_tmdb_movies`.
- Print a short summary (how many movies created and how many updated).

REASONING STEPS (Chain-of-Thought):
1. Decide how to extend the Movie model to store tmdb_id and genres (if not already present).
2. Implement a small TMDB client helper that:
   - reads TMDB_API_KEY from the environment,
   - calls the chosen TMDB endpoint(s),
   - returns normalized Python dicts with the fields needed for Movie.
3. Implement the management command `import_tmdb_movies` that:
   - iterates over pages/results from TMDB,
   - for each movie, creates or updates a Movie instance,
   - logs errors but continues processing.
4. Add a simple configuration mechanism (e.g. number of pages or items to fetch) via command options.
5. Print a final summary of created vs updated movies.

OUTPUT:
- Updated Movie model (if needed) with tmdb_id and genres fields.
- TMDB client helper functions.
- Management command in `movies/management/commands/import_tmdb_movies.py`.
- Example usage: `python manage.py import_tmdb_movies`.

EVALUATION:
- The command runs successfully when TMDB_API_KEY is set.
- Movies are correctly imported/updated in the database.
- No API key is hard-coded.
- Failures in TMDB calls do not crash the command.
