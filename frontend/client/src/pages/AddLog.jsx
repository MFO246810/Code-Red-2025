import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUpload } from 'react-icons/fa';
import './AddLog.css';

const AddLog = () => {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [caption, setCaption] = useState('');
  const [location, setLocation] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Get logged-in user (from localStorage after login/signup)
  const user = JSON.parse(localStorage.getItem('user'));

  const handleUpload = async (e) => {
    e.preventDefault();
    setError('');

    if (!file) {
      setError('Please select an image file.');
      return;
    }

    if (!user || !user.User_ID) {
      setError('User not logged in.');
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('User_ID', user.User_ID);
      formData.append('Title', title);
      formData.append('Caption', caption);
      formData.append('Location', location);

      const response = await fetch('http://localhost:5000/Handle_Logging', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Upload failed');
      }

      alert('File uploaded successfully!');
      navigate(`/log/${data.Photo_ID}`); // redirect to new log page
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='addlog-page'>
      <h2 className='page-title'>Add New Log</h2>

      {loading ? (
        <div className='loading-spinner'>
          <div className='spinner'></div>
          <p>Analyzing stellar data...</p>
        </div>
      ) : (
        <form className='upload-form' onSubmit={handleUpload}>
          <div className='input-group'>
            <label htmlFor='title'>Title</label>
            <input
              type='text'
              id='title'
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>

          <div className='input-group'>
            <label htmlFor='caption'>Caption</label>
            <input
              type='text'
              id='caption'
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
            />
          </div>

          <div className='input-group'>
            <label htmlFor='location'>Location</label>
            <input
              type='text'
              id='location'
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>

          <div className='upload-area'>
            <FaUpload size={50} color='var(--secondary-text)' />
            <p>{file ? file.name : 'Drag & drop an image or click to select'}</p>
            <input
              type='file'
              accept='image/*'
              onChange={(e) => setFile(e.target.files[0])}
              required
            />
          </div>

          {error && <p className='error-text'>{error}</p>}

          <button type='submit' className='upload-button' disabled={loading}>
            Upload & Analyze
          </button>
        </form>
      )}
    </div>
  );
};

export default AddLog;
