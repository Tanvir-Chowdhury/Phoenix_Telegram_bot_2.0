import logging
import os
from flask import Flask, request
import requests
from aiogram import Bot
from openai import OpenAI

# Flask app setup
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch Telegram and OpenAI API keys from environment variables
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Please set TELEGRAM_TOKEN and OPENAI_API_KEY in the environment variables.")

# Initialize the bot
bot = Bot(token=TELEGRAM_TOKEN)

# Bot personality
BOT_PERSONALITY = (
    "You are a helpful friend. Behave like a human friend who helps in everything related to private university admission test in Bangladesh. "
    "Your name is Phoenix. Do not mention that you are an AI language model and do not say that you will assist. "
    "Your creator is Phoenix Admission Care."
)

# Create a dictionary to store conversation history for each user
messages = {}

# Set the Telegram webhook
def set_webhook():
    webhook_url = f"https://phoenix-telegram-bot-2-0.onrender.com/{TELEGRAM_TOKEN}"  
    try:
        response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={webhook_url}")
        if response.status_code == 200:
            logger.info("Webhook set successfully.")
        else:
            logger.error(f"Failed to set webhook: {response.text}")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")

# Endpoint to receive messages from Telegram
@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    user_message = message.get("text")

    if not chat_id or not user_message:
        return "Invalid message", 400

    logger.info(f"Received message: {user_message} from chat ID: {chat_id}")

    # Fetch or create conversation history for the user
    if chat_id not in messages:
        messages[chat_id] = []

    # Add the new message to the history
    messages[chat_id].append({"role": "user", "content": user_message})

    # Generate response from OpenAI
    response = generate_response(chat_id)

    # Send the generated response to Telegram
    send_telegram_message(chat_id, response)

    return "OK", 200

def generate_response(chat_id: str) -> str:
    """Generate a response using OpenAI API with conversation history."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        # Include the system message at the start of the conversation
        conversation_history = [{"role": "system", "content": BOT_PERSONALITY}] + messages[chat_id]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": BOT_PERSONALITY},
                {"role": "user", "content": conversation_history,
                }
            ]
        )

        # Extract the generated response
        generated_response = response.choices[0].message.content.strip()
        logger.info(f"Response generated: {generated_response}")

        # Add the assistant's response to the conversation history
        messages[chat_id].append({"role": "assistant", "content": generated_response})

        return generated_response
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Sorry, something went wrong while processing your request."

def send_telegram_message(chat_id, message):
    """Send message to Telegram using bot."""
    try:
        bot.send_message(chat_id, message)
        logger.info(f"Sent message: {message} to chat ID: {chat_id}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

# Main route to check if the bot is working
@app.route('/')
def home():
    return "Your Bot Is Ready!"

if __name__ == '__main__':
    # Set up Flask to listen on the correct port for Render
    set_webhook()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
