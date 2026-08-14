# دکوراتورها

---

<a id="messenger_on_message"></a>
## [`@app.on_message(*filters)`](#messenger_on_message)

دریافت تمام رویدادهای پیام (جدید، ویرایش، حذف، ری‌اکشن). این دکوراتور جامع‌ترین است و تمام انواع پیام را پوشش می‌دهد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_message()
    async def handler(event):
        print(f"پیام: {event.text}")

    app.run()
```

---

<a id="messenger_on_new_message"></a>
## [`@app.on_new_message(*filters)`](#messenger_on_new_message)

فقط پیام‌های جدید را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_new_message()
    async def handler(event):
        print(f"پیام جدید: {event.text}")

    app.run()
```

---

<a id="messenger_on_edit_message"></a>
## [`@app.on_edit_message(*filters)`](#messenger_on_edit_message)

فقط پیام‌های ویرایش شده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_edit_message()
    async def handler(event):
        print(f"پیام ویرایش شد: {event.text}")

    app.run()
```

---

<a id="messenger_on_delete_message"></a>
## [`@app.on_delete_message(*filters)`](#messenger_on_delete_message)

فقط پیام‌های حذف شده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_delete_message()
    async def handler(event):
        print(f"پیام حذف شد: {event.message_id}")

    app.run()
```

---

<a id="messenger_on_add_reaction"></a>
## [`@app.on_add_reaction(*filters)`](#messenger_on_add_reaction)

فقط افزودن ری‌اکشن به پیام‌ها را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_add_reaction()
    async def handler(event):
        print(f"ری‌اکشن اضافه شد: {event.reactions}")

    app.run()
```

---

<a id="messenger_on_remove_reaction"></a>
## [`@app.on_remove_reaction(*filters)`](#messenger_on_remove_reaction)

فقط حذف ری‌اکشن از پیام‌ها را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_remove_reaction()
    async def handler(event):
        print(f"ری‌اکشن حذف شد")

    app.run()
```

---

<a id="messenger_on_chat_updates"></a>
## [`@app.on_chat_updates(*filters)`](#messenger_on_chat_updates)

دریافت به‌روزرسانی‌های چت (تغییرات در گروه‌ها، کانال‌ها و...).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_chat_updates()
    async def handler(event):
        print(f"بروزرسانی چت")

    app.run()
```

---

<a id="messenger_on_show_activities"></a>
## [`@app.on_show_activities(*filters)`](#messenger_on_show_activities)

دریافت فعالیت‌های در حال انجام (تایپ کردن، آپلود، ضبط صدا).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_show_activities()
    async def handler(event):
        print(f"فعالیت: {event.activity}")

    app.run()
```

---

<a id="messenger_on_show_notifications"></a>
## [`@app.on_show_notifications(*filters)`](#messenger_on_show_notifications)

دریافت اعلان‌های نمایش داده شده.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_show_notifications()
    async def handler(event):
        print(f"اعلان جدید")

    app.run()
```

---

<a id="messenger_on_remove_notifications"></a>
## [`@app.on_remove_notifications()`](#messenger_on_remove_notifications)

دریافت حذف اعلان‌ها.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_remove_notifications()
    async def handler(event):
        print(f"اعلان حذف شد")

    app.run()
```

---

<a id="messenger_on_voice_chat_update"></a>
## [`@app.on_voice_chat_update(*filters)`](#messenger_on_voice_chat_update)

دریافت به‌روزرسانی‌های ویس چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_voice_chat_update()
    async def handler(event):
        print(f"بروزرسانی ویس چت")

    app.run()
```

---

<a id="messenger_on_voice_chat_participant"></a>
## [`@app.on_voice_chat_participant(*filters)`](#messenger_on_voice_chat_participant)

دریافت تغییرات شرکت‌کنندگان ویس چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_voice_chat_participant()
    async def handler(event):
        print(f"تغییر شرکت‌کننده ویس چت")

    app.run()
```

---

<a id="messenger_on_call_update"></a>
## [`@app.on_call_update(*filters)`](#messenger_on_call_update)

دریافت به‌روزرسانی‌های تماس صوتی/تصویری.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_call_update()
    async def handler(event):
        print(f"بروزرسانی تماس")

    app.run()
```

---

<a id="messenger_on_call_signal"></a>
## [`@app.on_call_signal(*filters)`](#messenger_on_call_signal)

دریافت سیگنال‌های تماس (داده‌های فنی ارتباط).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_call_signal()
    async def handler(event):
        print(f"سیگنال تماس")

    app.run()
```

---

<a id="messenger_on_scheduled_message"></a>
## [`@app.on_scheduled_message(*filters)`](#messenger_on_scheduled_message)

دریافت به‌روزرسانی‌های پیام‌های زمان‌بندی شده.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_scheduled_message()
    async def handler(event):
        print(f"پیام زمان‌بندی شده")

    app.run()
```

---

<a id="messenger_on_draft_message"></a>
## [`@app.on_draft_message(*filters)`](#messenger_on_draft_message)

دریافت به‌روزرسانی‌های پیش‌نویس پیام‌ها.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_draft_message()
    async def handler(event):
        print(f"پیش‌نویس پیام")

    app.run()
```

---

<a id="messenger_on_unconfirmed_session"></a>
## [`@app.on_unconfirmed_session(*filters)`](#messenger_on_unconfirmed_session)

دریافت نشست‌های تأیید نشده (ضد ورود غیرمجاز).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    @app.on_unconfirmed_session()
    async def handler(event):
        print(f"نشست تأیید نشده")

    app.run()
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">

<a href="../client-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>