import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = ({ onLogout }) => {
    const [dropdownVisible, setDropdownVisible] = useState(false);

    return (
        <header className="main-header">
          <Link to="/" className="logo">
            ASTROLOG
          </Link>
          <div 
            className="user-profile"
            onMouseEnter={() => setDropdownVisible(true)}
            onMouseLeave={() => setDropdownVisible(false)}
          >
            <span>StarGazer22</span>
            <img src="https://i.pravatar.cc/40" alt="User Profile" />
            {dropdownVisible && (
                <div className="profile-dropdown">
                    <Link to="/account" className='dropdown-item'>Account</Link>
                    <button onClick={onLogout} className='dropdown-item logout-btn'>Logout</button>
                </div>
            )}
          </div>
        </header>
    );
};

export default Header;