import React, {useState,useContext,useEffect, useCallback} from "react";
import { Link, useHistory } from "react-router-dom";
import "./Navbar.css";
import { Button } from "./Button";
import { AuthContext } from "../Contexts/AuthContext";
import axios from "axios";
axios.defaults.withCredentials = true;

function Navbar() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const [click, setClick] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isFavoritesOpen, setIsFavoritesOpen] = useState(false);
  const { isSignedIn, setIsSignedIn } = useContext(AuthContext);
  const { userPk } = useContext(AuthContext);
  const [user, setUser] = useState("");
  const [favorites, setFavorites] = useState([]);

  const handleClick = () => setClick(!click);
  const closeMobileMenu = () => setClick(false);

  const history = useHistory();

  const gameImageMap = {
    EldenRing: 'images/eldenRing.png',
    Dota2: 'images/dota.jpg',
    LeagueOfLegends: 'images/league.png',
    BaldursGate3: 'images/baldursGate.png',
    CSGO: 'images/csgo.jpg',
};

  const handleDropDown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleFavorites = () => {
    setIsFavoritesOpen(!isFavoritesOpen);
    setIsDropdownOpen(false);
  };

  const closeDropdowns = () => {
    setIsDropdownOpen(false);
    setIsFavoritesOpen(false);
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

  const fetchFavorites = async () => {
    try {
      const response = await axios.get(`${backendUrl}/favourite/list/`, {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        withCredentials: true,
      });
      const userFavorites = response.data
      console.log(userFavorites);
      setFavorites(userFavorites);
      console.log(favorites[0].blog_id);
    } catch (error) {
      console.error("Error fetching favorites:", error);
    }
  };

  useEffect(() => {
    if (isSignedIn) {
      fetchFavorites();
    }
  }, [isSignedIn]);
  

  const handleUsername = useCallback(() => {
    axios
      .get(`${backendUrl}/account/${userPk}/`, {
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
      });
  }, [userPk, backendUrl]);

  useEffect(() => {
    if (isSignedIn) {
      handleUsername();
    }
  }, [isSignedIn, handleUsername]);

  const handleSignOut = () => {
    axios.get(`${backendUrl}/account/signout/`, { withCredentials: true })
      .then((response) => {
        if (response.status === 200) {
          console.log("Successful logout:", response.data);
          alert(JSON.stringify(response.data));
          setIsSignedIn(false);
          localStorage.removeItem("isSignedIn");
          closeDropdowns();
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
          {isSignedIn && (
            <div className="dropdown">
              <button className="btn--outline" onClick={handleDropDown}>
                <div className="profile-icon">
                  <img src="/images/defaultUser.png" alt="Profile" />
                </div>
              </button>
              {isDropdownOpen && (
                <div className="dropdown-content">
                  <Link to="/myguides">
                    <button onClick={closeDropdowns}>My Guides</button>
                  </Link>
                  <Link to="/settings">
                    <button onClick={closeDropdowns}>Settings</button>
                  </Link>
                  <Link to="/social">
                    <button onClick={closeDropdowns}>Social</button>
                  </Link>
                  <button onClick={handleSignOut}>Sign Out</button>
                </div>
              )}
            </div>
          )}
          {isSignedIn && (
             <div className={`favorites-dropdown ${isFavoritesOpen ? 'open' : ''}`} onMouseEnter={handleFavorites} onMouseLeave={handleFavorites}>
              <div className="profile-icon">
                <img src="/images/star.png" alt="Favourites" />
              </div>
              {isFavoritesOpen && (
                <div className="favorites-dropdown-content">
                  {favorites.map((favorite) => (
                    <Link key={favorite} to={`/blog/${favorite.blog_id}`}>
                      <div className="circle">
                        <img className="game-image" src={gameImageMap[favorite.blog_game]} alt={favorite.blog_game} />
                        <div className="tooltip">{favorite.blog_title}</div>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </nav>
    </>
  );
}
export default Navbar;
