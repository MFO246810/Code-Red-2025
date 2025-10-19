import React from 'react';
import { NavLink } from 'react-router-dom';
import './NavBar.css';

const NavBar = () => {
  return (
    <nav className='secondary-nav'>
        <NavLink to="/add-log" className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>Add Log</NavLink>
        <NavLink to="/my-logs" className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>My Logs</NavLink>
        <NavLink to="/community-logs" className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>Community Logs</NavLink>
    </nav>
  )
}

export default NavBar