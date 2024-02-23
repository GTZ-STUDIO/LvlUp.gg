import React, {useState, useContext} from 'react';
import {Link} from 'react-router-dom';
import './Navbar.css';
import { Button } from './Button';
import { AuthContext } from '../Contexts/AuthContext';

function Navbar() {
    const [click, setClick] = useState(false)
    const [button, setButton] = useState(true)
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const { isSignedIn, setIsSignedIn } = useContext(AuthContext);

    const handleClick = () => setClick(!click)
    const closeMobileMenu = () => setClick(false)

const showButton = () => {
    if(window.innerWidth <= 960) {
        setButton(false)
    } else {
        setButton(true)
    }
};

const handleDropDown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };
  
const closeDropdown = () => {
    setIsDropdownOpen(false);
};

const handleSignOut = () => {  
    setIsSignedIn(false); 
};

window.addEventListener('resize', showButton);

    return (
    <>
        <nav className='navbar'>
            <div className='navbar-container'>
                <Link to="/" className="navbar-logo">
                    LVLUP  <i className="fa-solid fa-arrow-up"></i>
                </Link>
                <div className='menu-icon' onClick={handleClick}>
                    <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
                </div>
                <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                    <li className='nav-item'>
                        <Link to='/guides' className='nav-links' onClick={closeMobileMenu}>
                            GUIDES
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='about' className='nav-links' onClick={closeMobileMenu}>
                            ABOUT
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='signin' className='nav-links-mobile' onClick={closeMobileMenu}>
                            Sign In
                        </Link>
                    </li>
                </ul>
                {isSignedIn ? (
                    <div className="dropdown">
                        <button className="btn--outline" onClick={handleDropDown}>
                            <div className="profile-icon">
                                <img src='/images/defaultUser.png' alt="Profile" />
                            </div>
                        </button>
                        {isDropdownOpen && (
                            <div className="dropdown-content">
                                <button onClick={() => { handleSignOut(); closeDropdown(); }}>Sign Out</button>
                            </div>
                        )}
                    </div>
                ) : (
                    <Button buttonStyle='btn--outline'>SIGN IN</Button>
                )}
            </div>
        </nav>
    </>
    )
}

export default Navbar
