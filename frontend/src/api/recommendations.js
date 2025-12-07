import apiClient from './axios';

const recommendationsAPI = {
  /**
   * Get personalized movie recommendations
   * @param {number} limit - Number of recommendations (default: 20)
   * @returns {Promise} {recommendations: [], strategy: string, count: number, user_ratings_count: number}
   */
  getRecommendations: async (limit = 20) => {
    const response = await apiClient.get(`/recommendations/`, {
      params: { limit }
    });
    return response.data;
  },
};

export default recommendationsAPI;

