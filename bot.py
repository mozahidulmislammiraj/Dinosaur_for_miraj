import os, telebot, openai, threading
from flask import Flask

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(func=lambda m: True)
def chat_with_gpt(msg):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": msg.text}]
        )
        reply = response.choices[0].message.content
        bot.reply_to(msg, reply)
    except Exception as e:
        bot.reply_to(msg, "Error: " + str(e))

# Flask server for Render
app = Flask(__name__)
@app.route("/")
def home():
    return "Bot is running ✅"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)