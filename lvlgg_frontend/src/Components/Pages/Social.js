import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios'; // Import Axios
import '../../App.css';
import FriendsList from '../FriendsList';

function Social() {
    const backendUrl = process.env.REACT_APP_BACKEND_URL;

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
            const response = await axios.post(`${backendUrl}/account/follow/`, {
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

    const fetchFriends = useCallback(async () => {
        try {
            const response = await axios.get(`${backendUrl}/account/friends/`);
            setFriends(response.data);
        } catch (error) {
            console.error('Error:', error);
        }
    }, [backendUrl]);

    useEffect(() => {
        fetchFriends();
    }, [fetchFriends]);

    return (
        <div className='social'>
            <div className='form-container'>
                <form onSubmit={handleFormSubmit}>
                    <input
                        type='text'
                        placeholder='Search for a user to follow'
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
