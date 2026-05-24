import telebot
import requests

# التوكن الجديد الخاص بك
TOKEN = "8699507145:AAGdWfpMNUXqk0Db1qSGinCJwjNBk1eXu5E"
# مفتاح OpenRouter الجديد (إذا استمر خطأ 401، أنشئ مفتاحاً جديداً من موقعهم)
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(TOKEN)

def ask_openrouter(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": text}]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"خطأ ({response.status_code}): تأكد من مفتاح OpenRouter."
    except Exception as e:
        return f"خطأ: {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_openrouter(message.text)
    bot.reply_to(message, reply)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
