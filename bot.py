import re
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus

API_TOKEN = "8218013108:AAHh62XuqHWLkORJH-IwjgpNlXyPJX1QZp8"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# دیتای موقت کاربر
user_data = {}

# regex چک لینک پست
POST_LINK_PATTERN = r"https?:\/\/t\.me\/([A-Za-z0-9_]+)/(\d+)"

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.reply(
        "سلام! 👋\n"
        "عکس، کپشن، دکمه و لینک بده، من پست کامل می‌سازم و فقط اگر صاحب کانال باشی ارسال می‌کنم.\n\n"
        "اول لینک کانال رو بفرست:"
    )
    user_data[msg.from_user.id] = {}

# Step 1: گرفتن لینک کانال
@dp.message(F.text)
async def step_channel(msg: types.Message):
    user_id = msg.from_user.id

    if "channel" not in user_data[user_id]:
        user_data[user_id]["channel"] = msg.text.strip()
        await msg.reply("اوکی ✔️\nحالا **عکس** بفرست یا بگو «ندارم».")
        return

    # Step 2: عکس
    if "photo" not in user_data[user_id]:
        if msg.photo:
            user_data[user_id]["photo"] = msg.photo[-1].file_id
            await msg.reply("عکس ذخیره شد ✔️\nحالا کپشن بده:")
        else:
            user_data[user_id]["photo"] = None
            await msg.reply("بدون عکس ادامه میدم ✔️\nکپشن بده:")
        return

    # Step 3: کپشن
    if "caption" not in user_data[user_id]:
        user_data[user_id]["caption"] = msg.text
        await msg.reply("کپشن ذخیره شد ✔️\n\nحالا متن دکمه رو بده:")
        return

    # Step 4: متن دکمه
    if "btn_text" not in user_data[user_id]:
        user_data[user_id]["btn_text"] = msg.text
        await msg.reply("اوکی ✔️\nحالا لینک دکمه رو بده:")
        return

    # Step 5: لینک دکمه
    if "btn_url" not in user_data[user_id]:
        user_data[user_id]["btn_url"] = msg.text
        await msg.reply("همه‌چی آمادست! ⏳\nپست داره چک میشه...")

        await send_post(msg)
        return


async def send_post(msg: types.Message):
    user_id = msg.from_user.id
    data = user_data[user_id]

    channel = data["channel"]

    # چک اینکه لینک کانال t.me/xxxx هست
    if not channel.startswith("https://t.me/"):
        await msg.reply("❌ لینک کانال معتبر نیست.")
        return

    username = channel.replace("https://t.me/", "")

    # گرفتن اطلاعات کانال
    try:
        chat = await bot.get_chat(username)
    except:
        return await msg.reply("❌ ربات به کانال دسترسی ندارد.")

    # چک ادمین بودن ربات
    bot_member = await bot.get_chat_member(chat.id, (await bot.me).id)
    if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await msg.reply("❌ ربات در کانال ادمین نیست.")

    # پیدا کردن صاحب کانال
    admins = await bot.get_chat_administrators(chat.id)
    owner_id = None
    for a in admins:
        if a.status == ChatMemberStatus.OWNER:
            owner_id = a.user.id

    if owner_id != msg.from_user.id:
        return await msg.reply("❌ فقط صاحب کانال می‌تواند پست ارسال کند.")

    # ساخت دکمه
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=data["btn_text"], url=data["btn_url"])]
        ]
    )

    # ارسال پست
    try:
        if data["photo"]:
            await bot.send_photo(
                chat_id=chat.id,
                photo=data["photo"],
                caption=data["caption"],
                reply_markup=keyboard
            )
        else:
            await bot.send_message(
                chat_id=chat.id,
                text=data["caption"],
                reply_markup=keyboard
            )
    except Exception as e:
        return await msg.reply(f"❌ خطا در ارسال پست: {e}")

    await msg.reply("✔️ پست با موفقیت داخل کانال ارسال شد!")
    user_data.pop(user_id, None)
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run).start()
