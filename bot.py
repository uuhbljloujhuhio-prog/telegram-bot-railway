import telebot
from flask import Flask, request
import os

# توکن ربات از محیط Railway (Environment Variable)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ✅ لیست کانال‌هایی که باید کاربر عضو باشه
REQUIRED_CHANNELS = [
    "@iranmovazii",
    "@money_money_only",
    "@footballfifal",
    "@frylensery"
]

# 🟢 بررسی عضویت کاربر در کانال‌ها
def is_subscribed(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

# 🚀 دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📂 دریافت فایل", url="https://t.me/ktztkdkydlydx"))
        bot.send_message(message.chat.id, "✅ عضویت شما تأیید شد!\nروی دکمه زیر بزن تا فایل رو دریافت کنی:", reply_markup=markup)
    else:
        text = "❌ برای دریافت فایل باید در کانال‌های زیر عضو شوید:\n\n"
        for ch in REQUIRED_CHANNELS:
            text += f"👉 {ch}\n"
        text += "\nپس از عضویت، دوباره /start را بزن ✅"
        bot.send_message(message.chat.id, text)

# 🌐 Webhook برای Railway
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    # ست کردن Webhook خودکار
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.environ.get('RAILWAY_STATIC_URL')}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
