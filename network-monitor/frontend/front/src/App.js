import React, { useState, useEffect } from 'react';

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    maxWidth: '800px',
    margin: '0 auto',
    padding: '20px',
    backgroundColor: '#f0f4f8',
    borderRadius: '10px',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
  },
  header: {
    backgroundColor: '#3498db',
    padding: '20px',
    borderRadius: '10px 10px 0 0',
    marginBottom: '20px',
  },
  title: {
    margin: '0',
    color: 'white',
    fontSize: '24px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    marginBottom: '20px',
  },
  inputGroup: {
    display: 'flex',
    gap: '10px',
  },
  input: {
    flex: '1',
    padding: '10px',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ddd',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#2ecc71',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  table: {
    width: '100%',
    borderCollapse: 'separate',
    borderSpacing: '0 10px',
  },
  th: {
    backgroundColor: '#34495e',
    color: 'white',
    padding: '15px',
    textAlign: 'left',
    borderRadius: '5px 5px 0 0',
  },
  td: {
    padding: '15px',
    backgroundColor: 'white',
    borderBottom: '1px solid #ecf0f1',
  },
  badge: {
    padding: '5px 10px',
    borderRadius: '20px',
    fontWeight: 'bold',
    display: 'inline-block',
    textAlign: 'center',
    minWidth: '80px',
  },
  badgeUp: {
    backgroundColor: '#2ecc71',
    color: 'white',
  },
  badgeDown: {
    backgroundColor: '#e74c3c',
    color: 'white',
  },
  error: {
    color: '#e74c3c',
    marginTop: '10px',
  },
};

export default function App() {
  const [ipAddresses, setIpAddresses] = useState([
    { address: '192.168.1.1', status: 'up', name: 'Router' },
    { address: '10.0.0.1', status: 'down', name: 'Server' },
  ]);
  const [newIpAddress, setNewIpAddress] = useState('');
  const [newDeviceName, setNewDeviceName] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      setIpAddresses(prevAddresses => 
        prevAddresses.map(ip => ({
          ...ip,
          status: Math.random() > 0.5 ? 'up' : 'down' // Randomly change status
        }))
      );
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const isValidIpAddress = (ip) => {
    const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return ipRegex.test(ip);
  };

  const handleAddIp = (e) => {
    e.preventDefault();
    if (!newIpAddress || !newDeviceName) {
      setError('Please enter both IP address and device name.');
      return;
    }
    if (!isValidIpAddress(newIpAddress)) {
      setError('Please enter a valid IP address.');
      return;
    }
    if (ipAddresses.some(ip => ip.address === newIpAddress)) {
      setError('This IP address already exists.');
      return;
    }
    setIpAddresses([...ipAddresses, { address: newIpAddress, status: 'up', name: newDeviceName }]);
    setNewIpAddress('');
    setNewDeviceName('');
    setError('');
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>IP Address Dashboard</h1>
      </header>
      <form onSubmit={handleAddIp} style={styles.form}>
        <div style={styles.inputGroup}>
          <input
            type="text"
            placeholder="Enter IP address"
            value={newIpAddress}
            onChange={(e) => setNewIpAddress(e.target.value)}
            style={styles.input}
          />
          <input
            type="text"
            placeholder="Enter device name"
            value={newDeviceName}
            onChange={(e) => setNewDeviceName(e.target.value)}
            style={styles.input}
          />
          <button type="submit" style={styles.button}>Add Device</button>
        </div>
      </form>
      {error && <p style={styles.error}>{error}</p>}
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>IP Address</th>
            <th style={styles.th}>Device Name</th>
            <th style={styles.th}>Status</th>
          </tr>
        </thead>
        <tbody>
          {ipAddresses.map((ip) => (
            <tr key={ip.address}>
              <td style={styles.td}>{ip.address}</td>
              <td style={styles.td}>{ip.name}</td>
              <td style={styles.td}>
                <span style={{
                  ...styles.badge,
                  ...(ip.status === 'up' ? styles.badgeUp : styles.badgeDown)
                }}>
                  {ip.status.toUpperCase()}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}