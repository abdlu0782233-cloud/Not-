import os
import telebot
from flask import Flask, request
from google import genai
from google.genai import types

# --- الإعدادات والمفاتيح المدمجة بنجاح ---
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
WEBHOOK_URL = "https://web-production-aa4e6.up.railway.app/" 
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__) 

# تهيئة عميل الذكاء الاصطناعي الفائق
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# قاموس لتخزين ذاكرة المحادثة المستمرة لكل مستخدم
chat_sessions = {}

# --- [1] معالج الصور في الخاص ---
@bot.message_handler(content_types=['photo'])
def handle_private_photo(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    caption = message.caption.strip() if message.caption else ""

    # إذا لم يكتب المستخدم نصاً مع الصورة، نضع أمراً تلقائياً للتحليل
    if not caption:
        caption = "حلل هذه الصورة واشرح ما بداخلها بالتفصيل باللغة العربية."

    try:
        msg_waiting = bot.reply_to(message, "🔄 لارا تقوم بتحميل الصورة وتحليلها بالذكاء الاصطناعي الفائق... انتظر لحظة.")
        
        # تحميل ملف الصورة من تليجرام
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # إرسال الصورة والنص لأقوى نموذج (Gemini Pro)
        response = ai_client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[
                types.Part.from_bytes(data=downloaded_file, mime_type='image/jpeg'),
                caption
            ]
        )
        
        bot.edit_message_text(response.text, chat_id, msg_waiting.message_id)
    except Exception as e:
        bot.reply_to(message, "❌ نعتذر، فشل معالجة الصورة. تأكد من إعدادات السيرفر والمفاتيح.")

# --- [2] معالج النصوص والمحادثة المستمرة (الذاكرة) ---
@bot.message_handler(func=lambda m: True)
def handle_private_text(message):
    if not message.text: return
    text = message.text.strip()
    user_id = message.from_user.id

    # عند إرسال أمر البدء
    if text == "/start":
        bot.reply_to(message, "🧠 أهلاً بك! أنا لارا، مساعدتك الشخصية بأقوى ذكاء اصطناعي (Gemini Pro).\n\nيمكنك الآن التحدث معي مباشرة، وطرح أسئلتك، أو إرسال شفرات برمجية، أو حتى إرسال صور لأقوم بتحليلها وشرحها لك فوراً مع ميزة حفظ سياق كلامنا!")
        return

    try:
        # إنشاء جلسة شات محتفظة بالذاكرة للمستخدم إذا لم تكن موجودة سابقاً
        if user_id not in chat_sessions:
            chat_sessions[user_id] = ai_client.chats.create(model="gemini-2.5-pro")
        
        # إرسال الرسالة واستقبال الرد بناءً على الذاكرة والمحادثات السابقة
        response = chat_sessions[user_id].send_message(text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "❌ عذراً، واجهت مشكلة في معالجة النص، يرجى المحاولة مرة أخرى.")

# استقبال التحديثات والويب هوك
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook_setup():
    bot.remove_webhook()
    status = bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    if status: return "تم إطلاق بوت لارا الشخصي بنجاح بالتوقيت الجديد! 🚀🔥", 200
    else: return "فشل إعداد الويب هوك.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

