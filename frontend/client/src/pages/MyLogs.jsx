import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './MyLogs.css';

const MyLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user || !user.User_ID) {
          setError('User not logged in');
          setLoading(false);
          return;
        }

        const response = await fetch(`http://127.0.0.1:5000/logs/${user.User_ID}`);
        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || 'Failed to fetch logs');
        }

        const data = await response.json();
        setLogs(data);
      } catch (err) {
        console.error('Error fetching logs:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
  }, []);

  if (loading) {
    return <div className="mylogs-page loading">Loading logs...</div>;
  }

  if (error) {
    return <div className="mylogs-page error">{error}</div>;
  }

  if (logs.length === 0) {
    return <div className="mylogs-page no-logs">No logs found.</div>;
  }

  return (
    <div className="mylogs-page">
      <h2 className="page-title">My Logs</h2>
      <div className="logs-list">
        {logs.map((log) => (
          <Link to={`/log/${log.Log_ID}`} key={log.Log_ID} className="log-item">
            {log.User_Photo ? (
              <img 
                src={`http://127.0.0.1:5000/uploads/${log.User_Photo}`} 
                alt={log.Description || 'User Photo'} 
                className="log-thumbnail" 
              />
            ) : (
              <div className="log-thumbnail placeholder">No Image</div>
            )}
            <div className="log-info">
              <h3>{log.Description || 'Untitled Log'}</h3>
              <p><strong>Tags:</strong> {log.Tags}</p>
              <p><strong>Date:</strong> {new Date(log.Created_at).toLocaleString()}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default MyLogs;
