import React from 'react';

const Input = ({ 
  label, 
  iconBefore, 
  className = '', 
  ...props 
}) => (
  <div className="relative group">
    {label && (
      <label className="absolute -top-3 left-3 px-2 text-sm text-white/80 bg-slate-900/50 backdrop-blur-sm rounded-md transition-all group-focus-within:text-blue-400">
        {label}
      </label>
    )}
    <div className="relative">
      {iconBefore && (
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          {iconBefore}
        </div>
      )}
      <input
        className={`w-full px-4 py-5 ${iconBefore ? 'pl-12' : ''} pr-12 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-gray-300 text-lg input-focus transition-all group-hover:border-white/40 peer ${className}`}
        {...props}
      />
    </div>
  </div>
);

export default Input;

