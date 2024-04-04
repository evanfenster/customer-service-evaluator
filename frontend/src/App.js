// App.js
import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import Footer from './components/Footer';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <main>
        <Container>
          <Row>
            <Col>
              <Dashboard />
            </Col>
          </Row>
        </Container>
      </main>
      <Footer />
    </div>
  );
}

export default App;