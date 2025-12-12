#!/bin/bash
set -e

echo "🚀 Starting FilmHub Backend Setup..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for database to be ready..."
until python manage.py shell -c "from django.db import connection; connection.ensure_connection()" 2>/dev/null; do
  echo "   Database is unavailable - sleeping"
  sleep 1
done
echo "✅ Database is ready!"

# Run migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput
echo "✅ Migrations completed!"

# Check if movies already exist and import if needed
echo "📽️  Checking for existing movies..."
MOVIE_COUNT=$(python manage.py shell -c "from movies.models import Movie; print(Movie.objects.count())" 2>/dev/null || echo "0")

if [ "$MOVIE_COUNT" = "0" ]; then
  echo "📽️  No movies found. Importing from TMDB (this may take a minute)..."
  python manage.py import_tmdb_movies --pages 15 || echo "⚠️  Import failed, but continuing..."
  echo "✅ Import process completed!"
elif [ "$MOVIE_COUNT" -lt 100 ]; then
  echo "📽️  Found $MOVIE_COUNT movies (less than 100). Importing more to reach ~300 movies..."
  # Calculate pages needed: (300 - current) / 20 per page, rounded up
  PAGES_NEEDED=$(( (300 - MOVIE_COUNT + 19) / 20 ))
  # Cap at 20 pages to avoid too long imports
  if [ "$PAGES_NEEDED" -gt 20 ]; then
    PAGES_NEEDED=20
  fi
  echo "📽️  Importing $PAGES_NEEDED additional pages (~$((PAGES_NEEDED * 20)) movies)..."
  python manage.py import_tmdb_movies --pages $PAGES_NEEDED || echo "⚠️  Import failed, but continuing..."
  echo "✅ Import process completed!"
else
  echo "✅ Database already has $MOVIE_COUNT movies (≥100). Skipping import."
fi

echo "🎬 Starting Django application..."
exec "$@"

