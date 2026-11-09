# دریافت پیام ساده

---

```python
from maxrubika import Bot

bot = Bot("Token") # در این خط توکن بات خود را وارد کنید

@bot.on_command("start")
async def start(bot, event):
    await event.reply("سلام، پیام شما دریافت شد.")

bot.run()
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-examples/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مثال‌ها</a>

</div>