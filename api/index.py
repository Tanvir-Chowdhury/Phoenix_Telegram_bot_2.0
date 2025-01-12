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


# Function to upload the image to ImgBB
def upload_image_to_imgbb(file_data):
    try:
        # Ensure that the image is saved in JPEG format
        image = Image.open(BytesIO(file_data))
        output = BytesIO()
        image.convert("RGB").save(output, format="JPEG")
        output.seek(0)

        # Convert the image to base64
        encoded_image = base64.b64encode(output.getvalue()).decode('utf-8')

        # Prepare the request to ImgBB
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "c90d51820f6ac98aaac3a710e84371a4",
            "image": encoded_image
        }

        response = requests.post(url, data=payload)
        logging.info(f"ImgBB response status code: {response.status_code}")
        logging.info(f"ImgBB response text: {response.text}")

        if response.status_code == 200:
            result = response.json()
            logging.info(f"Image uploaded successfully to ImgBB: {result['data']['url']}")
            return result['data']['url']
        else:
            logging.error(f"Failed to upload image to ImgBB: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Exception during image upload to ImgBB: {str(e)}")
        return None



@router.message(lambda msg: msg.photo)
async def process_image(message: types.Message):
    try:
        username = message.from_user.username
    except AttributeError:
        await message.answer("Please set a username in Telegram settings and try again.")
        return

    # Initialize message history for the user if not already present
    if username not in messages:
        messages[username] = []

    # Notify the user that the bot is processing the image
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Get the file_id of the largest photo
    file_id = message.photo[-1].file_id

    # Download the photo
    try:
        file = await bot.get_file(file_id)
        file_data = await bot.download_file(file.file_path)


        # Convert to JPEG if needed
        try:
            image = Image.open(BytesIO(file_data))
            output = BytesIO()
            image.convert("RGB").save(output, format="JPEG")
            file_data = output.getvalue()  # Update the file_data with JPEG content
            logging.info("Converted image to JPEG format")
        except Exception as e:
            logging.error(f"Error processing image format: {str(e)}")
            bot.reply_to(message, "Failed to process the image format.")
            return
        
        # Upload image to ImgBB
        image_url = upload_image_to_imgbb(file_data)
        if not image_url:
            bot.reply_to(message, "Failed to upload image to ImgBB.")
            return

        # Encode the image to Base64
        # base64_image = encode_image(photo_bytes)

        # Prompt text accompanying the image
        user_message = message.caption if message.caption else "Please analyze the image."

        # Log the user's message and the image processing action
        logging.info(f'{username} sent an image with prompt: {user_message}')

        # Add the user's message and encoded image to their message history
        messages[username].append({"role": "user", "content": user_message})
        messages[username].append({"role": "user", "content": image_url})

        # Prepare the conversation history for the OpenAI API
        # conversation_history = [{"role": "system", "content": BOT_PERSONALITY}] + messages[username]

        # Notify the user that the bot is processing the image
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        for attempt in range(3):
            # Log the image URL being sent
            logging.info(f"Sending image URL to OpenAI Vision API: {image_url}")

            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Ensure you're using the correct GPT-4 Vision model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_message},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
            )
        

        chatgpt_response = response.choices[0].message.content.strip()

        # Notify the user that the bot is processing the image
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        # Add the bot's response to the message history
        messages[username].append({"role": "assistant", "content": chatgpt_response})

        # Send the bot's response to the user
        await message.reply(chatgpt_response, parse_mode='Markdown')

    except Exception as e:
        logging.error(f"Error processing image or generating response: {e}")
        await message.answer("Sorry, something went wrong while processing your image.")


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

# Handle all other messages
# @router.message(lambda msg: msg.photo)
# async def echo_msg(message: types.Message):
#     user_message = message.text
#     try:
#         username = message.from_user.username
#     except AttributeError:
#         await message.answer("Please set a username in Telegram settings and try again.")
#         return

#     # If this is the first message from the user, initialize their message history
#     if username not in messages:
#         messages[username] = []

#     # Add the user's message to their message history
#     messages[username].append({"role": "user", "content": user_message})

#     # Log the user's message
#     logging.info(f'{username}: {user_message}')

#     # Notify the user that the bot is typing
#     await bot.send_chat_action(chat_id=message.chat.id, action="typing")

#     # Generate a response using OpenAI
#     chatgpt_response = await generate_response(username)

#      # Notify the user that the bot is typing
#     await bot.send_chat_action(chat_id=message.chat.id, action="typing")

#     # Add the bot's response to the message history
#     messages[username].append({"role": "assistant", "content": chatgpt_response})

#     # Log the bot's response
#     logging.info(f'ChatGPT response: {chatgpt_response}')

#     # Send the bot's response to the chat
#     await message.reply(chatgpt_response, parse_mode='Markdown')

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
    if message.photo:
        # Handle image messages
        try:
            # Notify the user that the bot is processing the image
            await bot.send_chat_action(chat_id=message.chat.id, action="typing")

            # Get the file_id of the largest photo
            file_id = message.photo[-1].file_id

            # Download the photo
            file = await bot.get_file(file_id)
            file_data = await bot.download_file(file.file_path)

            # Convert to JPEG if needed
            try:
                image = Image.open(BytesIO(file_data))
                output = BytesIO()
                image.convert("RGB").save(output, format="JPEG")
                file_data = output.getvalue()  # Update the file_data with JPEG content
                logging.info("Converted image to JPEG format")
            except Exception as e:
                logging.error(f"Error processing image format: {str(e)}")
                await message.reply("Failed to process the image format.")
                return

            # Upload image to ImgBB
            image_url = upload_image_to_imgbb(file_data)
            if not image_url:
                await message.reply("Failed to upload image to ImgBB.")
                return

            # Prompt text accompanying the image
            user_message = message.caption if message.caption else "Please analyze the image."

            # Log the user's message and the image processing action
            logging.info(f'{username} sent an image with prompt: {user_message}')

            # Add the user's message and image URL to their message history
            messages[username].append({"role": "user", "content": user_message})
            messages[username].append({"role": "user", "content": image_url})

            # Notify the user that the bot is processing the image
            await bot.send_chat_action(chat_id=message.chat.id, action="typing")

            # Generate a response using OpenAI Vision API
            for attempt in range(3):
                logging.info(f"Sending image URL to OpenAI Vision API: {image_url}")
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_message},
                                {"type": "image_url", "image_url": {"url": image_url}}
                            ]
                        }
                    ],
                    max_tokens=1000,
                )
                if response:
                    break

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

