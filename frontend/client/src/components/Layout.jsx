import React from 'react';
import Header from './Header';
import NavBar from './NavBar';
import './Layout.css';

const Layout = ({ children, onLogout }) => {
  return (
    <>
      <Header onLogout={onLogout} />
      <NavBar />
      <main className="content-wrap page-container">{children}</main>
    </>
  );
};

export default Layout;