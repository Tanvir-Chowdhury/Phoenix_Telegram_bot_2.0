# import logging
# import asyncio
# from aiogram import Bot, Dispatcher, Router, types
# from aiogram.filters import Command
# from openai import OpenAI
# from aiogram.types import Update
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import uvicorn
# from aiogram.exceptions import TelegramAPIError

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Bot and OpenAI API keys
# TELEGRAM_TOKEN = "8078701645:AAGI970Rw9krnbfHRr-4DTh8wdQRo1vLZM4"
# OPENAI_API_KEY = "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"

# if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
#     raise ValueError("Please set TELEGRAM_TOKEN and OPENAI_API_KEY in the script.")

# # Initialize bot and dispatcher
# bot = Bot(token=TELEGRAM_TOKEN)
# dp = Dispatcher()
# router = Router()

# # Bot personality
# BOT_PERSONALITY = (
#     "You are a helpful friend. Behave like a human friend who helps in everything related to private university admission test in Bangladesh. "
#     "Your name is Phoenix. Do not mention that you are an AI language model and do not say that you will assist. "
#     "Your creator is Phoenix Admission Care."
# )

# # Create a dictionary to store messages for each user
# messages = {}

# async def generate_response(username: str) -> str:
#     """Generate a response using OpenAI API."""
#     logger.info(f"Generating response for user: {username}")
#     try:
#         client = OpenAI(api_key=OPENAI_API_KEY)
#         user_messages = messages[username]
#         conversation_history = [{"role": "system", "content": BOT_PERSONALITY}] + user_messages
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=conversation_history
#         )
#         generated_response = response.choices[0].message.content.strip()
#         logger.info(f"Response generated: {generated_response}")
#         return generated_response
#     except Exception as e:
#         logger.error(f"Error generating response: {e}")
#         return "Sorry, something went wrong while processing your request."

# @router.message(Command("start"))
# async def start_cmd(message: types.Message):
#     username = message.from_user.username
#     messages[username] = []
#     await message.answer("Hello, I'm Phoenix. How can I help you today?")

# @router.message(Command("newtopic"))
# async def new_topic_cmd(message: types.Message):
#     username = message.from_user.username
#     messages[username] = []
#     await message.answer("Created new chat!")

# @router.message(Command("help"))
# async def help_cmd(message: types.Message):
#     help_text = "/help - Show this help message\n/newtopic - Start a new chat\n"
#     await message.answer(help_text)

# @router.message()
# async def echo_msg(message: types.Message):
#     user_message = message.text
#     username = message.from_user.username
#     if username not in messages:
#         messages[username] = []
#     messages[username].append({"role": "user", "content": user_message})
#     await bot.send_chat_action(chat_id=message.chat.id, action="typing")
#     chatgpt_response = await generate_response(username)
#     messages[username].append({"role": "assistant", "content": chatgpt_response})
#     await message.reply(chatgpt_response, parse_mode='Markdown')

# # FastAPI app setup
# app = FastAPI()

# @app.get("/")
# async def main():
#     return JSONResponse(content={"message": "Your Bot Is Ready"})

# @app.post("/webhook")
# async def webhook(request: Request):
#     try:
#         update = Update(**await request.json())
#         await dp.feed_update(bot, update)
#         return JSONResponse(content={"status": "OK"})
#     except Exception as e:
#         logger.error(f"Error in webhook: {e}")
#         return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# # Include router in the dispatcher
# dp.include_router(router)

# # Entry point for the app
# if __name__ == "__main__":
    
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# Import necessary modules
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from flask import Flask
from threading import Thread
from openai import OpenAI

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
)

# Create a dictionary to store messages for each user
messages = {}

async def generate_response(username: str) -> str:
    """Generate a response using OpenAI API."""
    logger.info(f"Generating response for user: {username}")
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
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
    help_text = "/help - Show this help message\n/newtopic - Start a new chat\n"
    await message.answer(help_text)

# Handle all other messages
@router.message()
async def echo_msg(message: types.Message):
    user_message = message.text
    try:
        username = message.from_user.username
    except AttributeError:
        await message.answer("Please set a username in Telegram settings and try again.")
        return

    # If this is the first message from the user, initialize their message history
    if username not in messages:
        messages[username] = []

    # Add the user's message to their message history
    messages[username].append({"role": "user", "content": user_message})

    # Log the user's message
    logging.info(f'{username}: {user_message}')

    # Notify the user that the bot is typing
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # Generate a response using OpenAI
    chatgpt_response = await generate_response(username)

     # Notify the user that the bot is typing
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

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

