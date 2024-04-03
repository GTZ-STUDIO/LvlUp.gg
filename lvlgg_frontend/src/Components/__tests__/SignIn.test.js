import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter as Router } from 'react-router-dom';
import SignIn from '../../Components/Pages/SignIn';
import axios from 'axios';
import { AuthContext, AuthProvider } from '../../Contexts/AuthContext.js';

const backendUrl = process.env.REACT_APP_BACKEND_URL;

jest.mock('axios');

test('renders SignIn component', () => {
  const mockContextValue = { setIsSignedIn: jest.fn() };

  render(
    <Router> {/* Wrap your component with BrowserRouter */}
      <AuthContext.Provider value={mockContextValue}>
        <SignIn />
      </AuthContext.Provider>
    </Router>
  );

  const usernameInput = screen.getByLabelText('Username:');
  const passwordInput = screen.getByLabelText('Password:');

  expect(usernameInput).toBeInTheDocument();
  expect(passwordInput).toBeInTheDocument();
});

test('allows user to sign in', async () => {
    render(
        <Router> {/* Wrap your component tree with Router */}
          <AuthProvider>
            <SignIn />
          </AuthProvider>
        </Router>
    );
  const usernameInput = screen.getByLabelText('Username:');
  const passwordInput = screen.getByLabelText('Password:');
  const button = screen.getByText('Sign In');

  fireEvent.change(usernameInput, { target: { value: 'testuser' } });
  fireEvent.change(passwordInput, { target: { value: 'testpassword' } });

  axios.post.mockResolvedValueOnce({ status: 200, data: { message: 'Successful login' } });

  fireEvent.click(button);

  await waitFor(() => {
    expect(axios.post).toHaveBeenCalledWith(`${backendUrl}/account/signin/`, {
      username: 'testuser',
      password: 'testpassword',
    });
  });
});
