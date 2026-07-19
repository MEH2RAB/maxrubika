# مثال‌ها

---

<a id="bot_examples_simple_message"></a>
## [دریافت پیام ساده](#bot_examples_simple_message)

```python
from maxrubika import Bot

bot = Bot("Token")

@bot.on_command("start")
async def info(bot, event):
    await event.reply(f"سلام، پیام شما دریافت شد.")

bot.run()
```

---

<a id="bot_examples_user_info"></a>
## [نمایش اطلاعات کاربر](#bot_examples_user_info)

```python
from maxrubika import Bot
from maxrubika.bot.filters import ChatType

bot = Bot("Token")

@bot.on_command("start", ChatType("user"))
async def start(bot, event):
    i = await bot.get_chat_info(event.chat_id)

    first_name = getattr(i.data.chat, 'first_name', '-')
    last_name = getattr(i.data.chat, 'last_name', '-')
    username = getattr(i.data.chat, 'username', '-')

    await event.reply(f"""🔹 **نام:** {first_name}

🔸 **نام خانوادگی:** {last_name}

🔹 **نام‌کاربری:** {username}

🔸 **چت آیدی:**
`{event.chat_id}`

🔷 **سندر آیدی:**
`{event.author_id}`""")

@bot.on_command("start", ChatType(["group", "channel"]))
async def start_group(bot, event):
    r = await bot.get_chat_info(event.chat_id)
    await event.reply(f"🏷 **نام:** {r.data.chat.title}\n\n🆔 **چت آیدی:**\n`{event.chat_id}`")

bot.run(0)
```

---

<a id="bot_examples_dice_coin_random"></a>
## [تاس، سکه و عدد تصادفی](#bot_examples_dice_coin_random)

```python
from maxrubika import Bot
from maxrubika.bot.filters import Text
import random

bot = Bot("Token")

@bot.on_message(Text("^تاس"))
async def roll_dice(bot, event):
    dice = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    result = random.choice(dice)
    await event.reply(result)

@bot.on_message(Text("^سکه"))
async def coin(bot, event):
    result = random.choice(["🪙 شیر", "🪙 خط"])
    await event.reply(result)

@bot.on_message(Text("^عدد"))
async def random_number(bot, event):
    num = random.randint(1, 100)
    await event.reply(f"🔢 {num}")

bot.run(0)
```

---

<a id="bot_examples_echo_messages"></a>
## [اکو کردن پیام‌ها](#bot_examples_echo_messages)

```python
from maxrubika import Bot
from maxrubika.bot.filters import *

TOKEN = "Token"
SENDER_ID = ""

bot = Bot(TOKEN)

@bot.on_message(ChatType("group") & FromUser(SENDER_ID) & IsForwarded())
async def l(bot, event):
   await event.forward()
   await event.delete()

@bot.on_message(ChatType("group") & FromUser(SENDER_ID))
async def i(bot, event):
   await event.copy()
   await event.delete()

bot.run(0)
```

---

<a id="bot_examples_mute_users"></a>
## [سکوت کردن کاربران](#bot_examples_mute_users)

```python
from maxrubika import Bot
from maxrubika.bot.filters import ChatType, Text, IsReply, FromUser

token = "Token"
sender_id = ""

bot = Bot(token)
messages = {}
muted = []

@bot.middleware()
async def process_all_messages(bot, event, call_next):
    chat_id = str(event.chat_id)
    msg_id = event.msg_id
    author_id = event.author_id

    if chat_id not in messages:
        messages[chat_id] = []

    messages[chat_id].append({
        "msg_id": msg_id,
        "sender_id": author_id
    })

    if author_id in muted:
        try:
            await event.delete()
            return
        except: pass

    await call_next()

@bot.on_message(Text("^سکوت$") & ChatType("group") & FromUser(sender_id) & IsReply())
async def mute_user(bot, event):
    chat_id = str(event.chat_id)
    reply_to_id = event.reply_to_message_id

    target_sender = None
    for msg in messages.get(chat_id, []):
        if msg["msg_id"] == reply_to_id:
            target_sender = msg["sender_id"]
            break

    if not target_sender:
        await event.reply("**کاربر مورد نظر پیدا نشد!**")
        return

    if target_sender == sender_id:
        await event.reply("**شما نمی‌توانید خودتان را سکوت کنید!**")
        return

    if target_sender in muted:
        await event.reply(f"**[کاربر مورد نظر]({target_sender}) قبلاً سکوت شده است.**")
        return

    muted.append(target_sender)
    await event.reply(f"**[کاربر مورد نظر]({target_sender}) با موفیقت سکوت شد، از این پس پیام های کاربر از گروه حذف می‌شود.**")

@bot.on_message(Text("^لغو سکوت$") & ChatType("group") & FromUser(sender_id) & IsReply())
async def unmute_user(bot, event):
    chat_id = str(event.chat_id)
    reply_to_id = event.reply_to_message_id

    target_sender = None
    for msg in messages.get(chat_id, []):
        if msg["msg_id"] == reply_to_id:
            target_sender = msg["sender_id"]
            break

    if not target_sender:
        await event.reply("**کاربر مورد نظر پیدا نشد!**")
        return

    if target_sender in muted:
        muted.remove(target_sender)
        await event.reply(f"**سکوت [کاربر مورد نظر]({target_sender}) لغو شد.**")
    else:
        await event.reply(f"**[کاربر مورد نظر]({target_sender}) سکوت نبوده است.**")

bot.run(0)
```

---

<a id="bot_examples_tag_users"></a>
## [تگ (منشن) کردن کاربران](#bot_examples_tag_users)

```python
from maxrubika import Bot
from maxrubika.bot.filters import Text, IsReply, ChatType
import random
import json
import os
import asyncio

bot = Bot("Token")

DATA_FILE = "group_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

def get_group_data(chat_id):
    if chat_id not in data:
        data[chat_id] = {"admin": None, "users": []}
        save_data(data)
    return data[chat_id]

def is_admin(event):
    chat_id = str(event.chat_id)
    group_data = get_group_data(chat_id)
    return group_data["admin"] == str(event.author_id)

def get_non_admin_users(group_data, admin_id):
    return [user for user in group_data["users"] if user != admin_id]

def parse_tag_count(text):
    parts = text.split()
    if len(parts) > 1 and parts[1].isdigit():
        count = int(parts[1])
        if count == 0:
            raise ValueError("❌ **تعداد تگ نمی‌تواند ۰ باشد!**\nلطفاً عددی بین ۱ تا ۱۰۰۰ وارد کنید.")
        if count > 1000:
            raise ValueError("❌ **حداکثر تعداد برای تگ کردن ۱۰۰۰ نفر است!**\nلطفاً عددی کمتر از ۱۰۰۰ وارد کنید.")
        return count
    return 300

def generate_tags(users, count):
    positive_texts = [
        "سلام", "درود", "چه خبر؟", "خوبی؟", "چطوری؟",
        "عزیزم", "جانم", "گلم", "عشقم", "رفیق",
        "دوست خوبم", "نازنین", "مهربون", "زیبا", "خوشگل",
        "دلبر", "قشنگ", "استاد", "ماه من", "ستاره",
        "آفتاب", "شاهزاده", "سلطان", "دوست داشتنی",
        "خوش اخلاق", "بهترینی", "یک دونه‌ای", "ناز",
        "برادر", "خواهر", "ویژه", "خاص", "قهرمان"
    ]

    emojis = ["❤️", "🌹", "💫", "✨", "🌸", "💝", "🌟", "💗", "🌺", "💕"]
    
    selected = random.sample(users, min(count, len(users)))
    tags = []
    for i, user in enumerate(selected):
        text = random.choice(positive_texts)
        emoji = random.choice(emojis)
        tags.append(f"[{text} {emoji}]({user})")
    return tags

def chunk_tags(tags, max_per_message=30, per_line=3):
    messages = []
    for i in range(0, len(tags), max_per_message):
        chunk = tags[i:i + max_per_message]
        lines = [" | ".join(chunk[j:j+per_line]) for j in range(0, len(chunk), per_line)]
        messages.append("\n".join(lines))
    return messages

async def send_tag_messages(bot, chat_id, msg_id, tags, count, is_reply=False):
    messages = chunk_tags(tags)
    first_msg = f"✅ {count} نفر تگ شدند:\n\n{messages[0]}"

    if is_reply:
        await bot.send_message(chat_id, first_msg, reply_to_message_id=msg_id)
    else:
        await bot.send_message(chat_id, first_msg, reply_to_message_id=msg_id)

    for msg in messages[1:]:
        await asyncio.sleep(1)
        if is_reply:
            await bot.send_message(chat_id, msg, reply_to_message_id=msg_id)
        else:
            await bot.send_message(chat_id, msg, reply_to_message_id=msg_id)

async def handle_tag(bot, event, is_reply=False):
    chat_id = str(event.chat_id)
    author_id = str(event.author_id)

    if is_reply and not event.reply_to_message_id:
        return

    group_data = get_group_data(chat_id)

    if group_data["admin"] is None:
        await event.reply("❌ **ابتدا با نوشتن دستور 'فعال'، بات را فعال کنید.**")
        return

    if group_data["admin"] != author_id:
        await event.reply("❌ **فقط مدیر بات می‌تواند از این دستور استفاده کند!**")
        return

    users = get_non_admin_users(group_data, group_data["admin"])
    if not users:
        await event.reply("❌ **هیچ کاربری به جز مدیر در گروه ثبت نشده است!**")
        return

    try:
        count = parse_tag_count(event.text)
    except ValueError as e:
        await event.reply(str(e))
        return

    tags = generate_tags(users, count)

    if is_reply:
        msg_id = event.reply_to_message_id
    else:
        msg_id = event.msg_id

    await send_tag_messages(bot, chat_id, msg_id, tags, len(tags), is_reply)

@bot.on_message(Text("^تگ") & IsReply() & ChatType("group"))
async def handle_reply_tag(bot, event):
    await handle_tag(bot, event, is_reply=True)

@bot.on_message(Text("^تگ") & ChatType("group"))
async def handle_normal_tag(bot, event):
    if not event.reply_to_message_id:
        await handle_tag(bot, event, is_reply=False)

@bot.on_message(Text("^فعال$") & ChatType("group"))
async def set_admin(bot, event):
    chat_id = str(event.chat_id)
    author_id = str(event.author_id)
    group_data = get_group_data(chat_id)

    if group_data["admin"] is not None:
        admin_id = group_data["admin"]
        await event.reply(f"❌ **این بات قبلاً توسط [این کاربر]({admin_id}) فعال شده است!**\n\nتنها ایشان می‌توانند از بات استفاده کنند.")
        return

    group_data["admin"] = author_id
    if author_id not in group_data["users"]:
        group_data["users"].append(author_id)
    save_data(data)

    chat_info = await bot.get_chat_info(event.chat_id)
    title = chat_info.data.chat.title
    await event.reply(f"✅ **ثبت نام شما به عنوان مدیر بات در گروه '{title}' با موفقیت انجام شد.**\n\nشما اکنون می‌توانید از دستور 'تگ' برای منشن کردن کاربران استفاده فرمایید.")

@bot.on_message(ChatType("group"))
async def save_users(bot, event):
    chat_id = str(event.chat_id)
    author_id = str(event.author_id)
    group_data = get_group_data(chat_id)

    if author_id not in group_data["users"]:
        group_data["users"].append(author_id)
        save_data(data)

bot.run(0)
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">

<a href="../bot-guide/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>