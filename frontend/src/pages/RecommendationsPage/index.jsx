import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import MovieCard from '../components/MovieCard';
import recommendationsAPI from '../api/recommendations';
import './RecommendationsPage.css';

const RecommendationsPage = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [strategy, setStrategy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userRatingsCount, setUserRatingsCount] = useState(0);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await recommendationsAPI.getRecommendations(20);
      setRecommendations(data.recommendations || []);
      setStrategy(data.strategy);
      setUserRatingsCount(data.user_ratings_count || 0);
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      setError('Error loading recommendations');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-center py-32">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-3 border-blue-500 border-t-transparent mb-4"></div>
            <p className="text-gray-300">Loading recommendations...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="text-center py-32">
          <p className="text-red-400 text-lg mb-4">{error}</p>
          <button
            onClick={fetchRecommendations}
            className="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  const isColdStart = strategy === 'cold-start';

  return (
    <div className="recommendations-page">
      {/* Header */}
      <div className="recommendations-header">
        <h1 className="recommendations-title">
          Recommendations for You
        </h1>
        <p className="recommendations-subtitle">
          {isColdStart ? (
            <>
              Rate some movies to receive personalized recommendations
              {userRatingsCount > 0 && ` (${userRatingsCount} rating${userRatingsCount !== 1 ? 's' : ''} so far)`}
            </>
          ) : (
            <>
              Based on your {userRatingsCount} rating{userRatingsCount !== 1 ? 's' : ''}
            </>
          )}
        </p>
      </div>

      {/* Cold Start Message */}
      {isColdStart && (
        <div className="recommendations-cold-start">
          <div className="recommendations-cold-start-content">
            <div className="recommendations-cold-start-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="recommendations-cold-start-text">
              <h3 className="recommendations-cold-start-title">Start rating movies!</h3>
              <p className="recommendations-cold-start-description">
                Rate at least 3 movies to receive personalized recommendations based on your preferences.
              </p>
              <Link
                to="/movies"
                className="recommendations-cold-start-link"
              >
                Explore movies →
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Recommendations Grid */}
      {recommendations.length === 0 ? (
        <div className="recommendations-empty">
          <div className="recommendations-empty-emoji">🎬</div>
          <h2 className="recommendations-empty-title">No recommendations available</h2>
          <p className="recommendations-empty-text">Rate more movies to receive recommendations</p>
          <Link
            to="/movies"
            className="recommendations-empty-button"
          >
            Explore Movies
          </Link>
        </div>
      ) : (
        <>
          <div className="recommendations-count">
            {recommendations.length} recommendation{recommendations.length !== 1 ? 's' : ''} found
          </div>
          
          <div className="recommendations-grid">
            {recommendations.map((movie) => (
              <div key={movie.id} className="recommendations-movie">
                <MovieCard movie={movie} />
                {/* Predicted Score Badge */}
                {movie.predicted_score && (
                  <div className="recommendations-predicted-score">
                    <div className="recommendations-predicted-score-badge">
                      {movie.predicted_score.toFixed(1)} match
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default RecommendationsPage;

