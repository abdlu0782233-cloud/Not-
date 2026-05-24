import os
import time
import telebot
import requests

# --- الإعدادات الأساسية ---
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

bot = telebot.TeleBot(TOKEN)

print("🔄 تنظيف اتصالات السيرفر القديمة...")
try:
    bot.remove_webhook()
    time.sleep(1)
    print("✅ السيرفر جاهز ونظيف!")
except Exception as e:
    print(f"⚠️ تنبيه: {e}")

# دالة ذكية لإرسال النص مباشرة إلى جوجل وتجنب أخطاء المكتبات والـ 404
def ask_gemini_direct(text_prompt):
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
        return f"❌ فشل الاتصال المباشر بجوجل. السبب: {e}"

# --- معالج النصوص ---
@bot.message_handler(func=lambda m: True)
def handle_private_text(message
