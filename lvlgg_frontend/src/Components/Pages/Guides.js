import React, { useState, useEffect } from 'react';
import '../../App.css';
import { Link, useLocation } from "react-router-dom";
import axios from "axios";
//import { AuthContext } from '../../Contexts/AuthContext'


export default function Guides() {
  //const {setIsSignedIn} = useContext(AuthContext);
  const [blogs, setBlogs] = useState([]);
  const [selectedBlog, setSelectedBlog] = useState(null);
  const location = useLocation();
  const game = new URLSearchParams(location.search).get('gameName');

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
    axios.get(`http://localhost:8000/blog/get_blog/?id=${blogId}`)
      .then(response => {
        console.log(response.data.blogs)
        setSelectedBlog(response.data.blogs);
        console.log(selectedBlog[0].content)
      })
      .catch(error => {
        console.error('Error fetching blog content:', error);
      });
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
      <Link to='/createguide'>
        <button className='guides-button'>Create Guide</button>
      </Link>
    </div>
    <div className='guide-titles'>
      <h1>Guides</h1>
    </div>
    {blogs.length === 0 ? (
      <p>Nothing to see here</p>
    ) : (
      <ul className='guide-list'>
        {blogs.map(blog => (
          <li key={blog.id} onClick={() => handleBlogClick(blog.id)}>
            <div className='guide-title'>{blog.title}</div>
          </li>
        ))}
      </ul>
    )}
    <div className='guide-content'>
      {selectedBlog && selectedBlog.length > 0  && (
        <div>
          <h2>{selectedBlog[0].title}</h2>
          <p>{selectedBlog[0].content}</p>
          <p>Date Posted: {formatDate(selectedBlog[0].date_posted)}</p>
          <p>Author: {selectedBlog[0].author}</p>
        </div>
      )}
    </div>
  </div>
  )
}
