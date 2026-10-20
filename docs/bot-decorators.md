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

فقط پیام‌های حذف شده را دریافت می‌کند.

```python
@bot.on_delete_message()
async def handler(bot, event):
    print(f"پیام {event.deleted_message_id} حذف شد.")
```

---

<a id="bot_on_message"></a>
## [`on_message`](#bot_on_message)

همه نوع پیام (جدید، ویرایش شده، حذف شده، callback) را دریافت می‌کند.

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
```

---

<a id="bot_on_update"></a>
## [`on_update`](#bot_on_update)

همه نوع آپدیت‌ها را دریافت می‌کند.

```python
@bot.on_update()
async def update(bot, event):
    print(event)
```

---

<a id="bot_on_event_data"></a>
## [`on_event_data`](#bot_on_event_data)

رویدادهای مربوط به بات را دریافت می‌کند.

```python
@bot.on_event_data()
async def handler(bot, event):
    print(event)
```

---

<a id="bot_on_bot_joined"></a>
## [`on_bot_joined`](#bot_on_bot_joined)

رویداد مربوط به اضافه شدنِ بات در چت را دریافت می‌کند.

```python
@bot.on_bot_joined()
async def handler(bot, event):
    print(f"بات به چت {event.chat_id} اضافه شد.")
```

---

<a id="bot_on_bot_removed"></a>
## [`on_bot_removed`](#bot_on_bot_removed)

رویداد مربوط به حذف شدنِ بات از چت را دریافت می‌کند.

```python
@bot.on_bot_removed()
async def handler(bot, event):
    print(f"بات از چت {event.chat_id} حذف شد.")
```

---

<a id="bot_on_bot_permissions_changed"></a>
## [`on_bot_permissions_changed`](#bot_on_bot_permissions_changed)

رویداد مربوط به تغییر دسترسی بات در چت را دریافت می‌کند.

```python
@bot.on_bot_permissions_changed()
async def handler(bot, event):
    print(f"دسترسی بات در چت {event.chat_id} تغییر کرد.")
```

---

<a id="bot_on_started_bot"></a>
## [`on_started_bot`](#bot_on_started_bot)

رویداد مربوط به شروع بات را دریافت می‌کند.

```python
@bot.on_started_bot()
async def handler(bot, event):
    print("بات شروع شد.")
```

---

<a id="bot_on_stopped_bot"></a>
## [`on_stopped_bot`](#bot_on_stopped_bot)

رویداد مربوط به توقف بات را دریافت می‌کند.

```python
@bot.on_stopped_bot()
async def handler(bot, event):
    print("بات متوقف شد.")
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

<a href="../bot-methods/" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">→ صفحه قبل</a>

<a href="../bot-guide/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">صفحه اصلی</a>

<a href="../bot-filters/" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">صفحه بعد ←</a>

</div>