import os
import telebot
import google.generativeai as genai

# --- الإعدادات والمفاتيح المدمجة بأمان ---
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

# تهيئة وإعداد تليجرام والذكاء الاصطناعي
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# قاموس لتخزين ذاكرة المحادثة المستمرة لكل مستخدم (شات خاص)
chat_sessions = {}

print("🔄 جاري إلغاء الـ Webhook القديم وتنظيف الاتصال...")
try:
    bot.remove_webhook()
    print("✅ تم تنظيف الاتصال بنجاح!")
except Exception as e:
    print(f"⚠️ تنبيه أثناء تنظيف الـ Webhook: {e}")

# --- [1] معالج الصور في الخاص ---
@bot.message_handler(content_types=['photo'])
def handle_private_photo(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    caption = message.caption.strip() if message.caption else ""

    if not caption:
        caption = "حلل هذه الصورة واشرح ما بداخلها بالتفصيل باللغة العربية."

    try:
        msg_waiting = bot.reply_to(message, "🔄 لارا تقوم بتحميل الصورة وتحليلها بالذكاء الاصطناعي الفائق... انتظر لحظة.")
        
        # تحميل ملف الصورة من تليجرام
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # تحويل الصورة إلى بايتات متوافقة
        image_parts = [{"mime_type": "image/jpeg", "data": downloaded_file}]
        
        # استخدام نموذج الذكاء الاصطناعي القوي في تحليل الصور
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([caption, image_parts[0]])
        
        bot.edit_message_text(response.text, chat_id, msg_waiting.message_id)
    except Exception as e:
        bot.reply_to(message, "❌ نعتذر، فشل معالجة الصورة. تأكد من إعدادات المفاتيح.")

# --- [2] معالج النصوص والمحادثة المستمرة (الذاكرة) ---
@bot.message_handler(func=lambda m: True)
def handle_private_text(message):
    if not message.text: return
    text = message.text.strip()
    user_id = message.from_user.id

    if text == "/start":
        bot.reply_to(message, "🧠 أهلاً بك! أنا لارا، مساعدتك الشخصية بأقوى ذكاء اصطناعي (Gemini Pro).\n\nيمكنك الآن التحدث معي مباشرة، وطرح أسئلتك، أو إرسال شفرات برمجية، أو حتى إرسال صور لأقوم بتحليلها وشرحها لك فوراً مع ميزة حفظ سياق كلامنا!")
        return

    try:
        # إنشاء جلسة شات محتفظة بالذاكرة للمستخدم
        if user_id not in chat_sessions:
            model = genai.GenerativeModel('gemini-1.5-pro')
            chat_sessions[user_id] = model.start_chat(history=[])
        
        # إرسال الرسالة واستقبال الرد بناءً على الذاكرة
        response = chat_sessions[user_id].send_message(text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "❌ عذراً، واجهت مشكلة في معالجة النص، يرجى المحاولة مرة أخرى.")

# تشغيل البوت بنظام السحب الدوري المستمر وتجاوز أي أخطاء اتصال مؤقتة
if __name__ == "__main__":
    print("🚀 بوت لارا الشخصي يعمل الآن بنظام Polling المستقر... أرسل رسالة في تليجرام!")
    bot.infinity_polling(skip_pending=True)
