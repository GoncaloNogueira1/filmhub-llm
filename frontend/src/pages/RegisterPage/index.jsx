import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import authAPI from '../../api/auth';
import Navbar from '../../components/Navbar';
import './RegisterPage.css';

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
      <Navbar />
      <div className="register-container">
        <div className="register-card">
          <h2 className="register-title">Create Account</h2>
          
          {successMessage && (
            <div className="register-success">
              {successMessage}
            </div>
          )}

          {errors.general && (
            <div className="register-error">
              {errors.general}
            </div>
          )}

          <form onSubmit={handleSubmit} className="register-form">
            <div className="register-field">
              <label htmlFor="email" className="register-label">Email Address</label>
              <input
                id="email"
                type="email"
                name="email"
                placeholder="email@example.com"
                value={formData.email}
                onChange={handleChange}
                className="register-input"
                autoComplete="email"
              />
              {errors.email && (
                <p className="register-field-error">{errors.email}</p>
              )}
            </div>

            <div className="register-field">
              <label htmlFor="password" className="register-label">Password</label>
              <input
                id="password"
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                className="register-input"
                autoComplete="new-password"
              />
              {errors.password && (
                <p className="register-field-error">{errors.password}</p>
              )}
            </div>

            <div className="register-field">
              <label htmlFor="confirmPassword" className="register-label">Confirm Password</label>
              <input
                id="confirmPassword"
                type="password"
                name="confirmPassword"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="register-input"
                autoComplete="new-password"
              />
              {errors.confirmPassword && (
                <p className="register-field-error">{errors.confirmPassword}</p>
              )}
            </div>

            <div className="register-field">
              <label className="register-label">Age (Optional)</label>
              <input
                type="number"
                name="age"
                placeholder="25"
                min="13"
                max="120"
                value={formData.age}
                onChange={handleChange}
                className="register-input"
              />
              {errors.age && (
                <p className="register-field-error">{errors.age}</p>
              )}
            </div>

            <button type="submit" disabled={isLoading} className="register-button">
              {isLoading ? 'Creating account...' : 'Create Account'}
            </button>

            <div className="register-footer">
              <p>
                Already have an account?{' '}
                <button 
                  type="button"
                  onClick={() => navigate('/login')}
                  className="register-link"
                >
                  Sign in
                </button>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
