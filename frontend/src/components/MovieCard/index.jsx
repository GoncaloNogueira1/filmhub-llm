import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import WatchlistButton from '../WatchlistButton';
import './MovieCard.css';

const MovieCard = ({ movie }) => {
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);
  
  // Tratar diferentes formatos de URL do poster
  const getPosterUrl = () => {
    if (imageError) {
      return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="300"%3E%3Crect fill="%231e293b" width="200" height="300"/%3E%3Ctext fill="%2364758b" x="50%25" y="50%25" text-anchor="middle" dy=".3em" font-family="sans-serif" font-size="14"%3ENo Image%3C/text%3E%3C/svg%3E';
    }
    
    let url = movie.poster_url || movie.poster_path;
    
    // Se já é uma URL completa, usar diretamente
    if (url && (url.startsWith('http://') || url.startsWith('https://'))) {
      return url;
    }
    
    // Se é um caminho relativo do TMDB, construir URL com tamanho menor
    if (url && url.startsWith('/')) {
      return `https://image.tmdb.org/t/p/w185${url}`;
    }
    
    // Fallback
    return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="300"%3E%3Crect fill="%231e293b" width="200" height="300"/%3E%3Ctext fill="%2364758b" x="50%25" y="50%25" text-anchor="middle" dy=".3em" font-family="sans-serif" font-size="14"%3ENo Image%3C/text%3E%3C/svg%3E';
  };
  
  // Get genres as array
  const getGenres = () => {
    if (!movie.genres) return [];
    if (Array.isArray(movie.genres)) {
      return movie.genres.map(g => typeof g === 'string' ? g : g.name || g).slice(0, 2);
    }
    return [];
  };

  // Get release year
  const getYear = () => {
    if (movie.release_year) return movie.release_year;
    if (movie.release_date) {
      return new Date(movie.release_date).getFullYear();
    }
    return null;
  };

  return (
    <Link to={`/movies/${movie.id}`} className="movie-card">
      {/* Poster Image Container */}
      <div className="movie-card-poster-container">
        {imageLoading && (
          <div className="movie-card-poster-loading">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}
        
        <img
          src={getPosterUrl()}
          alt={movie.title}
          className={`movie-card-poster ${imageLoading ? 'loading' : 'loaded'}`}
          onLoad={() => setImageLoading(false)}
          onError={() => {
            setImageError(true);
            setImageLoading(false);
          }}
          loading="lazy"
        />
        
        {/* Gradient overlay on hover */}
        <div className="movie-card-overlay" />
        
        {/* Rating Badge - Only show on hover */}
        {movie.vote_average && (
          <div className="movie-card-rating">
            <div className="movie-card-rating-badge">
              <svg viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <span>{movie.vote_average.toFixed(1)}</span>
            </div>
          </div>
        )}
        
        {/* Watchlist Button - Only show on hover */}
        <div className="movie-card-watchlist">
          <WatchlistButton movieId={movie.id} size="sm" />
        </div>
      </div>
      
      {/* Movie Info - Always visible */}
      <div className="movie-card-info">
        <h3 className="movie-card-title">{movie.title}</h3>
        <div className="movie-card-meta">
          {getYear() && (
            <p className="movie-card-year">{getYear()}</p>
          )}
          {getGenres().length > 0 && (
            <div className="movie-card-genres">
              {getGenres().map((genre, idx) => (
                <span key={idx} className="movie-card-genre">{genre}</span>
              ))}
            </div>
          )}
        </div>
      </div>
    </Link>
  );
};

export default MovieCard;
