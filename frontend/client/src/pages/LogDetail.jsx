import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import LaikaChat from '../components/LaikaChat';
import './LogDetail.css';

const LogDetail = () => {
  const { id } = useParams(); // Get log ID from URL
  const [logData, setLogData] = useState(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchLogDetail = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/Current_logs/${id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch log');
        }
        const data = await response.json();
        setLogData(data);
      } catch (err) {
        console.error('Error fetching log:', err);
        setError('Could not load log details.');
      }
    };

    fetchLogDetail();
  }, [id]);

  if (error) {
    return <div className='logdetail-page error'>{error}</div>;
  }

  if (!logData) {
    return <div className='logdetail-page loading'>Loading...</div>;
  }
  console.log(logData.User_Photo)

  const buildImageUrl = (filePath) => filePath ? `http://127.0.0.1:5000/uploads/${filePath}` : null;

  return (
    <div className='logdetail-page'>
      <div className='log-details-container'>

        <h2 className='Detail_Title'>{logData.Title}</h2>

        <div className='log-image-container'>
          {logData.User_Photo && (
            <img 
              src={buildImageUrl(logData.User_Photo)} 
              alt={`${logData.Title} User Photo`} 
            />
          )}
          {logData.Output_Photo && (
            <img 
              src={buildImageUrl(logData.Output_Photo)} 
              alt={`${logData.Title} Output`} 
            />
          )}
        </div>

        <div className='details-grid'>
          <p><strong>Tags:</strong> {logData.Tags}</p>
          <p><strong>Date Taken:</strong> {logData.Created_at}</p>
          <p><strong>Location:</strong> {logData.Location || 'Unknown'}</p>
          <p><strong>User ID:</strong> {logData.User_ID}</p>
          <p><strong>Calibration:</strong> {logData.Calibration ? JSON.stringify(logData.Calibration, null, 2) : 'N/A'}</p>
          <p><strong>Description:</strong> {logData.Description || 'No description'}</p>
        </div>
      </div>

      <button className='laika-edge-bar' onClick={() => setIsChatOpen(true)}>
        Laika
      </button>

      {isChatOpen && <LaikaChat logData={logData} closeChat={() => setIsChatOpen(false)} />}
    </div>
  );
};

export default LogDetail;
