import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FavoriteButton = ({ blogId, initialIsFavorited, onToggle }) => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const [loading, setLoading] = useState(false);
  const [isFavorited, setIsFavorited] = useState(initialIsFavorited);

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const response = await axios.get(`${backendUrl}/favourite/list/`);
        const favorites = response.data.map((favorite) => favorite.blog_id);
        setIsFavorited(favorites.includes(blogId));
      } catch (error) {
        console.error('Failed to fetch favorites:', error);
      }
    };

    fetchFavorites();
  }, [backendUrl, blogId]);

  const handleToggleFavorite = async () => {
    setLoading(true);
    setIsFavorited(!isFavorited); // Update the state immediately
  
    try {
      const csrfToken = getCookie('csrftoken');
      const action = isFavorited ? 'unsubscribe' : 'subscribe';
      const method = isFavorited ? 'DELETE' : 'POST';
  
      await axios.request({
        url: `${backendUrl}/favourite/${action}/${blogId}/`,
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
      });
      onToggle();
    } catch (error) {
      console.error('Failed to toggle favorite:', error);
   
      setIsFavorited(!isFavorited);
    } finally {
      setLoading(false);
    }
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

  return (
    <button onClick={handleToggleFavorite} disabled={loading}>
      {isFavorited ? 'Unfavorite' : 'Favorite'}
    </button>
  );
};

export default FavoriteButton;
