import React, { useState, useEffect } from 'react';
import { useAuthStore } from '../../stores/authStore';
import useWatchlistStore from '../../stores/watchlistStore';
import './WatchlistButton.css';

const WatchlistButton = ({ movieId, className = '', size = 'sm' }) => {
  const { isAuthenticated } = useAuthStore();
  const { isInWatchlist, addToWatchlist, removeFromWatchlist, fetchWatchlist, movieIds } = useWatchlistStore();
  const [loading, setLoading] = useState(false);
  
  // Get current watchlist status from store
  const inWatchlist = isInWatchlist(movieId);

  // Fetch watchlist on mount if authenticated and not loaded
  useEffect(() => {
    if (isAuthenticated && movieId) {
      const { count } = useWatchlistStore.getState();
      if (count === 0) {
        fetchWatchlist();
      }
    }
  }, [movieId, isAuthenticated, fetchWatchlist]);

  const handleToggle = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!isAuthenticated) {
      return;
    }

    setLoading(true);
    try {
      if (inWatchlist) {
        await removeFromWatchlist(movieId);
      } else {
        await addToWatchlist(movieId);
      }
    } catch (error) {
      console.error('Error toggling watchlist:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <button
      onClick={handleToggle}
      disabled={loading}
      className={`watchlist-button size-${size} ${inWatchlist ? 'in-list' : 'not-in-list'} ${loading ? 'loading' : ''} ${className}`}
      title={inWatchlist ? 'Remove from list' : 'Add to list'}
      aria-label={inWatchlist ? 'Remove from list' : 'Add to list'}
    >
      {loading ? (
        <svg fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      ) : (
        <svg
          fill={inWatchlist ? 'currentColor' : 'none'}
          stroke="currentColor"
          viewBox="0 0 24 24"
          strokeWidth={inWatchlist ? 0 : 1.5}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
          />
        </svg>
      )}
    </button>
  );
};

export default WatchlistButton;

