import React from 'react';
import './Button.css';

const Button = ({ 
  variant = 'primary', 
  size = 'md', 
  loading = false,
  children, 
  className = '', 
  ...props 
}) => {
  const variantClass = `button-${variant}`;
  const sizeClass = `button-${size}`;

  return (
    <button
      className={`button ${variantClass} ${sizeClass} ${className}`}
      disabled={loading}
      {...props}
    >
      {loading && (
        <svg className="button-spinner" fill="none" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" pathLength="1" />
          <path d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" stroke="currentColor" strokeWidth="4" pathLength="1" />
        </svg>
      )}
      {children}
    </button>
  );
};

export default Button;

