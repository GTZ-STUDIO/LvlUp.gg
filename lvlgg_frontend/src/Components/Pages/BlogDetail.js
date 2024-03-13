import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import '../../App.css';

const BlogDetail = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  const gameImageMap = {
    "EldenRing": "url(/images/eldenRing.png)",
    "LeagueOfLegends": "url(/images/league.png)",
    "Dota2": "url(/images/dota.jpg)",
    "CSGO": "url(/images/csgo.jpg)",
    "BaldursGate3": "url(/images/baldursGate.jpeg)",
  };
  
  useEffect(() => {
    axios.get(`http://localhost:8000/blog/get_blog/?id=${id}`)
      .then(response => {
        setBlog(response.data.blogs[0]); 
      })
      .catch(error => {
        console.error('Error fetching blog:', error);
      });
  }, [id]); // Re-run the effect if the ID changes



  if (!blog) {
    return <div>Loading...</div>;
  }

  return (
    <div className="page-container" style={{ backgroundImage: gameImageMap[blog.game] }}>
      <div className="blog-detail-container">
        <h1 className="blog-title">{blog.title}</h1>
        <p className="blog-content">{blog.content}</p>
        <p className="blog-metadata">Date Posted: {blog.date_posted}</p>
        <p className="blog-metadata">Author: {blog.author}</p>
      </div>
    </div>
  );
};

export default BlogDetail;

