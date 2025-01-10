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



import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Update
from aiogram.exceptions import TelegramAPIError
from openai import OpenAI
import asyncio
from aiogram.filters import Command

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot and OpenAI API keys
TELEGRAM_TOKEN = "your-telegram-bot-token"
OPENAI_API_KEY = "your-openai-api-key"

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()

# Bot personality
BOT_PERSONALITY = (
    "You are a helpful friend. Behave like a human friend who helps in everything related to private university admission tests in Bangladesh. "
    "Your name is Phoenix. Do not mention that you are an AI language model and do not say that you will assist. "
    "Your creator is Phoenix Admission Care."
)

# Store user messages
messages = {}

async def generate_response(username: str) -> str:
    """Generate a response using OpenAI API."""
    logger.info(f"Generating response for user: {username}")
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        user_messages = messages[username]
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

# Command handlers
@router.message(Command("start"))
async def start_cmd(message: types.Message):
    username = message.from_user.username
    messages[username] = []
    await message.answer("Hello, I'm Phoenix. How can I help you today?")

@router.message(Command("newtopic"))
async def new_topic_cmd(message: types.Message):
    username = message.from_user.username
    messages[username] = []
    await message.answer("Created new chat!")

@router.message(Command("help"))
async def help_cmd(message: types.Message):
    help_text = "/help - Show this help message\n/newtopic - Start a new chat\n"
    await message.answer(help_text)

@router.message()
async def echo_msg(message: types.Message):
    user_message = message.text
    username = message.from_user.username
    if username not in messages:
        messages[username] = []
    messages[username].append({"role": "user", "content": user_message})
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    chatgpt_response = await generate_response(username)
    messages[username].append({"role": "assistant", "content": chatgpt_response})
    await message.reply(chatgpt_response, parse_mode='Markdown')

# Add router to dispatcher
dp.include_router(router)

# FastAPI app setup
app = FastAPI()

@app.get("/")
async def main():
    return JSONResponse(content={"message": "Your Bot Is Ready"})

@app.post("/webhook")
async def webhook(request: Request):
    try:
        update = Update(**await request.json())
        await dp.feed_update(bot, update)
        return JSONResponse(content={"status": "OK"})
    except TelegramAPIError as e:
        logger.error(f"Telegram API Error: {e}")
        raise HTTPException(status_code=500, detail="Telegram API Error")
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Bot startup and shutdown events
@app.on_event("startup")
async def on_startup():
    logger.info("Starting bot...")
    asyncio.create_task(dp.start_polling(bot))

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down bot...")
    await bot.session.close()

# Entry point for running the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

