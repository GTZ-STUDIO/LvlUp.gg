import React, { useState, useEffect, useContext } from 'react';
import '../../App.css';
import axios from "axios";
import { AuthContext } from '../../Contexts/AuthContext'
import { useHistory } from 'react-router-dom';

export default function MyGuides() {
  const { userPk } = useContext(AuthContext);
  const [blogs, setBlogs] = useState([]);
  const history = useHistory();

  const gameImageMap = {
    "EldenRing": "images/eldenRing.png",
    "LeagueOfLegends": "images/league.png",
    "Dota2": "images/dota.jpg",
    "CSGO": "images/csgo.jpg",
    "BaldursGate3": "images/baldursGate.jpeg",
  };

  const getCookie = (name) => {
    const cookieValue = document.cookie
      .split('; ')
      .find((row) => row.startsWith(`${name}=`));
    if (cookieValue) {
      return cookieValue.split('=')[1];
    }
    return null;
  };

  useEffect(() => {
    axios.get(`http://localhost:8000/blog/get_blog/?author=${userPk}`, {
      withCredentials: true
    })
    .then(response => {
      if(response.status === 200) {
        console.log('got all blogs successfully');   
        setBlogs(response.data.blogs); // Assuming response.data is an array of blogs   
      } else {
        console.log('unsuccessful');
      }
    })
    .catch(error => {
      console.error('Error getting blogs:', error);
    });
  }, [userPk]);

  const handleDelete = (blogId) => {
    const csrfToken = getCookie('csrftoken');
    axios.delete(`http://localhost:8000/blog/delete_blog/${blogId}/`, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      withCredentials: true
    })
    .then(response => {
      if(response.status === 200) {
        console.log('blog deleted successfully');
        setBlogs(blogs.filter(blog => blog.id !== blogId));
        alert("Guide Deleted Successfully")
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
        {blogs.length > 0 && blogs.map(blog => (
          <li key={blog.id}>
            <div className='guide-item'>
              <img src={gameImageMap[blog.game] || 'images/img-home.jpg'} alt={blog.title} className="guide-image"/>
              <button className='guide-title' onClick={() => history.push(`/blog/${blog.id}`)}>
                {blog.title}
              </button>
              <button className='myguides-btn-delete' onClick={() => handleDelete(blog.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
  
}
