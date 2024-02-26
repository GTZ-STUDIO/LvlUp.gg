import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect'; // import the extend-expect library
import ExplorePage from '../../Components/ExplorePage.js';

test('renders ExplorePage component', () => {
    const { getByTestId } = render(<ExplorePage />);
    const videoElement = getByTestId('video-element');
    expect(videoElement).toBeInTheDocument();
});


test('renders video element with correct attributes', () => {
    const { getByTestId } = render(<ExplorePage />);
    const videoElement = getByTestId('video-element');
    expect(videoElement).toBeInTheDocument();
    expect(videoElement).toHaveAttribute('src', '/videos/video-6.mp4');
    expect(videoElement).toHaveAttribute('autoplay');
    expect(videoElement).toHaveAttribute('loop');
});

