import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './AuthForm.css';

const SignUp = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          UserName: username,
          Email: email,
          Password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Signup failed');
        return;
      }

      // Optionally store user info
      localStorage.setItem('user', JSON.stringify(data.user));

      alert('Signup successful!');
      navigate('/login'); // redirect to login after successful signup
    } catch (err) {
      console.error('Error signing up:', err);
      setError('An unexpected error occurred.');
    }
  };

  return (
    <div className='auth-container'>
      <div className='auth-form-wrapper'>
        <h1 className='auth-title'>SIGN-UP</h1>
        <p className='auth-subtitle'>
          or <Link to='/login'>login</Link>
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
            <label htmlFor='email'>Email</label>
            <input
              type='email'
              id='email'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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

          <button type='submit' className='auth-button'>SIGN-UP</button>
        </form>
      </div>
    </div>
  );
};

export default SignUp;
