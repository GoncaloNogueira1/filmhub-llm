import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';
import authAPI from '../api/auth';
import './ProfilePage.css';

const ProfilePage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const [profile, setProfile] = useState({ first_name: '', last_name: '', age: '' });
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
      setProfile({
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        age: data.age || ''
      });
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
        first_name: profile.first_name,
        last_name: profile.last_name,
        age: profile.age ? parseInt(profile.age) : null
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

  if (loading) return <div className="profile-loading">Loading...</div>;

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
            <label className="profile-label">First Name</label>
            <input
              type="text"
              value={profile.first_name || ''}
              onChange={(e) => setProfile({...profile, first_name: e.target.value})}
              className="profile-input"
              placeholder={profile.first_name ? '' : 'Your first name'}
            />
          </div>

          <div className="profile-field">
            <label className="profile-label">Last Name</label>
            <input
              type="text"
              value={profile.last_name || ''}
              onChange={(e) => setProfile({...profile, last_name: e.target.value})}
              className="profile-input"
              placeholder={profile.last_name ? '' : 'Your last name'}
            />
          </div>

          <div className="profile-field">
            <label className="profile-label">Age</label>
            <input
              type="number"
              value={profile.age || ''}
              onChange={(e) => setProfile({...profile, age: e.target.value})}
              className="profile-input"
              placeholder={profile.age ? '' : 'Your age'}
              min="13"
              max="120"
            />
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
