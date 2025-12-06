import logging
from django.core.management.base import BaseCommand
from movies.models import Movie
from movies.tmdb_client import TMDBClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import movies from TMDB API into the local database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            default=5,
            help='Number of pages to fetch from TMDB (default: 5)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing movies before importing'
        )
    
    def handle(self, *args, **options):
        pages = options['pages']
        clear_existing = options['clear']
        
        self.stdout.write(self.style.WARNING(
            f'Starting TMDB import (fetching {pages} pages)...'
        ))
        
        # Clear existing movies if requested
        if clear_existing:
            count = Movie.objects.count()
            Movie.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f'Cleared {count} existing movies'
            ))
        
        # Initialize TMDB client
        try:
            client = TMDBClient()
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return
        
        # Fetch genre mapping
        self.stdout.write('Fetching genre list...')
        genre_map = client.get_genre_list()
        if not genre_map:
            self.stdout.write(self.style.ERROR(
                'Failed to fetch genre list. Continuing without genres.'
            ))
            genre_map = {}
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Loaded {len(genre_map)} genres'
            ))
        
        # Import movies
        created_count = 0
        updated_count = 0
        error_count = 0
        
        for page in range(1, pages + 1):
            self.stdout.write(f'Fetching page {page}/{pages}...')
            
            movies = client.get_popular_movies(page)
            if not movies:
                self.stdout.write(self.style.WARNING(
                    f'No movies returned for page {page}'
                ))
                continue
            
            for tmdb_movie in movies:
                try:
                    # Normalize TMDB data
                    movie_data = client.normalize_movie_data(tmdb_movie, genre_map)
                    
                    # Create or update movie
                    movie, created = Movie.objects.update_or_create(
                        tmdb_id=movie_data['tmdb_id'],
                        defaults=movie_data
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'  ✓ Created: {movie.title} ({movie.release_year})'
                        ))
                    else:
                        updated_count += 1
                        self.stdout.write(
                            f'  ↻ Updated: {movie.title} ({movie.release_year})'
                        )
                
                except Exception as e:
                    error_count += 1
                    logger.exception(f"Error processing movie: {e}")
                    self.stdout.write(self.style.ERROR(
                        f'  ✗ Error processing movie ID {tmdb_movie.get("id")}: {e}'
                    ))
        
        # Print summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('Import completed!'))
        self.stdout.write(f'  Created: {created_count}')
        self.stdout.write(f'  Updated: {updated_count}')
        self.stdout.write(f'  Errors:  {error_count}')
        self.stdout.write(f'  Total:   {created_count + updated_count}')
        self.stdout.write('=' * 50)
