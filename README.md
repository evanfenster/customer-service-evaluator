# Customer Service Chat Analysis Dashboard

This project is a web-based dashboard for analyzing customer service chat logs and providing insights into agent performance and sentiment analysis. The dashboard allows users to upload chat log files, processes them using natural language processing techniques, and displays the results in an interactive and visually appealing manner.

## Features

- Upload chat log files in JSON format
- Analyze chat logs for sentiment analysis and agent performance metrics
- Display chat history with sentiment color-coding
- Show overall analysis scores and sentiment scores
- Provide feedback and suggestions based on the analysis results
- Interactive sentiment scores chart
- Responsive and user-friendly UI

## Prerequisites

Before running the application, make sure you have the following prerequisites installed:

- Node.js (version 12 or above)
- npm (Node Package Manager)
- Python (version 3.6 or above)
- Flask (Python web framework)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/customer-service-chat-analysis.git
   ```

2. Navigate to the project directory:
   ```
   cd customer-service-chat-analysis
   ```

3. Install the frontend dependencies:
   ```
   cd frontend
   npm install
   ```

4. Install the backend dependencies:
   ```
   cd ../backend
   pip install -r requirements.txt
   ```

## Configuration

1. Obtain an API key for natural language processing:
   - Sign up for a Google Gemini API key. 

2. Set up the API key:
   - Create a new file named `.env` in the root directory.
   - Open the `.env` file and add the following line:
     ```
     API_KEY=your-api-key
     ```
   - Replace `your-api-key` with the actual API key you obtained.

## Running the Application

1. Start the backend server:
   ```
   cd backend
   flask run
   ```

2. In a separate terminal, start the frontend development server:
   ```
   cd frontend
   npm start
   ```

3. Open your web browser and navigate to `http://localhost:3000` to access the dashboard.

## Chat Log Format

The chat log files should be in JSON format and follow a specific structure. Here's an example of what a chat log file should look like:

```json
{
  "session_id": "987654321",
  "start_time": "2024-04-02T15:00:00Z",
  "end_time": "2024-04-02T15:45:00Z",
  "customer_id": "C54321",
  "agent_id": "A12345",
  "channel": "app",
  "messages": [
    {
      "message_id": "1",
      "timestamp": "2024-04-02T15:01:00Z",
      "sender": "customer",
      "text": "My service has been horrible lately!"
    },
    {
      "message_id": "2",
      "timestamp": "2024-04-02T15:01:30Z",
      "sender": "agent",
      "text": "I'm sorry to hear that. Could you describe the issues you're facing?"
    },
    ...
  ],
  "session_metadata": {
    "rating": 5,
    "tags": [
      "service_issue",
      "technical_support",
      "resolved"
    ]
  }
}
```

The chat log file should have the following fields:

- `session_id` (string): A unique identifier for the chat session.
- `start_time` (string): The start time of the chat session in ISO 8601 format.
- `end_time` (string): The end time of the chat session in ISO 8601 format.
- `customer_id` (string): An identifier for the customer.
- `agent_id` (string): An identifier for the customer service agent.
- `channel` (string): The communication channel of the chat session (e.g., "app", "web", "phone").
- `messages` (array): An array of message objects representing the conversation between the customer and the agent. Each message object should have the following fields:
  - `message_id` (string): A unique identifier for the message.
  - `timestamp` (string): The timestamp of the message in ISO 8601 format.
  - `sender` (string): The sender of the message, either "customer" or "agent".
  - `text` (string): The content of the message.
- `session_metadata` (object): Additional metadata about the chat session. It can include fields like:
  - `rating` (number): A rating score for the chat session.
  - `tags` (array): An array of tags or labels associated with the chat session.

Ensure that your chat log files adhere to this format for proper analysis and visualization in the dashboard.

...

## Usage

1. Prepare your chat log files in the JSON format described above.
2. Click on the "Choose File" button to select a chat log file.
3. Once the file is uploaded, the dashboard will display the analysis results.
4. Explore the chat history, sentiment scores, and feedback sections to gain insights into the customer service interactions.
5. Use the sentiment scores chart to visualize the sentiment trends over time.
6. Customize the dashboard by modifying the code and CSS files to suit your specific requirements.

## Acknowledgements

- [React](https://reactjs.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Recharts](https://recharts.org/)
- [Flask](https://flask.palletsprojects.com/)