import { create } from 'zustand';
import * as watchlistAPI from '../api/watchlist';

const useWatchlistStore = create((set, get) => ({
  watchlist: [],
  count: 0,
  loading: false,
  error: null,
  movieIds: new Set(), // Quick lookup for O(1) checks

  // Fetch watchlist from API
  fetchWatchlist: async () => {
    set({ loading: true, error: null });
    try {
      const data = await watchlistAPI.getWatchlist();
      const movieIds = new Set(data.watchlist.map(item => item.movie.id || item.movie_id));
      set({
        watchlist: data.watchlist,
        count: data.count,
        movieIds,
        loading: false,
      });
    } catch (error) {
      console.error('Error fetching watchlist:', error);
      set({ error: error.message, loading: false });
    }
  },

  // Add movie to watchlist
  addToWatchlist: async (movieId) => {
    try {
      const response = await watchlistAPI.addToWatchlist(movieId);
      // Update local state immediately for instant feedback
      const { watchlist, movieIds } = get();
      const newMovieIds = new Set(movieIds);
      newMovieIds.add(movieId);
      
      // Add the new item to watchlist if not already present
      const itemExists = watchlist.some(
        item => (item.movie?.id || item.movie_id) === movieId
      );
      
      if (!itemExists && response.watchlist_item) {
        set({
          watchlist: [...watchlist, response.watchlist_item],
          count: watchlist.length + 1,
          movieIds: newMovieIds,
        });
      } else {
        set({
          movieIds: newMovieIds,
        });
      }
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      throw error;
    }
  },

  // Remove movie from watchlist
  removeFromWatchlist: async (movieId) => {
    try {
      await watchlistAPI.removeFromWatchlist(movieId);
      // Update local state immediately for instant feedback
      const { watchlist, movieIds } = get();
      const newWatchlist = watchlist.filter(
        item => (item.movie?.id || item.movie_id) !== movieId
      );
      const newMovieIds = new Set(movieIds);
      newMovieIds.delete(movieId);
      
      set({
        watchlist: newWatchlist,
        count: newWatchlist.length,
        movieIds: newMovieIds,
      });
    } catch (error) {
      console.error('Error removing from watchlist:', error);
      throw error;
    }
  },

  // Check if movie is in watchlist
  isInWatchlist: (movieId) => {
    return get().movieIds.has(movieId);
  },

  // Clear watchlist (e.g., on logout)
  clearWatchlist: () => {
    set({
      watchlist: [],
      count: 0,
      movieIds: new Set(),
      error: null,
    });
  },
}));

export default useWatchlistStore;

