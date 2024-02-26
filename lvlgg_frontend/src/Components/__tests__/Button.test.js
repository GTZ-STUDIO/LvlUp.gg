import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter as Router } from 'react-router-dom'
import { MemoryRouter } from 'react-router-dom';
import { Button } from '../../Components/Button.js';

test('renders button component', () => {
    const { getByText } = render(
        <MemoryRouter>
            <Button>Click me</Button>
        </MemoryRouter>
    );
    const buttonElement = getByText('Click me');
    expect(buttonElement).toBeInTheDocument();
});

test('renders button component with correct style and size', () => {
    const { container } = render(
        <Router>
            <Button buttonStyle="btn--primary" buttonSize="btn--medium">Click me</Button>
        </Router>
    );
    const buttonElement = container.querySelector('button');
    expect(buttonElement).toHaveClass('btn');
    expect(buttonElement).toHaveClass('btn--primary');
});
