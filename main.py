import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- কনফিগারেশন (আপনার তথ্যগুলো এখানে দিন) ---
API_TOKEN = '8530900754:AAFiFRX60Om1r485mTSdiEs37rvvjz78NbI'
ADMIN_ID = 5716499834 
STORAGE_BOT_USER = "GAlphaDrive_bot" # আপনার স্টোরেজ বটের ইউজারনেম
MAIN_CHANNEL_ID = -1002446777649  # আপনার মেইন চ্যানেলের আইডি

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Alpha Premium Main Bot is Live!"

# --- স্টার্ট কমান্ড ---
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
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- পোস্ট তৈরি করার কমান্ড (অ্যাডমিনের জন্য) ---
@bot.message_handler(commands=['post'])
def create_premium_post(message):
    if message.from_user.id == ADMIN_ID:
        try:
            # ফরম্যাট: /post [ফাইল_আইডি] [পোস্টার_লিঙ্ক] [মুভির নাম]
            args = message.text.split(maxsplit=3)
            if len(args) < 4:
                bot.reply_to(message, "❌ **সঠিকভাবে লিখুন:**\n`/post 11 https://link.com/photo.jpg Inception`", parse_mode="Markdown")
                return

            file_id = args[1]
            photo_url = args[2]
            movie_title = args[3]

            # বাটন সেটআপ
            markup = InlineKeyboardMarkup()
            
            # ১. ডেমো দেখুন বাটন (স্টোরেজ বটে নিয়ে যাবে)
            storage_link = f"https://t.me/{STORAGE_BOT_USER}?start={file_id}"
            btn_demo = InlineKeyboardButton("🎬 ডেমো দেখুন", url=storage_link)
            
            # ২. প্রিমিয়াম কিনুন বাটন
            btn_premium = InlineKeyboardButton("💎 প্রিমিয়াম কিনুন", url="https://t.me/XpremiumB")
            
            # বাটনগুলো নিচে নিচে সাজানো
            markup.add(btn_demo)
            markup.add(btn_premium)

            caption = (
                f"🔥 **NEW CONTENT RELEASED**\n\n"
                f"📺 **Content:** {movie_title}\n"
                f"✨ **Quality:** Ultra HD / Premium\n\n"
                f"👇 **নিচের বাটন থেকে ডেমো দেখুন অথবা ফুল এক্সেস কিনুন:**"
            )

            # সরাসরি চ্যানেলে পোস্ট পাঠানো
            bot.send_photo(MAIN_CHANNEL_ID, photo_url, caption=caption, reply_markup=markup, parse_mode="Markdown")
            bot.reply_to(message, "✅ পোস্টটি সফলভাবে চ্যানেলে পাঠানো হয়েছে!")
            
        except Exception as e:
            bot.reply_to(message, f"❌ ভুল হয়েছে: {str(e)}")
    else:
        bot.reply_to(message, "⚠️ আপনি এই কমান্ডটি ব্যবহার করার অনুমতি নেই।")

def run():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
