// AuthContext.js
import React, { createContext, useState, useEffect } from 'react';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [isSignedIn, setIsSignedIn] = useState(() => {
  
    return localStorage.getItem('isSignedIn') === 'true';
  });

  const [userPk, setUserPk] = useState(() => {
    return localStorage.getItem('userPk');
  });

  useEffect(() => {
    localStorage.setItem('isSignedIn', isSignedIn);
  }, [isSignedIn]);

  useEffect(() => {
    localStorage.setItem('userPk', userPk);
  }, [userPk]);

  return (
    <AuthContext.Provider value={{ isSignedIn, setIsSignedIn, userPk, setUserPk }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
