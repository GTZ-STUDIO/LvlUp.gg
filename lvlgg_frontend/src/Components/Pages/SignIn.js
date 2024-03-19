import React, { useContext, useState } from "react";
import { Link, useHistory } from "react-router-dom";
import axios from "axios";
import { AuthContext } from "../../Contexts/AuthContext";

const SignIn = () => {
  const { setIsSignedIn } = useContext(AuthContext);
  const { setUserPk } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory();

  const handleSignIn = () => {
    // Handle sign-in logic here
    console.log("Signing in...");
    axios
      .post("http://localhost:8000/account/signin/", {
        username,
        password,
      })
      .then((response) => {
        if (response.status === 200) {
          console.log("Successful login:", response.data);
          setIsSignedIn(true);
          setUserPk(parseInt(response.data.id));
          history.push("/");
        } else {
          console.error("Unexpected response status:", response.status);
        }
      })
      .catch((error) => {
        if (
          error.response &&
          (error.response.status === 401 || error.response.status === 400)
        ) {
          console.error("error:", error.response.data);
          alert(JSON.stringify(error.response.data));
        }
      });
  };

  return (
    <div className="signin">
      <div className="signin-form">
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          onChange={(e) => setUsername(e.target.value)}
          className="signin-input"
        />
      </div>
      <div className="signin-form">
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          onChange={(e) => setPassword(e.target.value)}
          className="signin-input"
        />
      </div>
      <button onClick={handleSignIn} className="signin-button">
        Sign In
      </button>
      <p className="signup-font">Don't have an account?</p>
      <Link to="/signup" className="btn-mobile">
        <button className="signup-button">Sign Up</button>
      </Link>
    </div>
  );
};

export default SignIn;
