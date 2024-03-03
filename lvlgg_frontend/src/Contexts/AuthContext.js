// AuthContext.js
import React, { createContext, useState, useEffect } from 'react';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [isSignedIn, setIsSignedIn] = useState(() => {
    // Initialize isSignedIn from local storage, defaulting to false
    return localStorage.getItem('isSignedIn') === 'true';
  });

  const [userPk, setUserPk] = useState(() => {
    // Initialize userPk from local storage, defaulting to null
    return localStorage.getItem('userPk');
  });

  useEffect(() => {
    // Update local storage when isSignedIn changes
    localStorage.setItem('isSignedIn', isSignedIn);
  }, [isSignedIn]);

  useEffect(() => {
    // Update local storage when userPk changes
    localStorage.setItem('userPk', userPk);
  }, [userPk]);

  return (
    <AuthContext.Provider value={{ isSignedIn, setIsSignedIn, userPk, setUserPk }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
