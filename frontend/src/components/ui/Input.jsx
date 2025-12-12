import React from 'react';
import './Input.css';

const Input = ({ 
  label, 
  iconBefore, 
  className = '', 
  ...props 
}) => (
  <div className="input-group">
    {label && (
      <label className="input-label">
        {label}
      </label>
    )}
    <div className="input-wrapper">
      {iconBefore && (
        <div className="input-icon-before">
          {iconBefore}
        </div>
      )}
      <input
        className={`input-field ${iconBefore ? 'input-with-icon' : ''} ${className}`}
        {...props}
      />
    </div>
  </div>
);

export default Input;

