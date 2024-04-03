import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import SignUp from '../../Components/Pages/SignUp.js';
import axios from 'axios';

const backendUrl = process.env.REACT_APP_BACKEND_URL;

jest.mock('axios');

test('renders SignUp component', () => {
  render(<SignUp />);
  const usernameInput = screen.getByLabelText('Username:');
  const emailInput = screen.getByLabelText('Email:');
  const passwordInput = screen.getByLabelText('Password:');
  const firstNameInput = screen.getByLabelText('FirstName:');
  const lastNameInput = screen.getByLabelText('LastName:');
  const button = screen.getByText('Create Account');

  expect(usernameInput).toBeInTheDocument();
  expect(emailInput).toBeInTheDocument();
  expect(passwordInput).toBeInTheDocument();
  expect(firstNameInput).toBeInTheDocument();
  expect(lastNameInput).toBeInTheDocument();
  expect(button).toBeInTheDocument();
});

test('allows user to sign up', async () => {
  render(<SignUp />);
  const usernameInput = screen.getByLabelText('Username:');
  const emailInput = screen.getByLabelText('Email:');
  const passwordInput = screen.getByLabelText('Password:');
  const firstNameInput = screen.getByLabelText('FirstName:');
  const lastNameInput = screen.getByLabelText('LastName:');
  const button = screen.getByText('Create Account');

  fireEvent.change(usernameInput, { target: { value: 'testuser' } });
  fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
  fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
  fireEvent.change(firstNameInput, { target: { value: 'Test' } });
  fireEvent.change(lastNameInput, { target: { value: 'User' } });

  axios.post.mockResolvedValueOnce({ status: 200, data: { message: 'Account created successfully' } });

  fireEvent.click(button);

  await waitFor(() => {
    expect(axios.post).toHaveBeenCalledWith(`${backendUrl}/account/signup/`, {
      username: 'testuser',
      email: 'test@example.com',
      password: 'testpassword',
      firstname: 'Test',
      lastname: 'User'
    });
  });
});
