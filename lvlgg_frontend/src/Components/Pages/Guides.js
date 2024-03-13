import React, { useState, useEffect, useContext } from 'react';
import '../../App.css';
import { Link, useLocation, useHistory } from "react-router-dom";
import axios from "axios";
import { AuthContext } from '../../Contexts/AuthContext'


export default function Guides() {
  const {isSignedIn} = useContext(AuthContext);
  const [blogs, setBlogs] = useState([]);
  const location = useLocation();
  const game = new URLSearchParams(location.search).get('gameName');
  const history = useHistory();

  const gameImageMap = {
    "EldenRing": "images/eldenRing.png",
    "LeagueOfLegends": "images/league.png",
    "Dota2": "images/dota.jpg",
    "CSGO": "images/csgo.jpg",
    "BaldursGate3": "images/baldursGate.jpeg",
  };

  useEffect(() => {
    let url = 'http://localhost:8000/blog/get_blog/';
    if (game) {
      url = `http://localhost:8000/blog/get_blog/?game=${game}`;
    }

    axios.get(url)
      .then(response => {
        setBlogs(response.data.blogs);
      })
      .catch(error => {
        console.error('Error fetching blogs:', error);
      });
  }, [game]); 

  const handleBlogClick = (blogId) => {
    history.push(`/blog/${blogId}`);
  };

  const formatDate = (dateString) => {
    const formattedDate = new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
    return formattedDate;
  };

  return (
    <div className='guides'>
    <div className='top-right'>
      {isSignedIn ? (
        <Link to='/createguide'>
          <button className='guides-button'>Create Guide</button>
        </Link>
      ) : (
        <Link to='/signin'>
          <button className='guides-button'>Sign In To Create Guide</button>
        </Link>
      )}
    </div>
    <div className='guide-titles'>
      <h1>Guides</h1>
    </div>
    
    <ul className='guide-list'>
      {blogs.map(blog => (
        <li key={blog.id} onClick={() => handleBlogClick(blog.id)}>
          <div className='guide-item'>
            <img src={gameImageMap[blog.game] || 'images/img-home.jpg'} alt={blog.title} className="guide-image"/>
            <div className='guide-title'>{blog.title}</div>
          </div>
        </li>
      ))}
    </ul>
  </div>
  )
}
