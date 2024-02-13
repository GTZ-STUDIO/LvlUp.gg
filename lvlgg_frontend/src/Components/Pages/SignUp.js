import React, { useState } from 'react';
import axios from 'axios';

const SignUp = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignUp = () => {
    console.log('Sending Data');
    axios.post('http://localhost:8000/create/', {
      username,
      email,
      password,
    })
    .then(response => {
      console.log('Account created successfully:', response.data);
      // Redirect or perform other actions upon successful account creation
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  return (
    <div className='signup'>
      <div>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
      </div>
      <button onClick={handleSignUp}>Create Account</button>
    </div>
  );
};

export default SignUp;