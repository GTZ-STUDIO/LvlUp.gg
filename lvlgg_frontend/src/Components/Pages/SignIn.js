import React from 'react';
import {Link} from 'react-router-dom';

const SignIn = () => {
  const handleSignIn = () => {
    // Handle sign-in logic here
    console.log('Signing in...');
  };

  return (
    <div className='signin'>
      <div>
        <label htmlFor="username">Username:</label>
        <input type="text" id="username" name="username" />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input type="password" id="password" name="password" />
      </div>
      <button onClick={handleSignIn}>Sign In</button>
      <Link to='/signup' className='btn-mobile'>
        <button>Sign Up</button>
      </Link>
    
    </div>
  );
};

export default SignIn;