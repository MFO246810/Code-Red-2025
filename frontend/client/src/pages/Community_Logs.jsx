import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './CommunityLogs.css';

const CommunityLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/logs');
        if (!response.ok) throw new Error('Failed to fetch logs');
        const data = await response.json();
        setLogs(data);
      } catch (err) {
        console.error(err);
        setError('Could not load community logs.');
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
  }, []);

  if (loading) return <div className="communitylogs-page loading">Loading...</div>;
  if (error) return <div className="communitylogs-page error">{error}</div>;

  return (
    <div className="communitylogs-page">
      <h2 className="page-title">Community Logs</h2>
      <div className="logs-grid">
        {logs.map((log) => (
          <Link to={`/log/${log.Log_ID}`} key={log.Log_ID} className="log-card">
            <div className="log-images">
              {log.User_Photo && (
                <img src={`http://127.0.0.1:5000/uploads/${log.User_Photo}`} alt="User Log" />
              )}
              {log.Output_Photo && (
                <img src={`http://127.0.0.1:5000/uploads/${log.Output_Photo}`} alt="Output Log" />
              )}
            </div>
            <div className="log-info">
              <h3>{log.Description || 'Untitled Log'}</h3>
              <p><strong>Tags:</strong> {log.Tags}</p>
              <p><strong>Date:</strong> {new Date(log.Created_at).toLocaleDateString()}</p>
              {log.Location && <p><strong>Location:</strong> {log.Location}</p>}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default CommunityLogs;
