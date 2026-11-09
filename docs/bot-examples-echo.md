# اکو کردن پیام‌ها

---

## روش اول: با استفاده از فیلترها

```python
from maxrubika import Bot
from maxrubika.bot.filters import *

TOKEN = "Token" # در این خط توکن بات خود را وارد کنید
SENDER_ID = "" # در این خط سندر آیدی اکانت خود را وارد کنید

bot = Bot(TOKEN)

@bot.on_new_message(ChatType("group") & FromUser(SENDER_ID) & IsForwarded())
async def l(bot, event):
   await event.forward()
   await event.delete()

@bot.on_new_message(ChatType("group") & FromUser(SENDER_ID))
async def i(bot, event):
   await event.copy()
   await event.delete()

bot.run()
```

---

## روش دوم: با استفاده از پراپرتی‌ها

```python
from maxrubika import Bot
from maxrubika.bot.filters import FromUser

TOKEN = "Token" # در این خط توکن بات خود را وارد کنید
SENDER_ID = "" # در این خط سندر آیدی اکانت خود را وارد کنید

bot = Bot(TOKEN)

@bot.on_new_message(FromUser(SENDER_ID))
async def i(bot, event):
    if event.is_forwarded or event.is_sticker or event.is_poll or event.is_location:
        await event.forward()
        await event.delete()
    else:
        await event.delete()
        await event.copy()

bot.run()
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-examples/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مثال‌ها</a>

</div>