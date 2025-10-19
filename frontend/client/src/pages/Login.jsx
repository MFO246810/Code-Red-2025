import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './AuthForm.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          UserName: username,
          Password: password,
        }),
      });
      console.log("Fetch Request Done processing")
      const data = await response.json();
      console.log("Data: ", data)
      if (!response.ok) {
        setError(data.error || 'Login failed');
        return;
      }

      // Save user info or token if needed
      localStorage.setItem('user', JSON.stringify(data.user));

      alert('Login successful!');
      navigate('/'); // Redirect user after login
    } catch (err) {
      console.error('Error logging in:', err);
      setError('An unexpected error occurred.');
    }
  };

  return (
    <div className='auth-container'>
      <div className='auth-form-wrapper'>
        <h1 className='auth-title'>LOGIN</h1>
        <p className='auth-subtitle'>
          or <Link to='/signup'>sign-up</Link>
        </p>
        <form className='auth-form' onSubmit={handleSubmit}>
          <div className='input-group'>
            <label htmlFor='username'>Username</label>
            <input
              type='text'
              id='username'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className='input-group'>
            <label htmlFor='password'>Password</label>
            <input
              type='password'
              id='password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className='error-text'>{error}</p>}

          <button type='submit' className='auth-button'>
            LOGIN
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
