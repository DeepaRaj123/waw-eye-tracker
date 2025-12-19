import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';

interface DashboardData {
  totalBlinks: number;
  avgBlinksPerHour: number;
  data: { time: string; blinks: number }[];
}

const App: React.FC = () => {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axios.get('http://localhost:3000/dashboard/user123', {
          headers: { 'x-api-key': 'demo-secret' },
        });
        setDashboard(response.data);
      } catch (error) {
        // Fallback mock data if backend not running
        setDashboard({
          totalBlinks: 127,
          avgBlinksPerHour: 23,
          data: [
            { time: '10:00', blinks: 12 },
            { time: '11:00', blinks: 15 },
            { time: '12:00', blinks: 18 },
            { time: '13:00', blinks: 20 },
            { time: '14:00', blinks: 16 }
          ]
        });
      }
      setLoading(false);
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div style={styles.loading}>
        Loading Dashboard...
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Wellness at Work Dashboard</h1>
      </div>
      
      <div style={styles.statsGrid}>
        <div style={styles.statCard}>
          <div style={styles.statNumber}>{dashboard?.totalBlinks}</div>
          <div style={styles.statLabel}>Total Blinks</div>
        </div>
        <div style={styles.statCard}>
          <div style={styles.statNumberGreen}>{dashboard?.avgBlinksPerHour}</div>
          <div style={styles.statLabel}>Avg/Hour</div>
        </div>
      </div>

      <div style={styles.chartCard}>
        <h2 style={styles.chartTitle}>📈 Blink Trends</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={dashboard?.data || []}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="time" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip />
            <Line type="monotone" dataKey="blinks" stroke="#4a90e2" strokeWidth={4} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

const styles: any = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%)',
    color: 'white',
    padding: '2rem',
    fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif',
  },
  header: { textAlign: 'center', marginBottom: '3rem' },
  title: {
    fontSize: '3rem',
    fontWeight: 'bold',
    background: 'linear-gradient(45deg, #4a90e2, #7b68ee)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    margin: 0,
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '2rem',
    marginBottom: '3rem',
  },
  statCard: {
    background: 'rgba(255,255,255,0.05)',
    backdropFilter: 'blur(10px)',
    padding: '2rem',
    borderRadius: '20px',
    border: '1px solid rgba(255,255,255,0.1)',
    textAlign: 'center',
  },
  statNumber: {
    fontSize: '3rem',
    fontWeight: 'bold',
    color: '#4a90e2',
    marginBottom: '0.5rem',
  },
  statNumberGreen: {
    fontSize: '3rem',
    fontWeight: 'bold',
    color: '#10b981',
    marginBottom: '0.5rem',
  },
  statLabel: { fontSize: '1.2rem', color: '#9CA3AF' },
  chartCard: {
    background: 'rgba(255,255,255,0.05)',
    backdropFilter: 'blur(10px)',
    padding: '2rem',
    borderRadius: '20px',
    border: '1px solid rgba(255,255,255,0.1)',
  },
  chartTitle: { marginBottom: '1.5rem', fontSize: '1.5rem' },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    background: '#1e1e1e',
    color: 'white',
    fontSize: '2rem',
  },
};

export default App;
