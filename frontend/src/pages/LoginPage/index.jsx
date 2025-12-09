import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../../stores/authStore';
import Navbar from '../../components/Navbar';
import authAPI from '../../api/auth';
import './LoginPage.css';

const LoginPage = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();

  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/movies');
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});
    
    try {
      await authAPI.login(formData);
      navigate('/movies');
    } catch (error) {
      console.error('Login error:', error);
      if (error.response?.data) {
        const serverErrors = {};
        const data = error.response.data;
        
        if (data.non_field_errors) {
          serverErrors.general = Array.isArray(data.non_field_errors) 
            ? data.non_field_errors[0] 
            : data.non_field_errors;
        }
        
        Object.keys(data).forEach(key => {
          if (key !== 'non_field_errors') {
            serverErrors[key] = Array.isArray(data[key]) 
              ? data[key][0] 
              : data[key];
          }
        });
        
        if (Object.keys(serverErrors).length === 0) {
          serverErrors.general = 'Login failed. Please check your credentials.';
        }
        
        setErrors(serverErrors);
      } else {
        setErrors({ general: 'Login failed. Please check your credentials.' });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <Navbar />
      <div className="login-container">
        <div className="login-card">
          <h2 className="login-title">Sign In</h2>
          
          {errors.general && (
            <div className="login-error">
              {errors.general}
            </div>
          )}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="login-field">
              <label className="login-label">Email</label>
              <input
                type="email"
                name="email"
                placeholder="email@example.com"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="login-input"
              />
              {errors.email && (
                <p className="login-field-error">{errors.email}</p>
              )}
            </div>
            
            <div className="login-field">
              <label className="login-label">Password</label>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="login-input"
              />
              {errors.password && (
                <p className="login-field-error">{errors.password}</p>
              )}
            </div>

            <button type="submit" disabled={loading} className="login-button">
              {loading ? 'Signing in...' : 'Sign In'}
            </button>

            <div className="login-footer">
              <p>
                Don't have an account?{' '}
                <button 
                  type="button"
                  onClick={() => navigate('/register')}
                  className="login-link"
                >
                  Sign up
                </button>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
