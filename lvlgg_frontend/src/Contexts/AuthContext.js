// AuthContext.js
import React, { createContext, useState, useEffect } from 'react';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [isSignedIn, setIsSignedIn] = useState(() => {
    // Initialize isSignedIn from local storage, defaulting to false
    return localStorage.getItem('isSignedIn') === 'true';
  });

  useEffect(() => {
      // Update local storage when isSignedIn changes
      localStorage.setItem('isSignedIn', isSignedIn);
  }, [isSignedIn]);

  return (
    <AuthContext.Provider value={{ isSignedIn, setIsSignedIn }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };