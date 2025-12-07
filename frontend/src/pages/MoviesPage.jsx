import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useInView } from 'react-intersection-observer';
import { useMoviesStore } from '../stores/moviesStore';
import SearchBar from '../components/SearchBar';
import MovieCard from '../components/MovieCard';
import './MoviesPage.css';

const MoviesPage = () => {
  const { 
    movies, 
    searchQuery, 
    hasMore, 
    loading, 
    fetchMovies, 
    searchMovies,
    clearSearch 
  } = useMoviesStore();
  
  const [ref, inView] = useInView({ threshold: 0.1 });

  // Initial load - only once on mount
  useEffect(() => {
    if (movies.length === 0 && !loading) {
      fetchMovies(1);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty dependency array - only run on mount

  // Infinite scroll
  useEffect(() => {
    if (inView && hasMore && !loading && movies.length > 0) {
      const nextPage = Math.floor(movies.length / 20) + 1;
      if (searchQuery) {
        searchMovies(nextPage);
      } else {
        fetchMovies(nextPage);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [inView, hasMore, loading, movies.length, searchQuery]);

  const handleSearch = useCallback((query) => {
    if (query && query.trim()) {
      searchMovies(1, query);
    } else {
      // Don't clear search, just fetch movies
      fetchMovies(1);
    }
  }, [searchMovies, fetchMovies]);

  if (loading && movies.length === 0) {
    return (
      <div className="movies-page">
        <div className="movies-loading-container">
          <div className="movies-loading-content">
            <div className="movies-spinner"></div>
            <p className="movies-loading-text">Loading movies...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="movies-page">
      {/* Compact Search */}
      <div className="movies-search">
          <SearchBar onSearch={handleSearch} />
        </div>

      {/* Movies Grid */}
      {loading && movies.length === 0 ? (
        <div className="movies-loading-container">
          <div className="movies-loading-content">
            <div className="movies-spinner"></div>
            <p className="movies-loading-text">Loading movies...</p>
          </div>
        </div>
      ) : movies.length === 0 ? (
        <div className="movies-empty">
          <p className="movies-empty-text">No movies found</p>
          </div>
        ) : (
          <>
          {searchQuery && (
            <div className="movies-results">
              {movies.length} result{movies.length !== 1 ? 's' : ''} for "{searchQuery}"
            </div>
          )}
          
          <div className="movies-grid">
              {movies.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
            
            {loading && (
            <div className="movies-loading-more">
              <div className="movies-loading-more-spinner"></div>
              </div>
            )}
            
          <div ref={ref} className="movies-infinite-scroll" />
          </>
        )}
    </div>
  );
};

export default MoviesPage;
