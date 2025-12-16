# Phoenix Telegram Bot

Phoenix Telegram Bot is a Telegram-based doubt-solving assistant built for **Phoenix Education / Phoenix Admission Care**.
The bot is designed to help students preparing for **Private University Admission Tests in Bangladesh**, especially in subjects like **Math, English, Analytical Ability, and General Knowledge**.

Students can mention this bot in Telegram groups to ask questions, clear doubts and even submit images of questions for explanation.

---

## 📌 Project Overview

* **Bot Name:** Phoenix
* **Platform:** Telegram
* **Target Users:** Admission test candidates of private universities in Bangladesh
* **Purpose:**

  * Act as a **24/7 doubt-solving partner**
  * Assist students with **admission-related academic questions**
  * Provide quick explanations in **simple, student-friendly language**
  * Analyze **images of questions** and give step-by-step answers

Phoenix behaves like a **helpful human friend**, not a formal assistant or AI, making learning more comfortable for students.

---

## ✨ Key Features

### ✅ Telegram Bot Integration

* Works in **Telegram groups**
* Students can mention the bot and ask questions

### ✅ Subject-wise Assistance

* Mathematics (Admission-level problems)
* English (Grammar, vocabulary, comprehension)
* Logical & Analytical questions
* General admission guidance

### ✅ Image-Based Question Solving

* Students can send **photos or scanned questions**
* The bot analyzes the image and explains the solution

### ✅ Conversational Memory

* Maintains **chat history per user**
* Allows contextual follow-up questions
* `/clear_cache` command resets conversation

### ✅ Human-like Personality

* Friendly tone
* Simple explanations
* No AI disclosure
* Acts as a senior helping junior students

### ✅ Web Server Keep-Alive

* Flask server ensures bot stays alive on cloud platforms

---

## 🛠️ Tech Stack

| Component            | Technology              |
| -------------------- | ----------------------- |
| Programming Language | Python                  |
| Bot Framework        | aiogram                 |
| AI Engine            | OpenAI API              |
| Image Processing     | Base64 Encoding         |
| Web Server           | Flask                   |
| Async Handling       | asyncio                 |
| Hosting Support      | Thread-based keep-alive |

---

## 📂 Project Structure

> All logic is handled inside a single Python file for simplicity and easy deployment.

---

## 🔐 Environment Setup

### 1️⃣ Install Dependencies

```bash
pip install aiogram flask openai pillow requests
```

### 2️⃣ Set API Keys

Inside the code, provide:

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
```

⚠️ **Important:**
Never expose API keys publicly in production. Use environment variables instead.

---

## ▶️ How to Run the Bot

```bash
python main.py
```

Once running:

* Flask server runs on port **8080**
* Telegram bot starts polling automatically

---

## 🤖 Bot Commands

| Command        | Description                 |
| -------------- | --------------------------- |
| `/phoenix`     | Start chatting with the bot |
| `/help`        | Show available commands     |
| `/clear_cache` | Clear chat history          |

---

## �� How the Bot Works

1. User sends a **text or image**
2. Message is stored in a **user-specific memory**
3. OpenAI processes:

   * Text-based queries
   * Image + text queries (Vision)
4. Bot replies in **simple, admission-focused language**
5. Chat history is updated for better follow-up responses

---

## 🖼️ Image Question Flow

* Student uploads a photo of a question
* Bot:

  * Converts image to Base64
  * Sends it with the question prompt
  * Receives explanation from OpenAI
* Returns a **clear, readable solution**

---

## 🎯 Use Case Example

> A student sends:
>
> * “Solve this math question” + image
> * Bot explains step by step without using LaTeX
> * Student asks a follow-up question
> * Bot continues from previous context

This makes Phoenix a true **study companion**, not just a Q&A bot.

---

## 🏫 Organization Behind the Project

**Phoenix Education**
An education-focused initiative helping Bangladeshi students prepare for private university admission tests through guidance, mentoring, and providing resources.

---

## ⚠️ Limitations

* Not intended for public exam cheating
* Responses depend on image clarity
* Requires active internet connection
* API usage cost depends on OpenAI plan

---

## 🚀 Future Improvements

* Subject-specific modes (Math-only, English-only)
* Admin broadcast system
* Daily practice questions
* Leaderboard & quizzes
* Bengali language support

---

## ❤️ Acknowledgements

* OpenAI for language & vision models
* aiogram for Telegram bot framework
* Phoenix Education students for inspiration

---
