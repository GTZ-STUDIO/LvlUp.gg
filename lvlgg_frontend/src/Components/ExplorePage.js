import React from 'react'
import '../App.css'
import './ExplorePage.css'


function ExplorePage() {
  return (
    <div className='explore-container'>
      <video data-testid="video-element" src="/videos/video-6.mp4" autoPlay loop muted />    
    </div>
  )
}

export default ExplorePage
