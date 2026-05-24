import os
import telebot
from flask import Flask, request
import google.generativeai as genai

# --- المفاتيح السرية ---
TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
WEBHOOK_URL = "https://web-production-aa4e6.up.railway.app/" 
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

# تهيئة البوت والذكاء الاصطناعي
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__) 

# قاموس لذاكرة الشات
chat_sessions = {}

# تفعيل الويب هوك تلقائياً عند بدء تشغيل الكود
try:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + TOKEN)
except Exception as e:
    print(f"Webhook setup error: {e}")

# --- [1] معالج الصور ---
@bot.message_handler(content_types=['photo'])
def handle_private_photo(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    caption = message.caption.strip() if message.caption else ""

    if not caption:
        caption = "حلل هذه الصورة واشرح ما بداخلها بالتفصيل باللغة العربية."

    try:
        msg_waiting = bot.reply_to(message, "🔄 لارة تقوم بتحميل الصورة وتحليلها بالذكاء الاصطناعي... انتظر لحظة.")
        
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_parts = [{"mime_type": "image/jpeg", "data": downloaded_file}]
        
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([caption, image_parts[0]])
        
        bot.edit_message_text(response.text, chat_id, msg_waiting.message_id)
    except Exception as e:
        bot.reply_to(message, "❌ نعتذر، فشل معالجة الصورة.")

# --- [2] معالج النصوص والذاكرة ---
@bot.message_handler(func=lambda m: True)
def handle_private_text(message):
    if not message.text: return
    text = message.text.strip()
    user_id = message.from_user.id

    if text == "/start":
        bot.reply_to(message, "🧠 أهلاً بك! أنا لارا مساعدتك الشخصية بالذكاء الاصطناعي.\n\nتحدث معي مباشرة في الخاص، أو أرسل لي صوراً لأقوم بتحليلها فوراً!")
        return

    try:
        if user_id not in chat_sessions:
            model = genai.GenerativeModel('gemini-1.5-pro')
            chat_sessions[user_id] = model.start_chat(history=[])
        
        response = chat_sessions[user_id].send_message(text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "❌ واجهت مشكلة في معالجة النص، حاول مجدداً.")

# مسار استقبال رسائل التليجرام
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# مسار الصفحة الرئيسية للتأكد من عمل السيرفر
@app.route('/')
def index():
    return "البوت يعمل بنجاح والذكاء الاصطناعي جاهز! 🚀", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
