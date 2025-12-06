import requests
import logging
from typing import List, Dict, Optional
from decouple import config

logger = logging.getLogger(__name__)


class TMDBClient:
    """Client for The Movie Database (TMDB) API v3"""
    
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
    
    def __init__(self):
        self.api_key = config('TMDB_API_KEY', default='')
        if not self.api_key:
            raise ValueError(
                "TMDB_API_KEY not found in environment variables. "
                "Please set it in your .env file."
            )
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a GET request to TMDB API with error handling"""
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                logger.error("TMDB API rate limit exceeded. Please wait before retrying.")
            else:
                logger.error(f"HTTP error fetching {endpoint}: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {endpoint}: {e}")
        except ValueError as e:
            logger.error(f"Error parsing JSON from {endpoint}: {e}")
        
        return None
    
    def get_popular_movies(self, page: int = 1) -> List[Dict]:
        """Fetch popular movies from TMDB"""
        data = self._make_request('movie/popular', {'page': page})
        return data.get('results', []) if data else []
    
    def get_genre_list(self) -> Dict[int, str]:
        """Fetch genre list and return mapping of id to name"""
        data = self._make_request('genre/movie/list')
        if not data:
            return {}
        
        return {genre['id']: genre['name'] for genre in data.get('genres', [])}
    
    def normalize_movie_data(self, tmdb_movie: Dict, genre_map: Dict[int, str]) -> Dict:
        """Normalize TMDB movie data to our Movie model format"""
        release_date = tmdb_movie.get('release_date', '')
        release_year = None
        if release_date:
            try:
                release_year = int(release_date.split('-')[0])
            except (ValueError, IndexError):
                logger.warning(f"Invalid release_date: {release_date}")
        
        # Map genre IDs to names
        genre_ids = tmdb_movie.get('genre_ids', [])
        genres = [genre_map.get(gid, f"Unknown({gid})") for gid in genre_ids]
        
        # Build full image URLs
        poster_path = tmdb_movie.get('poster_path', '')
        backdrop_path = tmdb_movie.get('backdrop_path', '')
        
        return {
            'tmdb_id': tmdb_movie['id'],
            'title': tmdb_movie.get('title', 'Unknown Title'),
            'overview': tmdb_movie.get('overview', ''),
            'release_year': release_year,
            'poster_url': f"{self.IMAGE_BASE_URL}{poster_path}" if poster_path else '',
            'backdrop_url': f"{self.IMAGE_BASE_URL}{backdrop_path}" if backdrop_path else '',
            'genres': genres,
            'vote_average': tmdb_movie.get('vote_average'),
            'popularity': tmdb_movie.get('popularity'),
        }
