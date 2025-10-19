import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className='home-container'>
        <div className='home-hero'>
            <h1 className='home-title'>AstroLog</h1>
            <p className='home-subtitle'>Turn your amateur astrophotography into real science.</p>
        </div>
        <footer className='home-footer'>
            <p>Contact Us: contact@astrolog.dev | Made with ❤️ by visionary developers</p>
        </footer>
    </div>
  )
}

export default Home;