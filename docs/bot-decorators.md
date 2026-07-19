# دکوراتورها

---

<a id="bot_on_new_message"></a>
## [`on_new_message`](#bot_on_new_message)

فقط پیام‌های جدید را دریافت می‌کند.

```python
@bot.on_new_message()
async def handler(bot, event):
    await event.reply("پیام جدید دریافت شد!")
```

---

<a id="bot_on_edit_message"></a>
## [`on_edit_message`](#bot_on_edit_message)

فقط پیام‌های ویرایش شده را دریافت می‌کند.

```python
@bot.on_edit_message()
async def handler(bot, event):
    await event.reply("پیام ویرایش شد!")
```

---

<a id="bot_on_delete_message"></a>
## [`on_delete_message`](#bot_on_delete_message)

فقط پیام‌های پاک شده را دریافت می‌کند.

```python
@bot.on_delete_message()
async def handler(bot, event):
    print(f"پیام {event.deleted_message_id} پاک شد")
```

---

<a id="bot_on_message"></a>
## [`on_message`](#bot_on_message)

همه نوع پیام (جدید، ویرایش، پاک، callback، شروع بات، توقف بات) را دریافت می‌کند.

```python
@bot.on_message()
async def handler(bot, event):
    print(f"رویداد: {event.update_type}")
```

---

<a id="bot_on_callback"></a>
## [`on_callback`](#bot_on_callback)

فقط کلیک روی دکمه‌های اینلاین (شیشه‌ای) را دریافت می‌کند.

```python
@bot.on_callback()
async def handler(bot, event):
    await event.reply(f"دکمه {event.text} کلیک شد!")
```

---

<a id="bot_on_command"></a>
## [`on_command`](#bot_on_command)

میانبر برای دریافت دستورات. معادل `@bot.on_new_message(Command("name"))`.

```python
@bot.on_command("start")
async def start(bot, event):
    await event.reply("شروع!")

@bot.on_command(["start", "شروع"], ChatType("user"))
async def start_user(bot, event):
    await event.reply("شروع فقط در پیوی!")
```

---

<a id="bot_middleware"></a>
## [`middleware`](#bot_middleware)

لایه میانی - قبل و بعد از همه هندلرها اجرا می‌شود. باید `await call_next()` صدا زده شود.

```python
@bot.middleware()
async def logger(bot, event, call_next):
    print(f"[{event.update_type}] {event.chat_id}: {event.text}")
    await call_next()
```

---

<a id="bot_on_start"></a>
## [`on_start`](#bot_on_start)

هنگام شروع بات اجرا می‌شود.

```python
@bot.on_start()
async def startup(bot):
    print("بات روشن شد!")
```

---

<a id="bot_on_shutdown"></a>
## [`on_shutdown`](#bot_on_shutdown)

هنگام خاموشی بات اجرا می‌شود.

```python
@bot.on_shutdown()
async def shutdown(bot):
    print("بات خاموش شد!")
```

---

<div style="display: flex; justify-content: center; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="bot-methods" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">→ صفحه قبل</a>

<a href="bot-guide" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">صفحه اصلی</a>

<a href="bot-filters" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">صفحه بعد ←</a>

</div>