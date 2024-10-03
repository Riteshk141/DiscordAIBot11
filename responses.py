import numpy as np
import pandas as pd
import datetime
import random
import pytz
import nltk
import re
import time
from nltk.corpus import movie_reviews, names
from nltk.data import find
from datasets import load_dataset
from nltk.corpus import nps_chat
from collections import Counter
from nltk.tokenize import word_tokenize
from difflib import get_close_matches
import random
import google.generativeai as genai
import google.api_core.exceptions
from simpleeval import simple_eval



api_key = 'AIzaSyAFD7omxzduKHJRWJwks6NJCRDxJDNuR28'
model_name = 'gemini-1.5-flash'


def chat_with_model(api_key, model_name, message, retries=3, backoff=2):
    """
    Initialize a chat session with the Generative AI model and get a response for a single message.
    Includes retry logic for handling internal server errors.

    Args:
        api_key (str): API key for authentication.
        model_name (str): The name of the Generative AI model to use.
        message (str): The message to send to the chat.
        retries (int): Number of times to retry in case of an error.
        backoff (int): Exponential backoff factor.

    Returns:
        str: The response from the model or an error message.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=[])

    attempt = 0
    while attempt < retries:
        try:
            response = chat.send_message(message)
            return response.text
        except google.api_core.exceptions.InternalServerError as e:
            attempt += 1
            wait_time = backoff ** attempt
            print(f"Attempt {attempt} failed with error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return "Failed to get a response after several attempts."



# Load a list of jokes
jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "What do you call fake spaghetti? An impasta!",
    "Why don’t programmers like nature? It has too many bugs.",
    "Why do cows wear bells? Because their horns don’t work.",
]

# Define a dictionary of time zones for different countries or regions
TIME_ZONES = {
    "us": "America/New_York",
    "uk": "Europe/London",
    "india": "Asia/Kolkata",
    "australia": "Australia/Sydney",
    "japan": "Asia/Tokyo",
    # Add more time zones as needed
}

def get_current_time(location: str = None) -> str:
    if location:
        # Use the provided location to find the correct time zone
        tz_name = TIME_ZONES.get(location.lower())
        if tz_name:
            tz = pytz.timezone(tz_name)
        else:
            # Default to UTC if the location is not found
            tz = pytz.utc
    else:
        # Default to UTC if no location is provided
        tz = pytz.utc

    current_time = datetime.datetime.now(tz)
    return f"The current time in {location or 'UTC'} is {current_time.strftime('%H:%M:%S')}."


def get_joke() -> str:
    return random.choice(jokes)



def get_response(user_input: str) -> str:

    user_input_lower = user_input.lower()

    if ("what's your name" in user_input_lower or "what is your name" in user_input_lower or "tell us about yourself" in
          user_input_lower or "tell me about yourself" in user_input_lower):
        return "I am your friendly chatbot!"

    elif "how are you" in user_input_lower or "how are you doing" in user_input_lower or "how you doing" in user_input_lower or "you good" in user_input_lower:
        return "I'm just a program, but I'm doing great! :)"

    elif "sorry" in user_input_lower or "forgive me" in user_input_lower or "forgive" in user_input_lower or "apologies" in user_input_lower or "apology" in user_input_lower:
        return "it's fine, dont worry :) !"

    elif "help" in user_input_lower or "assit" in user_input_lower or "guide" in user_input_lower:
        return "I'm here to assist you. How can I help?"

    elif "sad" in user_input_lower or "feeling bad" in user_input_lower or "terrible" in user_input_lower or "depressed" in user_input_lower:
        return "im sorry to hear that"

    elif "amazing" in user_input_lower or "nice" in user_input_lower or "good" in user_input_lower or "awesome" in user_input_lower or "amazing" in user_input_lower or "perfect" in user_input_lower:
        return "good to hear that, is there anything else you need help with ? "

    elif "hey" in user_input_lower or "hi" in user_input_lower or "hello" in user_input_lower or "greetings" in user_input_lower:
        return "hello there ! how can i help you ? "

    elif "thank you" in user_input_lower or "thanks" in user_input_lower or "appreciate" in user_input_lower:
        return "You're welcome! If you need more help, just ask."

    elif "bye" in user_input_lower or "goodbye" in user_input_lower or "see ya" in user_input_lower or "see you" in user_input_lower:
        return "Goodbye! Have a great day!"

    elif ("what's the time" in user_input_lower or "what is the time rn" in user_input_lower or
          "what is the time right now" in user_input_lower or "time rn" in user_input_lower):
        # Extract location if provided
        parts = user_input_lower.split()
        location = None
        for part in parts:
            if part in TIME_ZONES:
                location = part
                break
        return get_current_time(location)

    elif "tell me a joke" in user_input_lower or "give me a joke" in user_input_lower or "tell us a joke" in user_input_lower or "joke" in user_input_lower:
        print("here is some jokes")
        return get_joke()

    else:
        response = chat_with_model(api_key, model_name, user_input_lower)    # give response using gemini AI
        return response



# Example usage
if __name__ == "__main__":
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye!")
            break
        response = get_response(user_message)
        print(f"Bot: {response}")
