import React, { useState, useEffect } from 'react';
import ratingsAPI from '../../api/ratings';

const RatingForm = ({ movieId, onRatingSubmitted }) => {
  const [rating, setRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [userRating, setUserRating] = useState(null);

  // Load existing user rating
  useEffect(() => {
    const loadUserRating = async () => {
      setLoading(true);
      try {
        const existingRating = await ratingsAPI.getUserRating(movieId);
        if (existingRating) {
          setUserRating(existingRating);
          setRating(existingRating.score);
          setComment(existingRating.comment || '');
        }
      } catch (err) {
        console.error('Error loading user rating:', err);
      } finally {
        setLoading(false);
      }
    };

    if (movieId) {
      loadUserRating();
    }
  }, [movieId]);

  const handleStarClick = (value) => {
    setRating(value);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (rating === 0) {
      setError('Please select a rating');
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const ratingData = {
        score: rating,
        ...(comment.trim() && { comment: comment.trim() })
      };

      const result = await ratingsAPI.rateMovie(movieId, ratingData);
      setUserRating(result);
      
      // Callback to refresh recommendations
      if (onRatingSubmitted) {
        onRatingSubmitted(result);
      }
    } catch (err) {
      setError(err.response?.data?.score?.[0] || err.response?.data?.non_field_errors?.[0] || 'Error rating movie');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-4">
        <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
      <h3 className="text-lg font-semibold text-white mb-4">
        {userRating ? 'Update Rating' : 'Rate Movie'}
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Star Rating */}
        <div>
          <label className="block text-sm text-gray-300 mb-2">Rating</label>
          <div className="flex items-center gap-2">
            {[1, 2, 3, 4, 5].map((value) => (
              <button
                key={value}
                type="button"
                onClick={() => handleStarClick(value)}
                onMouseEnter={() => setHoveredRating(value)}
                onMouseLeave={() => setHoveredRating(0)}
                className="focus:outline-none transition-transform hover:scale-110 active:scale-95"
                aria-label={`Rate ${value} star${value !== 1 ? 's' : ''}`}
              >
                <svg
                  className={`w-8 h-8 transition-colors ${
                    value <= (hoveredRating || rating)
                      ? 'text-yellow-400 fill-current'
                      : 'text-gray-500 fill-none'
                  }`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </button>
            ))}
            {rating > 0 && (
              <span className="ml-2 text-sm text-gray-400">
                {rating}/5
              </span>
            )}
          </div>
        </div>

        {/* Comment Field */}
        <div>
          <label htmlFor="comment" className="block text-sm text-gray-300 mb-2">
            Comment (optional)
          </label>
          <textarea
            id="comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={3}
            className="w-full px-4 py-2 bg-slate-900/50 border border-slate-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none"
            placeholder="Share your thoughts about this movie..."
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-300 px-4 py-2 rounded-lg text-sm">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={submitting || rating === 0}
          className="w-full py-2.5 px-4 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:from-blue-500 disabled:hover:to-purple-600"
        >
          {submitting ? 'Saving...' : userRating ? 'Update Rating' : 'Submit Rating'}
        </button>
      </form>
    </div>
  );
};

export default RatingForm;

