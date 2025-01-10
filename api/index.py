import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from openai import OpenAI
from flask import Flask, request
from aiogram.types import Update

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot and OpenAI API keys
TELEGRAM_TOKEN = "8078701645:AAGI970Rw9krnbfHRr-4DTh8wdQRo1vLZM4" 
OPENAI_API_KEY = "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"  

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Please set TELEGRAM_TOKEN and OPENAI_API_KEY in the script.")

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()

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

# Flask app setup
app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return "Your Bot Is Ready"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = types.Update(**request.get_json())
    asyncio.run(dp.feed_update(bot, update))
    return "OK", 200

# Entry point for Vercel
if __name__ == "__main__":
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # app.run(host="0.0.0.0", port=8080)
    app.run()
