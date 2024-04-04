import os
import json
import google.generativeai as genai
import numpy as np
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

config = None
safety_config = None
model = None

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

def configure_genai():
    """Configure the Generative AI with the API key from the environment variables."""
    # Setup our general settings
    global config, safety_config, model
    config = {"max_output_tokens": 2048, "temperature": 0, "top_p": 1, "top_k": 32}
    safety_config = [{"category": category, "threshold": "BLOCK_NONE"} for category in ["HARM_CATEGORY_DANGEROUS", "HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
    model = genai.GenerativeModel('gemini-pro')

    # Load the API key from the environment variables
    api_key = os.getenv('API_KEY')
    if api_key is not None:
        genai.configure(api_key=api_key)
        return True
    else:
        print("API_KEY not found in the environment variables.")
        return False

def get_sentiment(text):
    """Return the sentiment of the given text as 'positive', 'negative', or 'neutral'."""
    global config, safety_config, model
    prompt = "Classify the sentiment of the following text as 'positive', 'negative', or 'neutral':\n\n" + text
    response = model.generate_content(prompt, generation_config=config, safety_settings=safety_config)
    result = response.text.strip().lower()
    return result

def append_sentiment_to_messages(messages):
    """Append sentiment values to each message in the messages list."""
    global model
    for message in messages:
        if 'sentiment' not in message:    
            sentiment = get_sentiment(message['text'])
            message['sentiment'] = sentiment

def calculate_agent_score(chat):
    """Calculate the agent's performance score."""
    # Calculate the response time score
    ideal_response_time = 60  # 1 minute in seconds
    response_times = []
    for i in range(1, len(chat['messages'])):
        if chat['messages'][i]['sender'] == 'agent' and chat['messages'][i - 1]['sender'] == 'customer':
            response_time = datetime.datetime.fromisoformat(chat['messages'][i]['timestamp'].replace("Z", "+00:00")) - datetime.datetime.fromisoformat(chat['messages'][i - 1]['timestamp'].replace("Z", "+00:00"))
            response_times.append(response_time.total_seconds())
    response_time_score = np.mean([1 if response_time <= ideal_response_time else -1 for response_time in response_times])

    # Calculate the sentiment score of the customer, which should weight later responses heavier
    customer_sentiments = [message['sentiment'] for message in chat['messages'] if message['sender'] == 'customer']
    num_cust_messages = len(customer_sentiments)
    customer_sentiment_score = 0
    for i in range(1, num_cust_messages):
        sentiment = customer_sentiments[i]
        weight = i / num_cust_messages
        customer_sentiment_score += (1 if sentiment == 'positive' else -.5 if sentiment == 'negative' else 0) * weight
    customer_sentiment_score /= (0.5* num_cust_messages)

    # Calculate the sentiment score of the agent
    agent_sentiments = [message['sentiment'] for message in chat['messages'] if message['sender'] == 'agent']
    agent_sentiment_score = np.mean([1 if sentiment == 'positive' else -1 if sentiment == 'negative' else .5 for sentiment in agent_sentiments])

    # Calculate the overall score
    overall_score = (response_time_score * 2.5) + (customer_sentiment_score * 5) + (agent_sentiment_score * 2.5)

    # Check if there is a 'rating' score in the 'session_metadata' field
    if 'session_metadata' in chat and 'rating' in chat['session_metadata']:
        rating = chat['session_metadata']['rating']
        overall_score = (overall_score * 0.8) + (rating * 2 * 0.2)

    # Return all scores
    return (response_time_score, customer_sentiment_score, agent_sentiment_score, overall_score)

@app.route('/analyze', methods=['POST'])
def analyze_chat():
    """Analyze a chat log and return the analysis results."""
    file = request.files['file']
    chat_data = json.load(file)
    append_sentiment_to_messages(chat_data['messages'])
    response_time_score, customer_sentiment_score, agent_sentiment_score, overall_score = calculate_agent_score(chat_data)

    analysis_results = {
        'chat_data': chat_data,
        'response_time_score': response_time_score,
        'customer_sentiment_score': customer_sentiment_score,
        'agent_sentiment_score': agent_sentiment_score,
        'overall_score': overall_score
    }

    return jsonify(analysis_results)

if __name__ == '__main__':
    configure_genai()
    app.run(debug=True)