import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FriendsList.css'; // Import CSS file for styling

function FriendsList() {
    const [friends, setFriends] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

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
        const fetchFriends = async () => {
            try {
                const response = await axios.get('http://localhost:8000/account/friends/');
                setFriends(response.data);
            } catch (error) {
                console.error('Error:', error);
            }
        };
        fetchFriends();
    }, []);

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleUnfriend = async (friendId) => {
        const csrfToken = getCookie('csrftoken');
        try {
            await axios.post('http://localhost:8000/account/unfollow/', { username: friends.find(friend => friend.id === friendId).username }, 
            {headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
              },});
            setFriends(friends.filter(friend => friend.id !== friendId));
            alert('Unfollowed Successfully')
        } catch (error) {
            console.error('Error removing friend:', error);
        }
    };

    const filteredFriends = friends.filter((friend) =>
        friend.username.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className='friends-list'>
            <h2>Friends List</h2>
            <input
                type='text'
                placeholder='Search for a friend...'
                value={searchTerm}
                onChange={handleSearchChange}
            />
            <ul>
                {filteredFriends.map((friend) => (
                    <li key={friend.id} className='friend-item'>
                        {friend.username}
                        <button onClick={() => handleUnfriend(friend.id)} className='unfriend-button'>Unfollow</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default FriendsList;
