import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../../Contexts/AuthContext';
import { useHistory } from 'react-router-dom';

export default function CreateGuide() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const { userPk } = useContext(AuthContext);
  const [ game, setGame ] = useState('');
  const history  = useHistory();

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
        game,
      }, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
      });

      console.log(response.data);
      alert('Guide Created Successfully')
      history.push("/guides");
    } catch (error) {
      console.error(error);
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
      <select
        className='dropdown-select'
        id="game"
        name="game"
        value={game}
        onChange={(e) => setGame(e.target.value)}
        required
      >
        <option value="" disabled selected>Select a game</option>
        <option value="EldenRing">EldenRing</option>
        <option value="Dota2">Dota2</option>
        <option value="LeagueOfLegends">LeagueOfLegends</option>
        <option value="BaldursGate3">BaldursGate3</option>
        <option value="CSGO">CSGO</option>
      </select>
      
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
