import telebot, openai, os

# Environment থেকে key নিন
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # চাইলে "gpt-4" দিতে পারেন
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response["choices"][0]["message"]["content"]
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "Error: " + str(e))

bot.polling()
