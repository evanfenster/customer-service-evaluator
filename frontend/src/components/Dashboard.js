import React, { useState } from 'react';
import axios from 'axios';
import { Container, Row, Col, Card } from 'react-bootstrap';
import FileUpload from './FileUpload';
import SentimentChart from './SentimentChart';
import ChatView from './ChatView';
import ChatInfo from './ChatInfo';
import { placeholderFeedback } from './Feedback';
import './Dashboard.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const Dashboard = () => {
  const [analysisResults, setAnalysisResults] = useState(null);

  const handleFileUpload = async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file, file.name);

      const response = await axios.post('http://localhost:5000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setAnalysisResults(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const transformChatData = (chatData) => {
    return chatData.messages.map((message) => ({
      timestamp: message.timestamp,
      sender: message.sender,
      sentiment: message.sentiment === 'positive' ? 1 : message.sentiment === 'negative' ? -1 : 0,
    }));
  };

  return (
    <Container fluid className="dashboard d-flex flex-column vh-100">
      <Row className="flex-grow-1">
        <Col md={4} lg={3} className="sidebar">
          <h1 className="text-center mb-4">Customer Service Evaluator</h1>
          <FileUpload onFileUpload={handleFileUpload} />
          {analysisResults && (
            <>
              <ChatInfo chatData={analysisResults.chat_data} />
              <Card className="mt-4">
                <Card.Body>
                  <Card.Title>Feedback</Card.Title>
                  <ul className="feedback-list">
                    {placeholderFeedback.map((feedback, index) => (
                      <li key={index}>{feedback}</li>
                    ))}
                  </ul>
                </Card.Body>
              </Card>
            </>
          )}
        </Col>
        <Col md={8} lg={9} className="main-content">
          {analysisResults && (
            <>
              <Card className="mb-4">
                <Card.Body>
                  <Card.Title className="text-center">Analysis</Card.Title>
                  <Row>
                    <Col>
                      <div className="score-label">Overall Score</div>
                      <div className="score-value">{analysisResults.overall_score.toFixed(1)}</div>
                    </Col>
                    <Col>
                      <div className="score-label">Response Time Score</div>
                      <div className="score-value">{analysisResults.response_time_score.toFixed(1)}</div>
                    </Col>
                    <Col>
                      <div className="score-label">Customer Sentiment Score</div>
                      <div className="score-value">{analysisResults.customer_sentiment_score.toFixed(1)}</div>
                    </Col>
                    <Col>
                      <div className="score-label">Agent Sentiment Score</div>
                      <div className="score-value">{analysisResults.agent_sentiment_score.toFixed(1)}</div>
                    </Col>
                  </Row>
                </Card.Body>
              </Card>
              <Row>
                <Col>
                  <ChatView messages={analysisResults.chat_data.messages} />
                </Col>
              </Row>
              <Row>
                <Col>
                  <Card className="mt-4">
                    <Card.Body>
                      <Card.Title className="text-center">Sentiment Scores</Card.Title>
                      <SentimentChart data={transformChatData(analysisResults.chat_data)} />
                    </Card.Body>
                  </Card>
                </Col>
              </Row>
            </>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;