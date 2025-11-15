import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8218013108:AAHh62XuqHWLkORJH-IwjgpNlXyPJX1QZp8"
bot = telebot.TeleBot(TOKEN)

# ذخیره‌سازی ساده برای هر کاربر
user_data = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "سلام! متن پستت رو بفرست.")


@bot.message_handler(content_types=['text', 'photo'])
def get_content(msg):
    uid = msg.from_user.id

    # عکس
    if msg.content_type == 'photo':
        file_id = msg.photo[-1].file_id
        user_data[uid] = {"photo": file_id}
        bot.reply_to(msg, "عکس ذخیره شد!\nمتن دکمه رو بفرست:")
        return

    # متن پست
    if uid not in user_data:
        user_data[uid] = {}

    if "text" not in user_data[uid]:
        user_data[uid]["text"] = msg.text
        bot.reply_to(msg, "متن دکمه رو بفرست:")
        return

    # متن دکمه
    if "btn_text" not in user_data[uid]:
        user_data[uid]["btn_text"] = msg.text
        bot.reply_to(msg, "لینک دکمه رو بفرست:")
        return

    # لینک دکمه
    if "btn_url" not in user_data[uid]:
        user_data[uid]["btn_url"] = msg.text
        bot.reply_to(msg, "آیدی چنل رو بفرست (مثلاً: @mychannel):")
        return

    # چنل
    user_data[uid]["channel"] = msg.text

    send_to_channel(msg)


def send_to_channel(msg):
    uid = msg.from_user.id
    data = user_data[uid]

    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text=data["btn_text"], url=data["btn_url"])
    markup.add(btn)

    try:
        if "photo" in data:
            bot.send_photo(
                chat_id=data["channel"],
                photo=data["photo"],
                caption=data.get("text", ""),
                reply_markup=markup
            )
        else:
            bot.send_message(
                chat_id=data["channel"],
                text=data["text"],
                reply_markup=markup
            )
        bot.reply_to(msg, "با موفقیت به چنل ارسال شد! 🎉")
    except Exception as e:
        bot.reply_to(msg, f"خطا: {e}")

    # پاک کردن داده‌ها
    user_data.pop(uid, None)


bot.polling()
