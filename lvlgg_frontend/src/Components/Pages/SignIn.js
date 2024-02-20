import React, {useState} from 'react';
import {Link, useHistory} from 'react-router-dom';
import axios from 'axios';

const SignIn = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const history = useHistory();

  const handleSignIn = () => {
    // Handle sign-in logic here
    console.log('Signing in...');
    axios.get('http://localhost:8000/users/', {
      username,
      password,
    })
    .then(response => {
      console.log('Successful sign in:', response.data);
      history.push('/')
      // Redirect or perform other actions upon successful login

    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  return (
    <div className='signin'>
    <div className='signin-form'>
      <label htmlFor="username">Username:</label>
      <input type="text" id="username" name="username" className='signin-input' />
    </div>
    <div className='signin-form'>
      <label htmlFor="password">Password:</label>
      <input type="password" id="password" name="password" className='signin-input' />
    </div>
    <button onClick={handleSignIn} className='signin-button'>Sign In</button>
    <Link to='/signup' className='btn-mobile'>
      <button className='signup-button'>Sign Up</button>
    </Link>
  </div>
  );
};

export default SignIn;