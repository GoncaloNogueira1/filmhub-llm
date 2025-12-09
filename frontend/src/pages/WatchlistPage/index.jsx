import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import MovieCard from '../../components/MovieCard';
import useWatchlistStore from '../../stores/watchlistStore';
import { useAuthStore } from '../../stores/authStore';
import Button from '../../components/ui/Button';
import './WatchlistPage.css';

const WatchlistPage = () => {
  const { isAuthenticated } = useAuthStore();
  const { watchlist, count, loading, error, fetchWatchlist, removeFromWatchlist } = useWatchlistStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      fetchWatchlist();
    }
  }, [isAuthenticated, fetchWatchlist]);

  const handleRemove = async (movieId) => {
    try {
      await removeFromWatchlist(movieId);
    } catch (error) {
      console.error('Error removing from watchlist:', error);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="watchlist-page">
        <div style={{ textAlign: 'center', color: 'white' }}>
          <h1 className="watchlist-title">My List</h1>
          <p style={{ fontSize: '1.125rem', color: 'rgb(156 163 175)', marginBottom: '2rem' }}>
            Please login to view your watchlist!
          </p>
          <Link to="/login">
            <Button>Login</Button>
          </Link>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="watchlist-page">
        <h1 className="watchlist-title" style={{ textAlign: 'center', marginBottom: '2rem' }}>My List</h1>
        <div className="watchlist-loading">
          <div className="watchlist-loading-spinner"></div>
          <p className="watchlist-loading-text">Loading your watchlist...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="watchlist-page">
        <div className="watchlist-error">
          <h1 className="watchlist-error-title">My List</h1>
          <p className="watchlist-error-text">{error}</p>
          <Button onClick={() => fetchWatchlist()}>Try Again</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="watchlist-page">
      <div className="watchlist-header">
        <h1 className="watchlist-title">My List</h1>
        {count > 0 && (
          <span className="watchlist-count">
            {count} {count === 1 ? 'movie' : 'movies'}
          </span>
        )}
      </div>

      {count === 0 ? (
        <div className="watchlist-empty">
          <div className="watchlist-empty-icon">
            <svg
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
              />
            </svg>
          </div>
          <h2 className="watchlist-empty-title">
            Your watchlist is empty
          </h2>
          <p className="watchlist-empty-text">
            Add movies to your watchlist to watch later!
          </p>
          <Link to="/movies">
            <Button>Explore Movies</Button>
          </Link>
        </div>
      ) : (
        <div className="watchlist-grid">
          {watchlist.map((item) => {
            const movie = item.movie || item;
            return (
              <div key={movie.id || item.movie_id} className="watchlist-movie">
                <MovieCard movie={movie} />
                <button
                  onClick={() => handleRemove(movie.id || item.movie_id)}
                  className="watchlist-remove-button"
                  title="Remove from list"
                >
                  Remove
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default WatchlistPage;

