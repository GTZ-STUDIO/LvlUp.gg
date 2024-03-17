import React, { useState, useEffect, useContext } from 'react';
import '../../App.css';
import axios from "axios";
import { AuthContext } from '../../Contexts/AuthContext'

export default function MyGuides() {
  const { userPk } = useContext(AuthContext);
  const [blogs, setBlogs] = useState([]);

  const gameImageMap = {
    "EldenRing": "images/eldenRing.png",
    "LeagueOfLegends": "images/league.png",
    "Dota2": "images/dota.jpg",
    "CSGO": "images/csgo.jpg",
    "BaldursGate3": "images/baldursGate.jpeg",
  };

  useEffect(() => {
    axios.get(`http://localhost:8000/blog/get_blog/${userPk}/`, {
      withCredentials: true
    })
    .then(response => {
      if(response.status === 200) {
        console.log('got all blogs successfully');
        setBlogs(response.data); // Assuming response.data is an array of blogs
      } else {
        console.log('unsuccessful');
      }
    })
    .catch(error => {
      console.error('Error getting blogs:', error);
    });
  }, [userPk]);

  const handleDelete = (blogId) => {
    axios.delete(`http://localhost:8000/blog/delete_blog/${blogId}/`, {
      withCredentials: true
    })
    .then(response => {
      if(response.status === 204) {
        console.log('blog deleted successfully');
        setBlogs(blogs.filter(blog => blog.id !== blogId));
      } else {
        console.log('unsuccessful');
      }
    })
    .catch(error => {
      console.error('Error deleting blog:', error);
    });
  };

  return (
    <div className='guides'>
      <ul className='guide-list'>
        {blogs.map(blog => (
          <li key={blog.id} onClick={() => handleDelete(blog.id)}>
            <div className='guide-item'>
              <img src={gameImageMap[blog.game] || 'images/img-home.jpg'} alt={blog.title} className="guide-image"/>
              <div className='guide-title'>{blog.title}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
