import os
import time
import telebot
import google.generativeai as genai

# --- المفاتيح والتوكن ---
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

# تهيئة تليجرام وإعداد الذكاء الاصطناعي
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# قاموس لذاكرة المحادثة المستمرة
chat_sessions = {}

print("🔄 تنظيف أي اتصالات أو ويب هوك قديم...")
try:
    bot.remove_webhook()
    time.sleep(1)  # تأخير بسيط لضمان فك التعارض مع السيرفر القديم
    print("✅ تم تنظيف الاتصال بنجاح!")
except Exception as e:
    print(f"⚠️ تنبيه: {e}")

# --- [1] معالج الصور ---
@bot.message_handler(content_types=['photo'])
def handle_private_photo(message):
    chat_id = message.chat.id
    caption = message.caption.strip() if message.caption else "حلل هذه الصورة واشرح ما بداخلها بالتفصيل باللغة العربية."

    try:
        msg_waiting = bot.reply_to(message, "🔄 لارا تقوم بتحميل الصورة وتحليلها بالذكاء الاصطناعي الفائق...")
        
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_parts = [{"mime_type": "image/jpeg", "data": downloaded_file}]
        
        # استخدام النموذج الأساسي المستقر بالمسار الصحيح
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([caption, image_parts[0]])
        
        bot.edit_message_text(response.text, chat_id, msg_waiting.message_id)
    except Exception as e:
        bot.reply_to(message, f"❌ فشل معالجة الصورة. السبب: {e}")

# --- [2] معالج النصوص والذاكرة ---
@bot.message_handler(func=lambda m: True)
def handle_private_text(message):
    if not message.text: return
    text = message.text.strip()
    user_id = message.from_user.id

    if text == "/start":
        bot.reply_to(message, "🧠 أهلاً بك! أنا لارا، مساعدتك الشخصية بأقوى ذكاء اصطناعي.\n\nتحدث معي مباشرة، وطرح أسئلتك، أو أرسل صوراً لأقوم بتحليلها فوراً!")
        return

    try:
        # إنشاء جلسة شات بالمسار المحدث المستقر
        if user_id not in chat_sessions:
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat_sessions[user_id] = model.start_chat(history=[])
        
        response = chat_sessions[user_id].send_message(text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"❌ عذراً، واجهت مشكلة في الاتصال بالذكاء الاصطناعي.\nالسبب: {e}")

if __name__ == "__main__":
    print("🚀 بوت لارا الشخصي ينطلق الآن بنظام Polling المستقر...")
    # استخدام سريان نظيف وتخطي الرسائل المتراكمة القديمة لحل التعارض 409
    bot.infinity_polling(skip_pending=True)
