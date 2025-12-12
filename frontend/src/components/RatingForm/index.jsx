import React, { useState, useEffect } from 'react';
import ratingsAPI from '../../api/ratings';
import './RatingForm.css';

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
        // Only log non-404 errors (404 is expected when user hasn't rated)
        if (err.response?.status !== 404) {
        console.error('Error loading user rating:', err);
        }
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
      <div className="rating-form-loading">
        <div className="rating-form-spinner"></div>
      </div>
    );
  }

  return (
    <div className="rating-form-container">
      <h3 className="rating-form-title">
        {userRating ? 'Update Rating' : 'Rate Movie'}
      </h3>

      <form onSubmit={handleSubmit} className="rating-form">
        {/* Star Rating */}
        <div className="rating-section">
          <label className="rating-label">Rating</label>
          <div className="rating-controls">
            <div className="rating-stars-container">
            {[1, 2, 3, 4, 5].map((value) => (
              <button
                key={value}
                type="button"
                onClick={() => handleStarClick(value)}
                onMouseEnter={() => setHoveredRating(value)}
                onMouseLeave={() => setHoveredRating(0)}
                  className="rating-star-button"
                aria-label={`Rate ${value} star${value !== 1 ? 's' : ''}`}
              >
                <svg
                    className={`rating-star ${
                    value <= (hoveredRating || rating)
                        ? 'active'
                        : 'inactive'
                    } ${hoveredRating >= value ? 'hovered' : ''}`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                    stroke="currentColor"
                    strokeWidth="0.5"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </button>
            ))}
            </div>
            {rating > 0 && (
              <span className="rating-value-badge">
                {rating}/5
              </span>
            )}
            {rating === 0 && (
              <span className="rating-hint">
                Click to rate
              </span>
            )}
          </div>
        </div>

        {/* Comment Field */}
        <div className="comment-section">
          <label htmlFor="comment" className="comment-label">
            Comment (optional)
          </label>
          <textarea
            id="comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={3}
            className="comment-textarea"
            placeholder="Share your thoughts about this movie..."
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="rating-error">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={submitting || rating === 0}
          className="rating-submit-button"
        >
          {submitting ? 'Saving...' : userRating ? 'Update Rating' : 'Submit Rating'}
        </button>
      </form>
    </div>
  );
};

export default RatingForm;

