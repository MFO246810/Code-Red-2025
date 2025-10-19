import React from 'react';
import './Account.css';

const Account = () => {
  return (
    <div className='account-page'>
      <h2 className='page-title'>My Account</h2>
      <div className='account-content'>
        <div className='pfp-section'>
          <img src='https://i.pravatar.cc/150' alt='Profile' className='account-pfp' />
          <button className='change-pfp-btn'>Change Picture</button>
        </div>
        <div className='details-section'>
          <div className='detail-item'>
            <label>Username</label>
            <input type='text' defaultValue='StarGazer22' />
            <button>Change</button>
          </div>
          <div className='detail-item'>
            <label>Email</label>
            <input type='email' defaultValue='stargazer@example.com' />
            <button>Change</button>
          </div>
          <div className='detail-item'>
            <label>Password</label>
            <input type='password' defaultValue='**********' />
            <button>Change</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Account;