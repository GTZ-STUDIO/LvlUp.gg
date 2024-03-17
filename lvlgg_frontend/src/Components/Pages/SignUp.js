import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";
//import { AuthContext } from '../../Contexts/AuthContext';

const SignUp = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstname, setFirstName] = useState("");
  const [lastname, setLastName] = useState("");
  const history = useHistory();

  const handleSignUp = () => {
    console.log("Sending Data");
    axios
      .post("http://localhost:8000/account/signup/", {
        username,
        email,
        password,
        firstname,
        lastname,
      })
      .then((response) => {
        if (response.status === 200) {
          console.log("Account created successfully:", response.data);
          alert("account created successfully");
          history.push("/signin");
        } else {
          console.error("Unexpected response status:", response.status);
        }

        // Redirect or perform other actions upon successful account creation
      })
      .catch((error) => {
        if (error.response && error.response.status === 400) {
          console.error("error:", error.response.data);
          alert(JSON.stringify(error.response.data));
        }
      });
  };

  return (
    <div className="signup">
      <div className="signup-form">
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="signin-input"
        />
      </div>
      <div className="signup-form">
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="signin-input"
        />
      </div>
      <div className="signup-form">
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="signin-input"
        />
      </div>
      <div className="signup-form">
        <label htmlFor="firstname">First:</label>
        <input
          type="text"
          id="firstname"
          name="firstname"
          value={firstname}
          onChange={(e) => setFirstName(e.target.value)}
          className="signin-input"
        />
      </div>
      <div className="signup-form">
        <label htmlFor="lastname">Last:</label>
        <input
          type="text"
          id="lastname"
          name="lastname"
          value={lastname}
          onChange={(e) => setLastName(e.target.value)}
          className="signin-input"
        />
      </div>
      <button onClick={handleSignUp} className="signup-button">
        Create Account
      </button>
    </div>
  );
};

export default SignUp;
