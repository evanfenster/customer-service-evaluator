import React from 'react';
import { Spinner } from 'react-bootstrap';
import './LoadingScreen.css';

const LoadingScreen = () => {
    return (
        <div className="loading-screen">
            <div>
                <Spinner animation="border" role="status" variant="primary" />
            </div>
            <div>
                <span className="sr-only">Analyzing chat log...</span>
            </div>
        </div>
    );
};

export default LoadingScreen;