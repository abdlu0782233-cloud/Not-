import telebot
import requests

# لا تضع أي مسافات هنا، فقط ضع المفاتيح بين العلامتين
TOKEN = "8699507145:AAGdWfpMNUXqk0Db1qSGinCJwjNBk1eXu5E"
OPENROUTER_API_KEY = "Sk-or-v1-049b43537b211a101fc95785e70043c0b1b133ca8fd705647b6258ca7ee7cdf1"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "google/gemini-2.0-flash-exp:free", "messages": [{"role": "user", "content": message.text}]}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
        else:
            reply = f"خطأ الاتصال (401): تأكد من المفتاح. كود الخطأ: {response.status_code}"
    except Exception as e:
        reply = "حدث خطأ في النظام."
        
    bot.reply_to(message, reply)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
