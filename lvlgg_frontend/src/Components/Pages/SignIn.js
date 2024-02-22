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
    axios.post('http://localhost:8000/account/signin/', {
      username,
      password,
    })
    .then(response => {
      if (response.status === 200) {
        console.log('Account created successfully:', response.data);
        history.push('/')
      } else {
        console.error('Unexpected response status:', response.status);
      }

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