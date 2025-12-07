import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import authAPI from '../../api/auth';
import '../RegisterPage.css';

const RegisterPage = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    age: '',
  });
  
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (formData.age && (formData.age < 13 || formData.age > 120)) {
      newErrors.age = 'Age must be between 13 and 120';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      const userData = {
        email: formData.email,
        password: formData.password,
      };
      
      if (formData.age) {
        userData.age = parseInt(formData.age);
      }

      await authAPI.register(userData);
      
      setSuccessMessage('Registration successful! Redirecting to login...');
      
      setTimeout(() => {
        navigate('/login');
      }, 2000);
      
    } catch (error) {
      if (error.response?.data) {
        const serverErrors = {};
        Object.keys(error.response.data).forEach(key => {
          if (Array.isArray(error.response.data[key])) {
            serverErrors[key] = error.response.data[key][0];
          } else {
            serverErrors[key] = error.response.data[key];
          }
        });
        setErrors(serverErrors);
      } else {
        setErrors({ general: 'Registration failed. Please try again.' });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-header">
          <h1 className="register-title">🎬 FilmHub</h1>
          <h2 className="register-subtitle">Create Account</h2>
          <p className="register-description">Join FilmHub to discover your next favorite movie</p>
        </div>

        {successMessage && (
          <div className="register-message success">
            {successMessage}
          </div>
        )}

        {errors.general && (
          <div className="register-message error">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit} className="register-form">
          <div className="register-field">
            <label htmlFor="email" className="register-label">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              value={formData.email}
              onChange={handleChange}
              className={`register-input ${errors.email ? 'error' : ''}`}
              placeholder="you@example.com"
            />
            {errors.email && (
              <p className="register-field-error">{errors.email}</p>
            )}
          </div>

          <div className="register-field">
            <label htmlFor="password" className="register-label">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              value={formData.password}
              onChange={handleChange}
              className={`register-input ${errors.password ? 'error' : ''}`}
              placeholder="••••••••"
            />
            {errors.password && (
              <p className="register-field-error">{errors.password}</p>
            )}
          </div>

          <div className="register-field">
            <label htmlFor="confirmPassword" className="register-label">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              autoComplete="new-password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className={`register-input ${errors.confirmPassword ? 'error' : ''}`}
              placeholder="••••••••"
            />
            {errors.confirmPassword && (
              <p className="register-field-error">{errors.confirmPassword}</p>
            )}
          </div>

          <div className="register-field">
            <label htmlFor="age" className="register-label">
              Age (Optional)
            </label>
            <input
              id="age"
              name="age"
              type="number"
              min="13"
              max="120"
              value={formData.age}
              onChange={handleChange}
              className={`register-input ${errors.age ? 'error' : ''}`}
              placeholder="25"
            />
            {errors.age && (
              <p className="register-field-error">{errors.age}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="register-submit"
          >
            {isLoading ? (
              <span className="register-submit-loading">
                <svg className="register-submit-spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating account...
              </span>
            ) : (
              'Create Account'
            )}
          </button>

          <div className="register-footer">
            <p className="register-footer-text">
              Already have an account?{' '}
              <Link to="/login" className="register-footer-link">
                Sign in
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
