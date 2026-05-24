import telebot
import requests

TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
# سأستخدم لك مفتاحاً عاماً للموديل المجاني
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(TOKEN)

def ask_openrouter(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://railway.app/",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-flash-1.5-8b",
        "messages": [{"role": "user", "content": text}]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: الرجاء التأكد من مفتاح الـ API في موقع OpenRouter."
    except Exception as e:
        return str(e)

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_openrouter(message.text)
    bot.reply_to(message, reply)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
