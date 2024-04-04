// FileUpload.js
import React from 'react';
import { Card, ListGroup, Row, Col, Form, Button } from 'react-bootstrap';

const FileUpload = ({ onFileUpload }) => {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    onFileUpload(file);
  };

  return (
    <Form>
      <Form.Group>
        <Form.Label>Upload Chat Log</Form.Label>
        <Form.Control type="file" onChange={handleFileChange} />
      </Form.Group>
    </Form>
  );
};

export default FileUpload;