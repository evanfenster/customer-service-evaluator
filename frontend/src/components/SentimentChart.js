import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Button } from 'react-bootstrap';

const SentimentChart = ({ data }) => {
  const [showCustomer, setShowCustomer] = useState(true);
  const [showAgent, setShowAgent] = useState(true);

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
  };

  const formatSentiment = (sentiment) => {
    if (sentiment === 1) return 'Positive';
    if (sentiment === 0) return 'Neutral';
    if (sentiment === -1) return 'Negative';
    return null;
  };

  // Directly format the main data array to include readable timestamps and sentiments.
  const formattedData = data.map((d) => ({
    ...d,
    timestamp: formatTimestamp(d.timestamp),
    sentiment: formatSentiment(d.sentiment),
  }));

  // Create a unique sorted list of all timestamps.
  const allTimestamps = [...new Set(formattedData.map((d) => d.timestamp))].sort((a, b) => new Date(a) - new Date(b));

  // Map of sentiments by timestamp, preparing entries for both customer and agent.
  const sentimentsByTimestamp = formattedData.reduce((acc, cur) => {
    const key = cur.timestamp;
    if (!acc[key]) {
      acc[key] = { customerSentiment: null, agentSentiment: null };
    }
    acc[key][`${cur.sender}Sentiment`] = cur.sentiment;
    return acc;
  }, {});

  // Fill in the chart data, ensuring each timestamp has both customer and agent data.
  const chartData = allTimestamps.map((timestamp) => ({
    timestamp,
    ...sentimentsByTimestamp[timestamp],
  }));

  const handleCustomerToggle = () => setShowCustomer((prevState) => !prevState);
  const handleAgentToggle = () => setShowAgent((prevState) => !prevState);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '10px' }}>
        <Button variant="primary" onClick={handleCustomerToggle} style={{ marginRight: '10px' }}>
          {showCustomer ? 'Hide Customer' : 'Show Customer'}
        </Button>
        <Button variant="primary" onClick={handleAgentToggle}>
          {showAgent ? 'Hide Agent' : 'Show Agent'}
        </Button>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis type="category" dataKey="sentiment" domain={['Negative', 'Neutral', 'Positive']} />
          <Tooltip />
          <Legend />
          {showCustomer && <Line type="monotone" dataKey="customerSentiment" stroke="#8884d8" activeDot={{ r: 8 }} name="Customer" connectNulls />}
          {showAgent && <Line type="monotone" dataKey="agentSentiment" stroke="#82ca9d" activeDot={{ r: 8 }} name="Agent" connectNulls />}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SentimentChart;
