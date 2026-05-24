import telebot
import requests
import time

# --- الإعدادات ---
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

bot = telebot.TeleBot(TOKEN)

# إيقاف أي اتصال ويب هوك قديم يسبب تعارض
try:
    bot.remove_webhook()
except:
    pass

def ask_gemini(text):
    # استخدام المسار المباشر والمحدث لتجنب خطأ 404
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": text}]}]}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"خطأ الاتصال: {response.status_code}"
    except Exception as e:
        return str(e)

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    if message.text == "/start":
        bot.reply_to(message, "مرحباً! أنا لارا، كيف أساعدك؟")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        reply = ask_gemini(message.text)
        bot.reply_to(message, reply)

if __name__ == "__main__":
    # skip_pending=True تحل مشكلة الـ 409 Conflict نهائياً
    bot.infinity_polling(skip_pending=True)
