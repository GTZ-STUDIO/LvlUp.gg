import React, {useContext, useState} from 'react';
import '../../App.css';
import { AuthContext } from '../../Contexts/AuthContext'
import { useHistory } from "react-router-dom";
import axios from 'axios';

const Settings = () => {
  const { userPk } = useContext(AuthContext);
  const {setIsSignedIn} = useContext(AuthContext);
  const history = useHistory();

  const [newUsername, setNewUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newEmail, setNewEmail] = useState('');

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

  const handleUpdateUsername = () => {
    console.log("CSRF Token:", getCookie('csrftoken'));
    axios.put(`http://localhost:8000/account/update/${userPk}/`, 
      { username: newUsername },
      {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        withCredentials: true
      })
        .then(response => {
          if(response.status === 200){
            console.log('Username updated successfully');
            alert("Username successfully changed")
          } else {
            console.log('Username change unsuccessful')
          }
        })
        .catch(error => {
            console.error('Error updating username:', error);
            // Optionally, you can handle the error or show an error message
        });
  };

  const handleUpdatePassword = () => {
    console.log("CSRF Token:", getCookie('csrftoken'));
    axios.put(`http://localhost:8000/account/update/${userPk}/`, 
      { password: newPassword },
      {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        withCredentials: true
      })
        .then(response => {
          if(response.status === 200){
            console.log('Password updated successfully');
            alert("Password successfully changed")
          } else {
            console.log('Pass change unsuccessful')
          }
        })
        .catch(error => {
            console.error('Error updating password:', error);
            // Optionally, you can handle the error or show an error message
        });
};

  const handleUpdateEmail = () => {
    console.log("CSRF Token:", getCookie('csrftoken'));
    axios.put(`http://localhost:8000/account/update/${userPk}/`, 
      { email: newEmail },
      {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      withCredentials: true
      })
        .then(response => {
          if(response.status === 200){
            console.log('Email updated successfully');
            alert("Password successfully changed")
          } else {
            console.log('Email change unsuccessful')
          }
        })
        .catch(error => {
            console.error('Error updating email:', error);
            // Optionally, you can handle the error or show an error message
        });
};
  
  return (
    <div className="settings">
      <div className='rectangle'></div>

        <h1>Account Settings</h1>
        <div className="input-wrapper">
          <input
              type="text"
              placeholder="Enter your new username"
              value={newUsername}
              onChange={(e) => setNewUsername(e.target.value)}
          />
          <button className="settings-btn" onClick={handleUpdateUsername}>
              Update Username
          </button>
        </div>
        <div className="input-wrapper">
          <input
            type="text"
            placeholder="Enter your new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <button className="settings-btn" onClick={handleUpdatePassword}>
            Update Password
          </button>
        </div>
        <div className="input-wrapper">
          <input
            type="text"
            placeholder="Enter your new email"
            value={newEmail}
            onChange={(e) => setNewEmail(e.target.value)}
          />
          <button className="settings-btn" onClick={handleUpdateEmail}>
            Update Email
          </button>
        </div>
        <button className="settings-btn-delete" onClick={handleDeleteConfirmation}>
          Delete Account
        </button>
      
      
    </div>
  );
};

export default Settings;