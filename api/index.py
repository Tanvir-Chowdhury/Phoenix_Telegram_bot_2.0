# Import necessary modules
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from flask import Flask
from threading import Thread
from openai import OpenAI
from io import BytesIO
from PIL import Image
import base64
import requests

# Flask app setup
app = Flask(__name__)

@app.route('/')
def main():
    return "Your Bot Is Ready"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

# Bot and OpenAI API keys
TELEGRAM_TOKEN = "8078701645:AAGI970Rw9krnbfHRr-4DTh8wdQRo1vLZM4" 
OPENAI_API_KEY = "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"  

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Please set TELEGRAM_TOKEN and OPENAI_API_KEY in the script.")

# Keep the Flask app alive
keep_alive()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()  # Create a router for handling messages

# Bot personality
BOT_PERSONALITY = (
    "You are a helpful friend. Behave like a human friend who helps in everything related to private university admission test in Bangladesh. "
    "Your name is Phoenix. Do not mention that you are an AI language model and do not say that you will assist. "
    "Your creator is Phoenix Admission Care."
    "If any math problem given, solve it without using Latex."
)

# Create a dictionary to store messages for each user
messages = {}
client = OpenAI(api_key=OPENAI_API_KEY)

async def generate_response(username: str) -> str:
    """Generate a response using OpenAI API."""
    logger.info(f"Generating response for user: {username}")
    try:
        
        # Fetch the message history for the user
        user_messages = messages[username]
        # Include the system message at the start of the conversation
        conversation_history = [{"role": "system", "content": BOT_PERSONALITY}] + user_messages
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )
        generated_response = response.choices[0].message.content.strip()
        logger.info(f"Response generated: {generated_response}")
        return generated_response
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Sorry, something went wrong while processing your request."



# Handle the /start command
@router.message(Command("phoenix"))
async def start_cmd(message: types.Message):
    try:
        username = message.from_user.username
    except AttributeError:
        await message.answer("Please set a username in Telegram settings and try again.")
        return
    messages[username] = []
    await message.answer("Hello, I'm Phoenix. How can I help you today?")

# Handle the /newtopic command
@router.message(Command("clear_cache"))
async def new_topic_cmd(message: types.Message):
    try:
        username = message.from_user.username
    except AttributeError:
        await message.answer("Please set a username in Telegram settings and try again.")
        return
    messages[username] = []
    await message.answer("Cleared the chat history!")

# Handle the /help command
@router.message(Command("help"))
async def help_cmd(message: types.Message):
    help_text = "/phoenix - Start the chat\n/help - Show this help message\n/clear_cache - Clear the chat history\n"
    await message.answer(help_text)

@router.message(lambda msg: True)
async def handle_message(message: types.Message):
    try:
        username = message.from_user.username
    except AttributeError:
        await message.answer("Please set a username in Telegram settings and try again.")
        return

    # Initialize message history for the user if not already present
    if username not in messages:
        messages[username] = []

    # Handle text and photo messages with if-else
    if message.photo or message.document:
        # Handle image messages
        try:
            # Notify the user that the bot is processing the image
            await bot.send_chat_action(chat_id=message.chat.id, action="typing")

            # Get the file_id of the largest photo
            file_id = message.photo[-1].file_id

            # Download the photo
            file = await bot.get_file(file_id)
            file_data = await bot.download_file(file.file_path)

            encoded_image = base64.b64encode(file_data.read()).decode('utf-8')

            # Prompt text accompanying the image
            user_message = message.caption if message.caption else "Please analyze the image."

            # Log the user's message and the image processing action
            logging.info(f'{username} sent an image with prompt: {user_message}')

            # Add the user's message and image URL to their message history
            messages[username].append({"role": "user", "content": user_message})
            messages[username].append({"role": "user", "content": f"data:image/png;base64,{encoded_image}"})

            # Notify the user that the bot is processing the image
            await bot.send_chat_action(chat_id=message.chat.id, action="typing")
            
            # Generate a response using OpenAI Vision API
            for attempt in range(3):
                logging.info(f"Sending image URL to OpenAI Vision API: {encoded_image}")
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": BOT_PERSONALITY + user_message},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}}
                            ]
                        }
                    ],
                    max_tokens=1000,
                )
                if response:
                    break

            # Notify the user that the bot is processing the image
            await bot.send_chat_action(chat_id=message.chat.id, action="typing")

            chatgpt_response = response.choices[0].message.content.strip()

            # Add the bot's response to the message history
            messages[username].append({"role": "assistant", "content": chatgpt_response})

            # Send the bot's response to the user
            await message.reply(chatgpt_response, parse_mode='Markdown')

        except Exception as e:
            logging.error(f"Error processing image or generating response: {e}")
            await message.answer("Sorry, something went wrong while processing your image.")
    else:
        # Handle text messages
        user_message = message.text

        # Add the user's message to their message history
        messages[username].append({"role": "user", "content": user_message})

        # Log the user's message
        logging.info(f'{username}: {user_message}')

        # Notify the user that the bot is typing
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        # Generate a response using OpenAI
        chatgpt_response = await generate_response(username)

        # Add the bot's response to the message history
        messages[username].append({"role": "assistant", "content": chatgpt_response})

        # Log the bot's response
        logging.info(f'ChatGPT response: {chatgpt_response}')

        # Send the bot's response to the chat
        await message.reply(chatgpt_response, parse_mode='Markdown')



async def main():
    # Set up the bot and dispatcher
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

