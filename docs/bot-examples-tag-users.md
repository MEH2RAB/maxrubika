# تگ (منشن) کردن کاربران

---

```python
from maxrubika import Bot
from maxrubika.bot.filters import Text, IsReply, ChatType
import random
import json
import os
import asyncio

bot = Bot("Token") # در این خط توکن بات خود را وارد کنید

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

@bot.on_new_message(Text("^تگ") & IsReply() & ChatType("group"))
async def handle_reply_tag(bot, event):
    await handle_tag(bot, event, is_reply=True)

@bot.on_new_message(Text("^تگ") & ChatType("group"))
async def handle_normal_tag(bot, event):
    if not event.reply_to_message_id:
        await handle_tag(bot, event, is_reply=False)

@bot.on_new_message(Text("^فعال$") & ChatType("group"))
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

bot.run()
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-examples/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مثال‌ها</a>

</div>