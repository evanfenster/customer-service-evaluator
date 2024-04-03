import os
import json
import sys
import google.generativeai as genai

def configure_genai():
    """Configure the Generative AI with the API key from the .env file."""
    api_key = os.getenv('API_KEY')
    if api_key is not None:
        genai.configure(api_key=api_key)
        return True
    else:
        print("API_KEY not found in the environment variables.")
        return False

def get_sentiment(text, model):
    """Return the sentiment of the given text as 'positive', 'negative', or 'neutral'."""
    prompt = "Classify the sentiment of the following text as 'positive', 'negative', or 'neutral':\n\n" + text
    response = model.generate_content(prompt)
    result = response.text.strip().lower()
    return result

def append_sentiment_to_messages(messages, model):
    """Append sentiment values to each message in the messages list."""
    for message in messages:
        sentiment = get_sentiment(message['text'], model)
        message['sentiment'] = sentiment

def process_chat_file(input_filepath, output_filepath, model):
    """Process a chat JSON file to append sentiment values and save it."""
    try:
        with open(input_filepath, 'r') as file:
            chat = json.load(file)

        append_sentiment_to_messages(chat['messages'], model)

        with open(output_filepath, 'w') as file:
            json.dump(chat, file, indent=4)
        print(f"Processed file saved as {output_filepath}")
    except FileNotFoundError:
        print(f"File not found: {input_filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) < 2:
        print("Please provide the name of the chat file as an argument.")
        return
    chat_file_name = sys.argv[1]
    if configure_genai():
        model = genai.GenerativeModel('gemini-pro')
        input_filepath = f'example_chats/{chat_file_name}.json'  # Modify this line
        output_filepath = f'example_chats/{chat_file_name}_with_sentiment.json'  # Modify this line
        process_chat_file(input_filepath, output_filepath, model)

if __name__ == "__main__":
    main()
