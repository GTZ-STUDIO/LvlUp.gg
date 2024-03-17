import React, { useState, useContext, useEffect, useCallback } from "react";
import { Link, useHistory } from "react-router-dom";
import "./Navbar.css";
import { Button } from "./Button";
import { AuthContext } from "../Contexts/AuthContext";
import axios from "axios";
axios.defaults.withCredentials = true;

function Navbar() {
  const [click, setClick] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const { isSignedIn, setIsSignedIn } = useContext(AuthContext);
  const { userPk } = useContext(AuthContext);
  const [user, setUser] = useState("");

  const handleClick = () => setClick(!click);
  const closeMobileMenu = () => setClick(false);

  const history = useHistory();

  const handleDropDown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const closeDropdown = () => {
    setIsDropdownOpen(false);
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

  const handleUsername = useCallback(() => {
    axios
      .get(`http://localhost:8000/account/${userPk}/`, {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        withCredentials: true,
      })
      .then((response) => {
        if (response.status === 200) {
          console.log("got Username successfully");
          setUser(response.data.username);
        } else {
          console.log("Username change unsuccessful");
        }
      })
      .catch((error) => {
        console.error("Error updating username:", error);
        // Optionally, you can handle the error or show an error message
      });
  }, [userPk]);

  useEffect(() => {
    if (isSignedIn) {
      handleUsername();
    }
  }, [isSignedIn, handleUsername]);

  const handleSignOut = () => {
    axios
      .get("http://localhost:8000/account/signout/", { withCredentials: true })
      .then((response) => {
        if (response.status === 200) {
          console.log("Successful logout:", response.data);
          alert(JSON.stringify(response.data));
          setIsSignedIn(false);
          localStorage.removeItem("isSignedIn");
          closeDropdown();
          history.push("/");
        } else {
          // Handle error
          console.error(response.data.message);
        }
      })
      .catch((error) => {
        // Handle error
        console.error(error);
      });
  };
  return (
    <>
      <nav className="navbar">
        <div data-testid="Navbar-1" className="navbar-container">
          <Link to="/" className="navbar-logo">
            LVLUP <i className="fa-solid fa-arrow-up"></i>
          </Link>
          <div className="menu-icon" onClick={handleClick}>
            <i className={click ? "fas fa-times" : "fas fa-bars"} />
          </div>
          <ul className={click ? "nav-menu active" : "nav-menu"}>
            <li className="nav-item">
              <Link
                to="/guides"
                className="nav-links"
                onClick={closeMobileMenu}
              >
                GUIDES
              </Link>
            </li>
            <li className="nav-item">
              <Link to="about" className="nav-links" onClick={closeMobileMenu}>
                ABOUT
              </Link>
            </li>
            <li className="nav-item">
              <Link
                to="signin"
                className="nav-links-mobile"
                onClick={closeMobileMenu}
              >
                Sign In
              </Link>
            </li>
          </ul>
          {isSignedIn ? (
            <div className="username">{user}</div>
          ) : (
            <Button buttonStyle="btn--outline">SIGN IN</Button>
          )}
          <div className="dropdown">
            <button className="btn--outline" onClick={handleDropDown}>
              <div className="profile-icon">
                <img src="/images/defaultUser.png" alt="Profile" />
              </div>
            </button>
            {isDropdownOpen && (
              <div className="dropdown-content">
                <Link to="/settings">
                  <button
                    onClick={() => {
                      handleDropDown();
                    }}
                  >
                    Settings
                  </button>
                </Link>
                <button
                  onClick={() => {
                    handleSignOut();
                  }}
                >
                  Sign Out
                </button>
                <Link to="/myguides">
                  <button
                    onClick={() => {
                      handleDropDown();
                    }}
                  >
                    My Guides
                  </button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </nav>
    </>
  );
}

export default Navbar;
