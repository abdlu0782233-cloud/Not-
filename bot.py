import telebot
import requests

TOKEN = "8984182509:AAFwLft__ZRL52grDeqTstV37ZRVcSr6URQ"
GEMINI_API_KEY = "AIzaSyA-gSgaswIYJevC7ZF-Gr_zQj2Pj0UXYMQ"

bot = telebot.TeleBot(TOKEN)

def ask_gemini(text):
    # نغير المسار لمسار عام عالمي
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": text}]}]}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"عذراً، الخدمة غير متاحة في منطقتك حالياً (كود {response.status_code})"
    except Exception as e:
        return str(e)

@bot.message_handler(func=lambda m: True)
def handle(message):
    reply = ask_gemini(message.text)
    bot.reply_to(message, reply)

if __name__ == "__main__":
    bot.infinity_polling()
