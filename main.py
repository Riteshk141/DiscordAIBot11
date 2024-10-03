import os
from discord import Intents, Client, Message
from dotenv import load_dotenv
from responses import get_response, chat_with_model, api_key, model_name
from custom_user_responses import CustomUserResponses
import re
from SpamProtection import SpamProtection

# Explicitly specify the path to the .env file
dotenv_path = 'C:/Users/rites/Desktop/Project/pythonProject/.env'
load_dotenv(dotenv_path=dotenv_path)

# Retrieve the token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Handling intents
intents = Intents.default()
intents.message_content = True  # Enable message content intent

client = Client(intents=intents)


SPECIFIC_USER2 = "mason141"

# Create an instance of CustomUserResponses
custom_responder = CustomUserResponses(SPECIFIC_USER2)
spam_protection = SpamProtection(client)  # Initialize with the client object


# Message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty)')
        return

    try:
        response = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(f"Failed to generate response: {e}")
        await message.channel.send("Sorry, I couldn't process your request at the moment.")


# Handling the startup for our bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

    # Get a default channel (e.g., the first channel in the server)
    for guild in client.guilds:
        channel = guild.text_channels[0]  # This selects the first text channel in the guild
        if channel:
            await channel.send(f"Hello I'm online and ready to chat")
            break  # Stop after sending to the first channel of the first guild


# ("Terminating... going offline! see you laterrrrr ")

async def send_long_message(channel, content):
    while len(content) > 2000:
        await channel.send(content[:2000])
        content = content[2000:]
    await channel.send(content)


# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    # Check for spam
    await spam_protection.check_spam(message)

    # Check if the bot is mentioned in the message
    if client.user.mention in message.content:
        user_message = message.content.replace(client.user.mention, "").strip()  # Clean the mention from the message
        username = message.author.name
        channel = str(message.channel)

        print(f'[{channel}] {username}: "{user_message}"')

        if not user_message:
            print('(Message was empty)')
            return

        # Check if the message is from the specific user
        response = custom_responder.get_custom_response(username, user_message)
        if response:
            await send_long_message(message.channel, response)
            return

        response = custom_responder.get_custom_response2(username, user_message)
        if response:
            await send_long_message(message.channel, response)
            return

        # # Check for mathematical expressions
        # response = get_response2(user_message)
        # if response:
        #     await send_long_message(message.channel, response)
        #     return

        # Generate response using the Generative AI model
        try:
            response = chat_with_model(api_key, model_name, user_message)
            print(f"Debug: chat_with_model returned: {response}")  # Debugging statement to check the response

            if response and response.strip():  # Ensure the response is not empty or just whitespace
                await send_long_message(message.channel, response)
                return
            else:
                await message.channel.send("Sorry, I couldn't process your request at the moment.")
                return
        except Exception as e:
            print(f"Failed to generate response: {e}")
            await message.channel.send("Sorry, I couldn't process your request at the moment.")
            return


def main() -> None:
    client.run(TOKEN)


if __name__ == '__main__':
    main()
