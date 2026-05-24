import os
import time
import telebot
import requests

# --- الإعدادات ---
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

bot = telebot.TeleBot(TOKEN)

# دالة الاتصال المباشر بجوجل بالمسار الصحيح والمستقر
def ask_gemini_direct(text_prompt):
    # استخدام المسار المحدث والمستقر
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": text_prompt}]
        }]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ خطأ من خادم جوجل (كود {response.status_code}):\n{response.text}"
    except Exception as e:
        return f"❌ فشل الاتصال. السبب: {e}"

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    if not message.text or message.text == "/start":
        bot.reply_to(message, "🚀 لارا جاهزة! أرسل سؤالك الآن.")
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_gemini_direct(message.text)
    bot.reply_to(message, reply)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
