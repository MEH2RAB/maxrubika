# دکوراتورها

---

<a id="client_on_message"></a>
## [`@client.on_message(*filters)`](#client_on_message)

دریافت تمام رویدادهای پیام (جدید، ویرایش، حذف، ری‌اکشن). این دکوراتور جامع‌ترین است و تمام انواع پیام را پوشش می‌دهد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_message()
async def handler(event):
    print(f"پیام: {event.text}")

client.run()
```

---

<a id="client_on_new_message"></a>
## [`@client.on_new_message(*filters)`](#client_on_new_message)

فقط پیام‌های جدید را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_new_message()
async def handler(event):
    print(f"پیام جدید: {event.text}")

client.run()
```

---

<a id="client_on_edit_message"></a>
## [`@client.on_edit_message(*filters)`](#client_on_edit_message)

فقط پیام‌های ویرایش شده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_edit_message()
async def handler(event):
    print(f"پیام ویرایش شد: {event.text}")

client.run()
```

---

<a id="client_on_delete_message"></a>
## [`@client.on_delete_message(*filters)`](#client_on_delete_message)

فقط پیام‌های حذف شده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_delete_message()
async def handler(event):
    print(f"پیام حذف شد: {event.message_id}")

client.run()
```

---

<a id="client_on_add_reaction"></a>
## [`@client.on_add_reaction(*filters)`](#client_on_add_reaction)

فقط افزودن ری‌اکشن به پیام‌ها را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_add_reaction()
async def handler(event):
    print(f"ری‌اکشن اضافه شد: {event.reactions}")

client.run()
```

---

<a id="client_on_remove_reaction"></a>
## [`@client.on_remove_reaction(*filters)`](#client_on_remove_reaction)

فقط حذف ری‌اکشن از پیام‌ها را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_remove_reaction()
async def handler(event):
    print(f"ری‌اکشن حذف شد")

client.run()
```

---

<a id="client_on_chat_updates"></a>
## [`@client.on_chat_updates(*filters)`](#client_on_chat_updates)

دریافت به‌روزرسانی‌های چت (تغییرات در گروه‌ها، کانال‌ها و...).

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_chat_updates()
async def handler(event):
    print(f"بروزرسانی چت")

client.run()
```

---

<a id="client_on_show_activities"></a>
## [`@client.on_show_activities(*filters)`](#client_on_show_activities)

دریافت فعالیت‌های در حال انجام (تایپ کردن، آپلود، ضبط صدا).

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_show_activities()
async def handler(event):
    print(f"فعالیت: {event.activity}")

client.run()
```

---

<a id="client_on_show_notifications"></a>
## [`@client.on_show_notifications(*filters)`](#client_on_show_notifications)

دریافت اعلان‌های نمایش داده شده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_show_notifications()
async def handler(event):
    print(f"اعلان جدید")

client.run()
```

---

<a id="client_on_remove_notifications"></a>
## [`@client.on_remove_notifications()`](#client_on_remove_notifications)

دریافت حذف اعلان‌ها.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_remove_notifications()
async def handler(event):
    print(f"اعلان حذف شد")

client.run()
```

---

<a id="client_on_voice_chat_update"></a>
## [`@client.on_voice_chat_update(*filters)`](#client_on_voice_chat_update)

دریافت به‌روزرسانی‌های ویس چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_voice_chat_update()
async def handler(event):
    print(f"بروزرسانی ویس چت")

client.run()
```

---

<a id="client_on_voice_chat_participant"></a>
## [`@client.on_voice_chat_participant(*filters)`](#client_on_voice_chat_participant)

دریافت تغییرات شرکت‌کنندگان ویس چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_voice_chat_participant()
async def handler(event):
    print(f"تغییر شرکت‌کننده ویس چت")

client.run()
```

---

<a id="client_on_call_update"></a>
## [`@client.on_call_update(*filters)`](#client_on_call_update)

دریافت به‌روزرسانی‌های تماس صوتی/تصویری.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_call_update()
async def handler(event):
    print(f"بروزرسانی تماس")

client.run()
```

---

<a id="client_on_call_signal"></a>
## [`@client.on_call_signal(*filters)`](#client_on_call_signal)

دریافت سیگنال‌های تماس (داده‌های فنی ارتباط).

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_call_signal()
async def handler(event):
    print(f"سیگنال تماس")

client.run()
```

---

<a id="client_on_scheduled_message"></a>
## [`@client.on_scheduled_message(*filters)`](#client_on_scheduled_message)

دریافت به‌روزرسانی‌های پیام‌های زمان‌بندی شده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_scheduled_message()
async def handler(event):
    print(f"پیام زمان‌بندی شده")

client.run()
```

---

<a id="client_on_draft_message"></a>
## [`@client.on_draft_message(*filters)`](#client_on_draft_message)

دریافت به‌روزرسانی‌های پیش‌نویس پیام‌ها.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_draft_message()
async def handler(event):
    print(f"پیش‌نویس پیام")

client.run()
```

---

<a id="client_on_unconfirmed_session"></a>
## [`@client.on_unconfirmed_session(*filters)`](#client_on_unconfirmed_session)

دریافت نشست‌های تأیید نشده (ضد ورود غیرمجاز).

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

@client.on_unconfirmed_session()
async def handler(event):
    print(f"نشست تأیید نشده")

client.run()
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">

<a href="/client-messenger" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>