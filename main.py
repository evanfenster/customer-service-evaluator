import os
import json
import sys
import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np
import datetime

config = None
safety_config = None
model = None

def configure_genai():
    """Configure the Generative AI with the API key from the .env file."""
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
        sentiment = get_sentiment(message['text'])
        message['sentiment'] = sentiment

def process_chat_file(chat, output_filepath):
    """Process a chat JSON file to append sentiment values and save it."""
    append_sentiment_to_messages(chat['messages'])
    with open(output_filepath, 'w') as file:
        json.dump(chat, file, indent=4)
    print(f"Processed file saved as {output_filepath}")

def get_sentiment_chart(messages, sender):
    """Generate a sentiment chart for the given sender's messages."""
    # Map sentiment to numerical values
    sentiment_mapping = {"negative": -1, "neutral": 0, "positive": 1}

    timestamps = []
    sentiments = []
    for message in messages:
        if message["sender"] == sender:
            timestamps.append(datetime.datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00")))
            sentiments.append(sentiment_mapping[message["sentiment"]])

    # Convert timestamps to matplotlib dates
    dates = date2num(timestamps)

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot_date(dates, sentiments, linestyle='-')

    sender_name = sender.capitalize()
    plt.title(f'{sender_name} Sentiment Over Time')
    plt.xlabel('Time')
    plt.ylabel('Sentiment')
    plt.yticks([-1, 0, 1], ['Negative', 'Neutral', 'Positive'])
    plt.grid(True)

    # Improve date formatting
    plt.gcf().autofmt_xdate()

    plt.show()

def get_all_sentiment_chart(messages):
    """Generate a sentiment chart for all messages, with a separate line for each sender."""
    # Map sentiment to numerical values
    sentiment_mapping = {"negative": -1, "neutral": 0, "positive": 1}

    timestamps = {}
    sentiments = {}
    senders = set()
    for message in messages:
        sender = message["sender"]
        senders.add(sender)
        if sender not in timestamps:
            timestamps[sender] = []
            sentiments[sender] = []
        timestamps[sender].append(datetime.datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00")))
        sentiments[sender].append(sentiment_mapping[message["sentiment"]])

    # Convert timestamps to matplotlib dates
    dates = {sender: date2num(timestamps[sender]) for sender in senders}

    # Plotting
    plt.figure(figsize=(10, 5))
    for sender in senders:
        plt.plot_date(dates[sender], sentiments[sender], linestyle='-', label=sender)

    plt.title('Sentiment Over Time')
    plt.xlabel('Time')
    plt.ylabel('Sentiment')
    plt.yticks([-1, 0, 1], ['Negative', 'Neutral', 'Positive'])
    plt.grid(True)
    plt.legend()

    # Improve date formatting
    plt.gcf().autofmt_xdate()

    plt.show()

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


def main():
    if len(sys.argv) < 2:
        print("Please provide the name of the chat file as an argument.")
        return
    chat_file_name = sys.argv[1]
    if configure_genai():
        input_filepath = f'example_chats/{chat_file_name}.json'  # Modify this line
        output_filepath = f'example_chats/{chat_file_name}_with_sentiment.json'  # Modify this line
        try: 
            with open(input_filepath, 'r') as file:
                input_chat = json.load(file)
        except FileNotFoundError:
            print(f"File not found: {input_filepath}")
            return
        #process_chat_file(input_chat, output_filepath)
        try:
            with open(output_filepath, 'r') as file:
                chat = json.load(file)
        except FileNotFoundError:
            print(f"File not found: {output_filepath}")
            return
        (rt_score, cs_score, as_score, overall_score) = calculate_agent_score(chat)
        get_all_sentiment_chart(chat['messages'])
        # get_sentiment_chart(chat['messages'], "customer")
        # get_sentiment_chart(chat['messages'], "agent")

if __name__ == "__main__":
    main()
