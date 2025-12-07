import React from 'react';

const Button = ({ 
  variant = 'primary', 
  size = 'md', 
  loading = false,
  children, 
  className = '', 
  ...props 
}) => {
  const base = 'font-semibold rounded-2xl transition-all duration-200 inline-flex items-center justify-center gap-2 shadow-lg hover:shadow-xl';
  const variants = {
    primary: 'gradient-btn text-white border-0',
    secondary: 'bg-white/20 hover:bg-white/30 text-white border border-white/30',
    danger: 'bg-red-500/90 hover:bg-red-600 text-white border-0'
  };
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-8 py-4 text-lg',
    lg: 'px-12 py-5 text-xl'
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${sizes[size]} ${loading ? 'opacity-75 cursor-not-allowed' : ''} ${className}`}
      disabled={loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin -ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" pathLength="1" className="opacity-25" />
          <path d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" stroke="currentColor" strokeWidth="4" pathLength="1" className="opacity-75" />
        </svg>
      )}
      {children}
    </button>
  );
};

export default Button;

