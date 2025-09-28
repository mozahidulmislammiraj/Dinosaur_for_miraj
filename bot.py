import os, telebot, openai, threading
from flask import Flask

# Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise SystemExit("Missing TELEGRAM_TOKEN or OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Telegram bot logic
@bot.message_handler(commands=['start'])
def start_message(msg):
    bot.reply_to(msg, "Bot active ✅ — Send any message and I'll reply.")

@bot.message_handler(func=lambda m: True)
def chat_with_gpt(msg):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg.text}]
        )
        reply = response["choices"][0]["message"]["content"]
        bot.reply_to(msg, reply)
    except Exception as e:
        bot.reply_to(msg, "Error: " + str(e))

# Flask web server (Render expects port)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Run bot in background thread
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)