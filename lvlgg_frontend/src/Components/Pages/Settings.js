import React, {useContext} from 'react';
import '../../App.css';
import { AuthContext } from '../../Contexts/AuthContext'
import { useHistory } from "react-router-dom";
import axios from 'axios';

const Settings = () => {
  const { userPk } = useContext(AuthContext);
  const {setIsSignedIn} = useContext(AuthContext);
  const history = useHistory();

  const getCookie = (name) => {
    const cookieValue = document.cookie
      .split('; ')
      .find((row) => row.startsWith(`${name}=`));
    if (cookieValue) {
      return cookieValue.split('=')[1];
    }
    return null;
  };
  
  const handleDeleteAccount = () => {
    console.log("CSRF Token:", getCookie('csrftoken'));
    axios.delete(`http://localhost:8000/account/delete/${userPk}/`, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'), // Replace 'csrftoken' with your CSRF token cookie name
      },
      withCredentials: true, // Send cookies with the request
    })
    .then(response => {
      if (response.status === 200) {
        console.log("Account deleted successfully");
        setIsSignedIn(false);
        history.push('/')
      } else {
        // Handle error response
        console.error("Failed to delete account:", response.data);
      }
    })
    .catch(error => {
      // Handle network error
      console.error("Network error:", error);
    });
  };

  const handleDeleteConfirmation = () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      handleDeleteAccount();
    }
  };
  
  return (
    <div className="settings">
      <div className='rectangle'></div>

        <h1>Account Settings</h1>
        <div className="input-wrapper">
          <input type="text" placeholder="Enter your new username" />
          <button className="settings-btn">Update Username</button>
        </div>
        <div className="input-wrapper">
          <input type="text" placeholder="Enter your new password" />
          <button className="settings-btn">Update Password</button>
        </div>
        <div className="input-wrapper">
          <input type="text" placeholder="Enter your new email" />
          <button className="settings-btn">Update Email</button>
        </div>
        <button className="settings-btn-delete" onClick={handleDeleteConfirmation}>
          Delete Account
        </button>
      
      
    </div>
  );
};

export default Settings;