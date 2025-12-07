import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Navbar from '../components/Navbar';
import authAPI from '../api/auth';
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
        <div className="login-content">
          <div className="login-header">
            <div className="login-icon-container">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
            <h2 className="login-title">Welcome back</h2>
            <p className="login-subtitle">Sign in to your account</p>
          </div>

          {errors.general && (
            <div className="login-error">
              {errors.general}
            </div>
          )}

          <form onSubmit={handleSubmit} className="login-form">
            <Input
              label="Email"
              type="email"
              name="email"
              placeholder="email@example.com"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              iconBefore={
                <svg style={{ width: '1.25rem', height: '1.25rem', color: 'rgb(156 163 175)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                </svg>
              }
            />
            {errors.email && (
              <p className="login-field-error">{errors.email}</p>
            )}
            
            <Input
              label="Password"
              type="password"
              name="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              iconBefore={
                <svg style={{ width: '1.25rem', height: '1.25rem', color: 'rgb(156 163 175)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              }
            />
            {errors.password && (
              <p className="login-field-error">{errors.password}</p>
            )}

            <Button type="submit" loading={loading} size="lg" className="login-submit-button">
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>

            <div className="login-footer">
              <p className="login-footer-text">
                Don't have an account?{' '}
                <button 
                  type="button"
                  onClick={() => navigate('/register')}
                  className="login-footer-link"
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
