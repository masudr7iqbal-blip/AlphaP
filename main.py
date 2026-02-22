import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- আপনার সঠিক তথ্যগুলো এখানে নিশ্চিত করুন ---
API_TOKEN = '8530900754:AAFiFRX60Om1r485mTSdiEs37rvvjz78NbI'
ADMIN_ID = 5716499834 
STORAGE_BOT_USER = "GAlphaDrive_bot"
MAIN_CHANNEL_ID = -1002446777649 

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

@server.route("/")
def webhook():
    return "Alpha Premium Main Bot is Active!", 200

# --- স্টার্ট কমান্ড (সবার জন্য কাজ করবে) ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "**What can this bot do?**\n\n"
        "💬 আপনি কি আমাদের **Alpha Premium Content** গ্রুপে জয়েন হতে চান? "
        "যেখানে আছে আনলিমিটেড সেরা সব ভাইরাল কালেকশন। "
        "সব আপডেট পেতে আমাদের সাথে থাকুন।"
    )
    markup = InlineKeyboardMarkup()
    btn_group = InlineKeyboardButton("💎 Join Premium Group", url="https://t.me/+LFEmWRfqWmhjMmZl")
    markup.add(btn_group)
    bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- পোস্ট কমান্ড (শুধুমাত্র অ্যাডমিনের জন্য) ---
@bot.message_handler(commands=['post'])
def create_premium_post(message):
    if message.from_user.id == ADMIN_ID:
        try:
            # ফরম্যাট: /post [ফাইল_আইডি] [পোস্টার_লিঙ্ক] [নাম]
            args = message.text.split(maxsplit=3)
            if len(args) < 4:
                bot.reply_to(message, "❌ **সঠিক ফরম্যাট:**\n`/post 11 https://link.com/img.jpg Movie Name`", parse_mode="Markdown")
                return

            file_id, photo_url, movie_title = args[1], args[2], args[3]

            markup = InlineKeyboardMarkup()
            storage_link = f"https://t.me/{STORAGE_BOT_USER}?start={file_id}"
            markup.add(InlineKeyboardButton("🎬 ডেমো দেখুন", url=storage_link))
            markup.add(InlineKeyboardButton("💎 প্রিমিয়াম কিনুন", url="https://t.me/XpremiumB"))

            caption = (
                f"🔥 **NEW CONTENT RELEASED**\n\n"
                f"📺 **Content:** {movie_title}\n"
                f"✨ **Quality:** Ultra HD / Premium\n\n"
                f"👇 **নিচের বাটন থেকে ডেমো দেখুন অথবা ফুল এক্সেস কিনুন:**"
            )

            bot.send_photo(MAIN_CHANNEL_ID, photo_url, caption=caption, reply_markup=markup, parse_mode="Markdown")
            bot.reply_to(message, "✅ সফলভাবে চ্যানেলে পোস্ট করা হয়েছে!")
            
        except Exception as e:
            bot.reply_to(message, f"❌ ভুল হয়েছে: {str(e)}")
    else:
        bot.reply_to(message, f"⚠️ আপনি অনুমোদিত নন। আপনার আইডি: {message.from_user.id}")

def run():
    server.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
