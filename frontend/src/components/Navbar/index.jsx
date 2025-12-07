import React, { useState, useEffect } from 'react';
import useAuthStore from '../stores/authStore';
import useWatchlistStore from '../stores/watchlistStore';
import { Link, useNavigate } from 'react-router-dom';
import Button from './ui/Button';
import authAPI from '../api/auth';
import './Navbar.css';

const Navbar = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuthStore();
  const { count, fetchWatchlist } = useWatchlistStore();
  const navigate = useNavigate();

  // Fetch watchlist count when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchWatchlist();
    }
  }, [isAuthenticated, fetchWatchlist]);

  const handleLogout = async () => {
    await authAPI.logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/movies" className="navbar-logo">
          🎬 FilmHub
        </Link>

        <div className="navbar-links">
          {isAuthenticated ? (
            <>
              <Link to="/movies" className="navbar-link">
                Movies
              </Link>
              <Link to="/recommendations" className="navbar-link">
                Recommendations
              </Link>
              <Link 
                to="/watchlist" 
                className="navbar-link"
                style={{ position: 'relative' }}
              >
                My List
                {count > 0 && (
                  <span style={{
                    position: 'absolute',
                    top: '-4px',
                    right: '-4px',
                    backgroundColor: 'rgb(59 130 246)',
                    color: 'white',
                    fontSize: '0.75rem',
                    fontWeight: 'bold',
                    borderRadius: '50%',
                    width: '1.25rem',
                    height: '1.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    {count > 9 ? '9+' : count}
                  </span>
                )}
              </Link>
              <Link 
                to="/profile" 
                className="navbar-profile-button"
              >
                <div className="navbar-profile-icon">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <div className="navbar-profile-online"></div>
                </div>
                <div className="navbar-profile-info">
                  <span className="navbar-profile-title">Profile</span>
                  <span className="navbar-profile-username">
                    {user?.username || user?.email?.split('@')[0] || 'User'}
                  </span>
                </div>
              </Link>
              <Button onClick={handleLogout} variant="secondary" size="sm">
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="secondary" size="sm">Login</Button>
              </Link>
              <Link to="/register">
                <Button size="sm">Sign Up</Button>
              </Link>
            </>
          )}
        </div>

        <button
          className="navbar-mobile-button"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle menu"
        >
          {mobileOpen ? (
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      {mobileOpen && (
        <>
          <div 
            className="navbar-overlay"
            onClick={() => setMobileOpen(false)}
          />
          <div className={`navbar-mobile-menu ${mobileOpen ? 'open' : ''}`}>
            <div className="navbar-mobile-menu-content">
              {/* Header */}
              <div className="navbar-mobile-header">
                <h2>Menu</h2>
                <button
                  onClick={() => setMobileOpen(false)}
                  className="navbar-mobile-close"
                  aria-label="Close menu"
                >
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Menu Items */}
              <div className="navbar-mobile-items">
                {isAuthenticated ? (
                  <>
                    <Link 
                      to="/movies" 
                      onClick={() => setMobileOpen(false)}
                      className="navbar-mobile-link"
                    >
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                      </svg>
                      <span>Movies</span>
                    </Link>
                    
                    <Link 
                      to="/recommendations" 
                      onClick={() => setMobileOpen(false)}
                      className="navbar-mobile-link"
                    >
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                      <span>Recommendations</span>
                    </Link>
                    
                    <Link 
                      to="/watchlist" 
                      onClick={() => setMobileOpen(false)}
                      className="navbar-mobile-link"
                      style={{ justifyContent: 'space-between' }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                        </svg>
                        <span>My List</span>
                      </div>
                      {count > 0 && (
                        <span style={{
                          backgroundColor: 'rgb(59 130 246)',
                          color: 'white',
                          fontSize: '0.75rem',
                          fontWeight: 'bold',
                          borderRadius: '50%',
                          width: '1.5rem',
                          height: '1.5rem',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center'
                        }}>
                          {count > 9 ? '9+' : count}
                        </span>
                      )}
                    </Link>
                    
                    <Link 
                      to="/profile" 
                      onClick={() => setMobileOpen(false)}
                      className="navbar-mobile-link"
                    >
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span>Profile</span>
                    </Link>

                    {/* User Info */}
                    <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
                      <div style={{ padding: '0.5rem 1rem' }}>
                        <p style={{ fontSize: '0.75rem', color: 'rgb(156 163 175)', marginBottom: '0.25rem' }}>Signed in as</p>
                        <p style={{ fontSize: '0.875rem', fontWeight: '500', color: 'white', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {user?.username || user?.email || 'User'}
                        </p>
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    <Link 
                      to="/login" 
                      onClick={() => setMobileOpen(false)}
                      className="navbar-mobile-link"
                    >
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                      </svg>
                      <span>Login</span>
                    </Link>
                    <Link 
                      to="/register"
                      onClick={() => setMobileOpen(false)}
                      style={{ display: 'block' }}
                    >
                      <Button className="w-full" size="sm">Sign Up</Button>
                    </Link>
                  </>
                )}
              </div>

              {/* Footer - Logout button if authenticated */}
              {isAuthenticated && (
                <div className="navbar-mobile-footer">
                  <Button 
                    onClick={() => {
                      handleLogout();
                      setMobileOpen(false);
                    }} 
                    variant="danger" 
                    className="w-full" 
                    size="sm"
                  >
                    <svg style={{ width: '1rem', height: '1rem', marginRight: '0.5rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Logout
                  </Button>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </nav>
  );
};

export default Navbar;

