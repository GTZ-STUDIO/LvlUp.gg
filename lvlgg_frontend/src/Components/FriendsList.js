import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FriendsList.css'; // Import CSS file for styling

function FriendsList() {
    const [friends, setFriends] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

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
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default FriendsList;
