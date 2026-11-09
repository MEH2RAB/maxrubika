# بررسی عضویت

---

## روش اول: بررسی عضویت به صورت مستقیم

```python
from maxrubika import Bot
from maxrubika.bot.filters import IsUser
from maxrubika.bot.exceptions import InvalidAccess

bot = Bot("Token") # توکن بات خود اینجا وارد شود

channel_id = "" # چت آیدی کانال اینجا وارد شود
username = "" # یوزرنیم کانال اینجا وارد شود

info = bot.get_chat_info(channel_id)

@bot.on_command("start", IsUser())
async def start(bot, event):
    try:
        await bot.get_chat_member(channel_id, event.sender_id)
    except InvalidAccess:
        await event.reply(f"‼ **ابتدا در کانال {username} عضو شوید و سپس مجدد بات را استارت کنید.**")
        return

    await event.reply(f"✅ **عضویت شما در کانال {info.title} تایید شد.**")

bot.run()
```

---

## روش دوم: بررسی عضویت با استفاده از فیلتر

```python
from maxrubika import Bot
from maxrubika.bot.filters import IsJoined, IsUser

bot = Bot("Token")  # توکن بات خود را اینجا وارد کنید

chat_ids = [  # چت آیدی گفتگو های مورد نظر را اینجا وارد کنید
    "",
    "",
]

usernames = ["", ""]  # نام کاربری یا لینک گفتگوهای مورد نظر خود را اینجا وارد کنید

@bot.on_command("start", ~IsJoined(chat_ids), IsUser())
async def not_joined(bot, event):
    links = "\n".join(f"👉 {link}" for link in usernames)
    await event.reply(f"‼ **ابتدا در کانال‌های زیر عضو شوید و سپس مجدد بات را استارت کنید.**\n{links}")

@bot.on_command("start", IsJoined(chat_ids), IsUser())
async def joined(bot, event):
    await event.reply("✅ **عضویت شما تایید شد.**")

bot.run()
```

---

## روش سوم: بررسی عضویت و اجازه‌ی ارسال پیام در گروه

```python
import asyncio
import time
from maxrubika import Bot
from maxrubika.bot.filters import IsGroup, IsJoined, FromChat

bot = Bot("Token") # توکن بات خود را اینجا وارد کنید

CHANNEL_LINK = ["@TheMAXRubika", "@TheProgrammer"] # نام کاربری کانال‌های مورد نظر را اینجا وارد کنید

GROUP_ID = "" # چت آیدی گروه خود را اینجا وارد کنید

info = bot.get_chat_info(GROUP_ID)
channels = "\n".join(f"👉 {link}" for link in CHANNEL_LINK)
sleep = 100
warned_users = {}

@bot.on_new_message(IsGroup() & ~IsJoined(CHANNEL_LINK) & FromChat(GROUP_ID))
async def not_joined(bot, event):
    chat_id = event.chat_id
    author_id = event.author_id
    now = time.time()

    last_warn = warned_users.get(chat_id, {}).get(author_id, 0)

    if now - last_warn < sleep:
        await event.delete()
        return

    warned_users.setdefault(chat_id, {})[author_id] = now

    await event.delete()

    warn = await bot.send_message(
        chat_id,
        f"⚠ **[کاربر گرامی]({author_id})**\n\n"
        f"برای ارسال پیام در گروه {info.title} ابتدا در کانال‌های زیر عضو شوید:\n\n"
        f"{channels}"
    )

    asyncio.create_task(bot.auto_delete_message(event.chat_id, warn.message_id, 60))

bot.run()
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-examples/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مثال‌ها</a>

</div>