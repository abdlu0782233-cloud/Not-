import telebot
import requests

# استخدم مفتاحك الجديد والمباشر هنا
OPENROUTER_API_KEY = "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"
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"

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
            return f"خطأ ({response.status_code}): تأكد من أن مفتاحك صالح في موقع OpenRouter."
    except Exception as e:
        return f"حدث خطأ: {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_openrouter(message.text)
    bot.reply_to(message, reply)

if __name__ == "__main__":
    # هذا السطر ينهي أي تعارض للـ 409
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
