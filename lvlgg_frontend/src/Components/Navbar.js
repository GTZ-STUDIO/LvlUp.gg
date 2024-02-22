import React, {useState} from 'react';
import {Link} from 'react-router-dom';
import './Navbar.css';
import { Button } from './Button';

function Navbar() {
    const [click, setClick] = useState(false)
    const [button, setButton] = useState(true)

    const handleClick = () => setClick(!click)
    const closeMobileMenu = () => setClick(false)

const showButton = () => {
    if(window.innerWidth <= 960) {
        setButton(false)
    } else {
        setButton(true)
    }
};

window.addEventListener('resize', showButton);

    return (
    <>
        <nav className='navbar'>
            <div className='navbar-container'>
                <Link to="/" className="navbar-logo">
                    LVLUP  <i class="fa-solid fa-arrow-up"></i>
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
                {button && <Button buttonStyle='btn--outline'>SIGN IN</Button>}
            </div>
        </nav>
    </>
    )
}

export default Navbar
