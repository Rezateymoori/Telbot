from telegram.ext import Updater, MessageHandler, Filters
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def ai_reply(text):
    payload = {"inputs": text}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    data = response.json()
    return data[0]["generated_text"] if isinstance(data, list) else "پاسخی دریافت نشد."

def handle_message(update, context):
    chat_type = update.message.chat.type
    user_text = update.message.text

    if chat_type in ["group", "supergroup"] and f"@{context.bot.username}" in user_text:
        clean_text = user_text.replace(f"@{context.bot.username}", "").strip()
        reply = ai_reply(clean_text)
        update.message.reply_text(reply)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()