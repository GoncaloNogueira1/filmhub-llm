import apiClient from './axios'; // Usa o axios existente

export const getMovies = async (page = 1, query = '') => {
  const params = new URLSearchParams({ page: page.toString(), page_size: '20' });
  if (query) params.append('q', query);
  
  const response = await apiClient.get(`/movies/?${params}`);
  return response.data;
};

export const getMovieDetail = async (movieId) => {
  const response = await apiClient.get(`/movies/${movieId}/`);
  return response.data;
};
