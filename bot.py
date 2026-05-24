import os
import time
import telebot
import requests

TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

bot = telebot.TeleBot(TOKEN)

# 1. تنظيف أي Webhook قديم لتجنب تعارض 409
print("🔄 تنظيف أي Webhook قديم...")
try:
    bot.remove_webhook()
    time.sleep(2) # تأخير بسيط لضمان فك الارتباط
except Exception as e:
    print(f"⚠️ خطأ أثناء تنظيف الـ Webhook: {e}")

def ask_gemini_direct(text_prompt):
    # استخدام المسار الصحيح للموديل
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": text_prompt}]}]}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ خطأ خادم (كود {response.status_code}): {response.text}"
    except Exception as e:
        return f"❌ فشل الاتصال: {e}"

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    if not message.text: return
    if message.text == "/start":
        bot.reply_to(message, "🚀 لارا تعمل الآن بكامل طاقتها!")
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_gemini_direct(message.text)
    bot.reply_to(message, reply)

if __name__ == "__main__":
    print("🚀 البوت يعمل الآن بنظام Polling آمن...")
    # skip_pending=True تقوم بتجاهل أي رسائل معلقة قد تسبب تعارضاً
    bot.infinity_polling(skip_pending=True)
