import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import Button from '../components/ui/Button';
import './NotFound.css';

const NotFound = () => {
  return (
    <Layout>
      <div className="not-found-container">
        <div className="not-found-content">
          <div className="not-found-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="not-found-title">404</h1>
          <h2 className="not-found-subtitle">Page Not Found</h2>
          <p className="not-found-description">
            The page you're looking for doesn't exist or has been moved.
          </p>
          <div className="not-found-actions">
            <Link to="/movies">
              <Button size="lg">Go to Movies</Button>
            </Link>
            <Link to="/">
              <Button variant="secondary" size="lg">Go Home</Button>
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default NotFound;

