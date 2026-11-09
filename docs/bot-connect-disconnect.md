# نحوه اتصال و قطع اتصال

---

برای برقراری و قطع اتصال در کتابخانه MAXRubika، دو روش اصلی وجود دارد که بسته به نوع استفاده (Sync یا Async) و نیاز پروژه، می‌توانید یکی را انتخاب کنید.

---

## روش اول: استفاده از Context Manager

در این روش نیازی به صدا زدن متد اضافه‌ای برای قطع اتصال نیست؛ کافی است از `with` (در حالت Sync) یا `async with` (در حالت Async) استفاده کنید. اتصال به‌صورت خودکار برقرار می‌شود و در پایان بلوک، به‌درستی بسته خواهد شد.

### حالت Sync

```python
from maxrubika import Bot

with Bot("Token") as bot:
    me = bot.get_me()
    print(me)
```

همچنین می‌توانید ابتدا شیء را بسازید و سپس از `with` استفاده کنید:

```python
from maxrubika import Bot

bot = Bot("Token")

with bot:
    me = bot.get_me()
    print(me)
```

### حالت Async

```python
import asyncio
from maxrubika import Bot

async def main():
    async with Bot("Token") as bot:
        me = await bot.get_me()
        print(me)

asyncio.run(main())
```

یا ساخت جداگانه‌ی شیء و سپس استفاده از `async with`:

```python
import asyncio
from maxrubika import Bot

async def main():
    bot = Bot("Token")

    async with bot:
        me = await bot.get_me()
        print(me)

asyncio.run(main())
```

---

## روش دوم: صدا زدن متد disconnect یا close

در این روش، خودتان به‌صورت دستی اتصال را برقرار می‌کنید و در انتهای عملیات، با صدا زدن متد مناسب، اتصال را می‌بندید.

### حالت Sync

در کدهای Sync از متد `disconnect` استفاده کنید:

```python
from maxrubika import Bot

bot = Bot("Token")

me = bot.get_me()
print(me)

bot.disconnect()  # قطع اتصال در پایان عملیات
```

### حالت Async

در کدهای Async از متد `close` استفاده کنید:

```python
import asyncio
from maxrubika import Bot

async def main():
    bot = Bot("Token")
    me = await bot.get_me()
    print(me)
    await bot.close()  # قطع اتصال در پایان عملیات

asyncio.run(main())
```

---

## نکته مهم

استفاده از این روش‌ها فقط زمانی لازم است که بخواهید یک عملیات موقت با کتابخانه انجام دهید (مثلاً دریافت اطلاعات یک‌باره‌ی یک شیء).

اگر از دکوراتورها، لانگ‌پولینگ یا وب‌هوک استفاده می‌کنید، نیازی به صدا زدن `disconnect` یا `close` یا استفاده از Context Manager نیست؛ زیرا کتابخانه خودش مدیریت اتصال را در طول اجرا به عهده دارد.

### مثال: استفاده از دکوراتور (بدون نیاز به قطع دستی)

```python
from maxrubika import Bot

bot = Bot("Token")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("سلام، پیام شما دریافت شد.")

bot.run()
```

در این حالت، کتابخانه به‌طور خودکار اتصال را در طول اجرای ربات مدیریت می‌کند و نیازی به فراخوانی متدهای `disconnect` یا `close` نخواهد بود.

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-more/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به توضیحات بیشتر</a>

</div>