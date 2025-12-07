import apiClient from './axios';

/**
 * Get user's watchlist
 * @returns {Promise<{watchlist: Array, count: number}>}
 */
export const getWatchlist = async () => {
  const response = await apiClient.get('/watchlist/');
  return response.data;
};

/**
 * Add movie to watchlist
 * @param {number} movieId - Movie ID to add
 * @returns {Promise<{message: string, watchlist_item: object}>}
 */
export const addToWatchlist = async (movieId) => {
  const response = await apiClient.post('/watchlist/', { movie_id: movieId });
  return response.data;
};

/**
 * Remove movie from watchlist
 * @param {number} movieId - Movie ID to remove
 * @returns {Promise<{message: string}>}
 */
export const removeFromWatchlist = async (movieId) => {
  const response = await apiClient.delete(`/watchlist/${movieId}/`);
  return response.data;
};

