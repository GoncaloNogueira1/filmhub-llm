import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';
import authAPI from '../api/auth';
import './ProfilePage.css';

const ProfilePage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const [profile, setProfile] = useState({ name: '', age: '', genre_preferences: {} });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    fetchProfile();
  }, [isAuthenticated, navigate]);

  const fetchProfile = async () => {
    try {
      const data = await authAPI.getProfile();
      setProfile(data);
    } catch (error) {
      console.error('Failed to fetch profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    try {
      await authAPI.updateProfile({
        name: profile.name,
        age: profile.age,
        genre_preferences: profile.genre_preferences
      });
      setMessage('Profile updated successfully!');
      fetchProfile();
    } catch (error) {
      setMessage('Error updating profile. Please check your data.');
      console.error('Update error:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleGenreChange = (genreId, value) => {
    setProfile(prev => ({
      ...prev,
      genre_preferences: {
        ...prev.genre_preferences,
        [genreId]: parseFloat(value)
      }
    }));
  };

  if (loading) return <div className="profile-loading">Loading...</div>;

  const genres = [
    { id: '28', name: 'Action' }, { id: '12', name: 'Adventure' }, { id: '16', name: 'Animation' },
    { id: '35', name: 'Comedy' }, { id: '80', name: 'Crime' }, { id: '99', name: 'Documentary' },
    { id: '18', name: 'Drama' }, { id: '10751', name: 'Family' }, { id: '14', name: 'Fantasy' },
    { id: '36', name: 'History' }, { id: '27', name: 'Horror' }, { id: '10402', name: 'Music' },
    { id: '9648', name: 'Mystery' }, { id: '10749', name: 'Romance' }, { id: '878', name: 'Sci-Fi' },
    { id: '10770', name: 'TV Movie' }, { id: '53', name: 'Thriller' }, { id: '10752', name: 'War' },
    { id: '37', name: 'Western' }
  ];

  return (
    <div className="profile-page">
      <div className="profile-container">
        <h1 className="profile-title">Edit Profile</h1>
        
        {message && (
          <div className={`profile-message ${message.includes('successfully') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="profile-form">
          <div className="profile-field">
            <label className="profile-label">Name</label>
            <input
              type="text"
              value={profile.name}
              onChange={(e) => setProfile({...profile, name: e.target.value})}
              className="profile-input"
              placeholder="Enter your name"
              required
            />
          </div>

          <div className="profile-field">
            <label className="profile-label">Age</label>
            <input
              type="number"
              value={profile.age}
              onChange={(e) => setProfile({...profile, age: e.target.value})}
              className="profile-input"
              placeholder="Enter your age"
              min="13"
              max="120"
              required
            />
          </div>

          <div className="profile-field">
            <label className="profile-genres-label">Genre Preferences</label>
            <div className="profile-genres-grid">
              {genres.map((genre) => (
                <div key={genre.id} className="profile-genre-item">
                  <label className="profile-genre-label">{genre.name}</label>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={profile.genre_preferences[genre.id] || 0}
                      onChange={(e) => handleGenreChange(genre.id, e.target.value)}
                      className="profile-genre-slider"
                    />
                    <span className="profile-genre-value">{(profile.genre_preferences[genre.id] || 0).toFixed(1)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={saving}
            className="profile-submit"
          >
            {saving ? 'Saving...' : 'Save Profile'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProfilePage;
