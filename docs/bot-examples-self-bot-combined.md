# ترکیب بات و سلف‌بات - دریافت لینک پست

---

```python
import re
from maxrubika import Bot, Messenger
from maxrubika.bot.filters import Text

bot = Bot("Token") # توکن بات خود را اینجا وارد کنید.
app = Messenger("mySession") # سشن اکانت خود را اینجا وارد کنید.

app.start()

@bot.on_message(Text(re.compile(r'https://rubika\.ir/\w+/[A-Z]+', re.IGNORECASE)))
async def get_post(bot, event):
    link = event.text.strip()

    try:
        result = await app.get_channel_post_by_link(link)
        ask_spam_link = result.ask_spam_link

        if ask_spam_link:
            await event.reply(f"**لینک پست مورد نظر آماده شد:\n\n>**{ask_spam_link}")
        else:
            await event.reply("**خطایی رخ داد.**")

    except Exception as e:
        print(e)
        await event.reply(f"**لطفاً لینک معتبر وارد شود.**")

bot.run()
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-examples/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مثال‌ها</a>

</div>