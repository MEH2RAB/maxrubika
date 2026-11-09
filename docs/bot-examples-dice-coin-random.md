# تاس، سکه و عدد تصادفی

---

```python
from maxrubika import Bot
from maxrubika.bot.filters import Text
import random

bot = Bot("Token") # در این خط توکن بات خود را وارد کنید

@bot.on_new_message(Text("^تاس"))
async def roll_dice(bot, event):
    dice = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    result = random.choice(dice)
    await event.reply(result)

@bot.on_new_message(Text("^سکه"))
async def coin(bot, event):
    result = random.choice(["🪙 شیر", "🪙 خط"])
    await event.reply(result)

@bot.on_new_message(Text("^عدد"))
async def random_number(bot, event):
    num = random.randint(1, 100)
    await event.reply(f"🔢 {num}")

bot.run()
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-examples/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مثال‌ها</a>

</div>