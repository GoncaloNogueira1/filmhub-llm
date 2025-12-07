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
  python manage.py import_tmdb_movies --pages 3 || echo "⚠️  Import failed, but continuing..."
  echo "✅ Import process completed!"
else
  echo "✅ Database already has $MOVIE_COUNT movies. Skipping import."
fi

echo "🎬 Starting Django development server..."
exec "$@"

