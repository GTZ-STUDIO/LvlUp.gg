import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../../Contexts/AuthContext';

export default function CreateGuide() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const { userPk } = useContext(AuthContext);

  const getCookie = (name) => {
    const cookieValue = document.cookie
      .split('; ')
      .find((row) => row.startsWith(`${name}=`));
    if (cookieValue) {
      return cookieValue.split('=')[1];
    }
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const csrfToken = getCookie('csrftoken');
      const response = await axios.post('http://localhost:8000/blog/create_blog/', {
        title,
        content,
        author: userPk, // Use the current user's ID as the author
      }, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
      });

      console.log(response.data);
      // Optionally, you can redirect the user to another page or show a success message
    } catch (error) {
      console.error(error);
      // Handle error, e.g., show an error message to the user
    }
  };

  return (
    <form className='createguide' onSubmit={handleSubmit}>
      <input
        type="text"
        id="title"
        name="title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder={'Title'}
        required
      />
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        name="content"
        id="content"
        cols="30"
        rows="10"
        placeholder={'Enter post'}
        required
      ></textarea>
      <button type="submit">Post Guide</button>
    </form>
  );
}
