import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useMoviesStore } from '../stores/moviesStore';
import { getMovieDetail } from '../api/movies';
import ratingsAPI from '../api/ratings';
import RatingForm from '../components/RatingForm';
import WatchlistButton from '../components/WatchlistButton';
import './MovieDetailPage.css';

const MovieDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { setCurrentMovie } = useMoviesStore();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [movieRating, setMovieRating] = useState(null);
  const [movie, setMovie] = useState(null);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const movieData = await getMovieDetail(id);
        setMovie(movieData);
        setCurrentMovie(movieData);
        
        // Load movie rating aggregate
        try {
          const ratingData = await ratingsAPI.getMovieRating(id);
          setMovieRating(ratingData);
        } catch (err) {
          console.error('Error loading movie rating:', err);
        }
      } catch (err) {
        setError('Movie not found');
      } finally {
        setLoading(false);
      }
    };
    fetchMovie();
  }, [id, setCurrentMovie]);

  const handleRatingSubmitted = () => {
    // Refresh movie rating after submission
    ratingsAPI.getMovieRating(id).then(setMovieRating).catch(console.error);
  };

  if (loading) {
    return (
      <div className="movie-detail-loading">
        <div className="movie-detail-spinner"></div>
      </div>
    );
  }

  if (error || !movie) {
    return (
      <div className="movie-detail-error">
        <div className="movie-detail-error-content">
          <div className="movie-detail-error-emoji">🎥</div>
          <h1 className="movie-detail-error-title">{error || 'Movie not found'}</h1>
          <button 
            onClick={() => navigate(-1)}
            className="movie-detail-error-button"
          >
            Back
          </button>
        </div>
      </div>
    );
  }

  const posterUrl = movie.poster_url || movie.poster_path || '';
  const fullPosterUrl = posterUrl.startsWith('http') 
    ? posterUrl 
    : posterUrl.startsWith('/') 
      ? `https://image.tmdb.org/t/p/w500${posterUrl}`
      : '';

  return (
    <div className="movie-detail-container">
        <button
          onClick={() => navigate(-1)}
        className="movie-detail-back"
        >
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        Back
        </button>

      <div className="movie-detail-grid">
        {/* Movie Info */}
        <div className="movie-detail-info">
          <div className="movie-detail-card">
            <div className="movie-detail-header">
              {fullPosterUrl && (
              <img
                  src={fullPosterUrl}
                alt={movie.title}
                  className="movie-detail-poster"
                />
              )}
              <div className="movie-detail-content">
                <h1 className="movie-detail-title">{movie.title}</h1>
                <div className="movie-detail-meta">
                  {movie.vote_average && (
                    <div className="movie-detail-rating">
                      <svg viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                      <span className="movie-detail-rating-value">{movie.vote_average.toFixed(1)}</span>
            </div>
                  )}
                  {movie.release_year && (
                    <span className="movie-detail-year">{movie.release_year}</span>
                  )}
                  {movieRating && movieRating.ratings_count > 0 && (
                    <span className="movie-detail-ratings-count">
                      {movieRating.ratings_count} rating{movieRating.ratings_count !== 1 ? 's' : ''}
                    </span>
                  )}
                  <WatchlistButton movieId={movie.id} size="sm" />
              </div>

                {movie.genres && movie.genres.length > 0 && (
                  <div className="movie-detail-genres">
                    {movie.genres.map((genre, idx) => (
                      <span key={idx} className="movie-detail-genre">
                        {typeof genre === 'string' ? genre : genre.name || genre}
                    </span>
                  ))}
                </div>
              )}

              {movie.overview && (
                <div>
                    <h3 className="movie-detail-overview-title">Overview</h3>
                    <p className="movie-detail-overview-text">{movie.overview}</p>
                </div>
              )}
              </div>
            </div>
          </div>
        </div>

        {/* Rating Form */}
        <div className="movie-detail-rating-form">
          <RatingForm movieId={parseInt(id)} onRatingSubmitted={handleRatingSubmitted} />
        </div>
      </div>
    </div>
  );
};

export default MovieDetailPage;
