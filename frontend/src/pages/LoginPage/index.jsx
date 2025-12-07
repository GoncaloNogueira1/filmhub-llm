import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Navbar from '../components/Navbar';
import authAPI from '../api/auth';

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
    <div className="min-h-screen">
      <Navbar />
      <div className="flex items-center justify-center p-4 min-h-[calc(100vh-80px)]">
        <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <div className="mx-auto h-24 w-24 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-3xl flex items-center justify-center mb-6 shadow-2xl">
            <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </div>
          <h2 className="text-4xl font-bold text-white mb-4">Welcome back</h2>
          <p className="text-gray-300">Sign in to your account</p>
        </div>

        {errors.general && (
          <div className="bg-red-500/90 text-white px-4 py-3 rounded-xl">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit} className="glass-card p-10 space-y-6">
          <Input
            label="Email"
            type="email"
            name="email"
            placeholder="email@example.com"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            iconBefore={
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
              </svg>
            }
          />
          {errors.email && (
            <p className="text-sm text-red-400 -mt-4">{errors.email}</p>
          )}
          
          <Input
            label="Password"
            type="password"
            name="password"
            placeholder="••••••••"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            iconBefore={
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            }
          />
          {errors.password && (
            <p className="text-sm text-red-400 -mt-4">{errors.password}</p>
          )}

          <Button type="submit" loading={loading} size="lg" className="w-full">
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>

          <div className="text-center">
            <p className="text-gray-300">
              Don't have an account?{' '}
              <button 
                type="button"
                onClick={() => navigate('/register')}
                className="font-semibold text-blue-400 hover:text-blue-300 transition-colors"
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
