import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import Axios
import '../../App.css';
import FriendsList from '../FriendsList';

function Social() {
    const [username, setUsername] = useState('');
    const [friends, setFriends] = useState([]);

    const handleInputChange = (event) => {
        setUsername(event.target.value);
    };

    const getCookie = (name) => {
        const cookieValue = document.cookie
          .split("; ")
          .find((row) => row.startsWith(`${name}=`));
        if (cookieValue) {
          return cookieValue.split("=")[1];
        }
        return null;
      };

      const handleFormSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/account/follow/', {
                username
            }, {
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                withCredentials: true, 
            });
            alert('Friend successfuly added');
            setFriends([...friends, response.data]);
    
            setUsername('');
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const fetchFriends = async () => {
        try {
            const response = await axios.get('http://localhost:8000/account/friends/');
            setFriends(response.data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    useEffect(() => {
        fetchFriends();
    }, []);

    return (
        <div className='social'>
            <div className='form-container'>
                <form onSubmit={handleFormSubmit}>
                    <input
                        type='text'
                        placeholder='Enter username'
                        value={username}
                        onChange={handleInputChange}
                    />
                    <button type='submit'>Follow</button>
                </form>
            </div>
            <FriendsList friends={friends} />
        </div>
    );
}

export default Social;
