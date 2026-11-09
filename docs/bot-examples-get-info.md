# دریافت چت آیدی و سندر آیدی

---

```python
from maxrubika import Bot
from maxrubika.bot.filters import ChatType

bot = Bot("Token") # در این خط توکن بات خود را وارد کنید

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

bot.run()
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-examples/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مثال‌ها</a>

</div>