import os
import time
import telebot
import requests

# --- الإعدادات الأساسية والمفاتيح ---
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

bot = telebot.TeleBot(TOKEN)

print("🔄 تنظيف اتصالات السيرفر القديمة والويب هوك...")
try:
    bot.remove_webhook()
    time.sleep(1)
    print("✅ السيرفر نظيف تماماً وجاهز!")
except Exception as e:
    print(f"⚠️ تنبيه أثناء التنظيف: {e}")

# دالة الاتصال المباشر بجوجل لتجاوز مشاكل الـ 404 وإصدارات المكتبة القديمة
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

# --- معالج النصوص والرسائل الفردية ---
@bot.message_handler(func=lambda message: True)
def handle_private_text(message):
    if not message.text:
        return
    
    text = message.text.strip()

    if text == "/start":
        bot.reply_to(message, "🧠 أهلاً بك! أنا لارا، مساعدتك الشخصية بأقوى ذكاء اصطناعي مستقر ومباشر.\n\nتحدث معي الآن وسأجيبك فوراً!")
        return

    # تشغيل حركة "جاري الكتابة..." لتأكيد التفاعل
    try:
        bot.send_chat_action(message.chat.id, 'typing')
    except Exception:
        pass
    
    # جلب الرد من خادم جوجل مباشرة
    reply = ask_gemini_direct(text)
    
    # إرسال الإجابة للمستخدم
    bot.reply_to(message, reply)

# تشغيل البوت بنظام السحب الدوري وتخطي أي رسائل قديمة عالقة بالخلفية
if __name__ == "__main__":
    print("🚀 بوت لارا ينطلق الآن بأقوى وأسرع اتصال مباشر...")
    bot.infinity_polling(skip_pending=True)
