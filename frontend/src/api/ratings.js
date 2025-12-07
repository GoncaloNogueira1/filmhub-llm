import apiClient from './axios';

const ratingsAPI = {
  /**
   * Rate a movie (create or update rating)
   * @param {number} movieId - Movie ID
   * @param {Object} ratingData - {score: 1-5, comment?: string}
   * @returns {Promise}
   */
  rateMovie: async (movieId, ratingData) => {
    const response = await apiClient.post(`/movies/${movieId}/rate/`, ratingData);
    return response.data;
  },

  /**
   * Get current user's rating for a movie
   * @param {number} movieId - Movie ID
   * @returns {Promise}
   */
  getUserRating: async (movieId) => {
    try {
      const response = await apiClient.get(`/movies/${movieId}/my-rating/`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        return null; // User hasn't rated this movie
      }
      throw error;
    }
  },

  /**
   * Get movie rating aggregate (average, count)
   * @param {number} movieId - Movie ID
   * @returns {Promise}
   */
  getMovieRating: async (movieId) => {
    const response = await apiClient.get(`/movies/${movieId}/rating/`);
    return response.data;
  },
};

export default ratingsAPI;

