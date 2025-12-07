import { create } from 'zustand';
import { getMovies } from '../api/movies';

export const useMoviesStore = create((set, get) => ({
  movies: [],
  searchQuery: '',
  currentPage: 1,
  hasMore: true,
  loading: false,
  currentMovie: null,

  fetchMovies: async (page = 1) => {
    const currentState = get();
    if (currentState.loading) {
      return;
    }
    
    set({ loading: true });
    try {
      const data = await getMovies(page);
      const results = data.results || [];
      
      const currentMovies = currentState.movies;
      const newMovies = page === 1 ? results : [...currentMovies, ...results];
      
      set({
        movies: newMovies,
        currentPage: page,
        hasMore: results.length === 20 && data.next !== null,
        searchQuery: '',
        loading: false
      });
    } catch (error) {
      console.error('Error fetching movies:', error);
      set({ loading: false, hasMore: false });
    }
  },

  setSearchQuery: (query) => {
    set({ searchQuery: query });
  },

  searchMovies: async (page = 1, query = null) => {
    if (get().loading) return;
    
    const searchQuery = query !== null ? query : get().searchQuery;
    set({ loading: true, searchQuery });
    
    try {
      const data = await getMovies(page, searchQuery);
      const results = data.results || [];
      set({
        movies: page === 1 ? results : [...get().movies, ...results],
        currentPage: page,
        hasMore: results.length === 20 && data.next !== null,
        loading: false
      });
    } catch (error) {
      console.error('Error searching movies:', error);
      set({ loading: false, hasMore: false });
    }
  },

  clearSearch: () => {
    set({ movies: [], searchQuery: '', currentPage: 1, hasMore: true });
  },

  setCurrentMovie: (movie) => set({ currentMovie: movie })
}));
