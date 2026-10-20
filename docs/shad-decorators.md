# دکوراتورها

---

<a id="shad_on_new_message"></a>
## [`@app.on_new_message(*filters)`](#shad_on_new_message)

فقط پیام‌های جدید را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_new_message()
async def handler(event):
    print(f"پیام جدید: {event.text}")

app.run()
```

---

<a id="shad_on_edit_message"></a>
## [`@app.on_edit_message(*filters)`](#shad_on_edit_message)

فقط پیام‌های ویرایش شده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_edit_message()
async def handler(event):
    print(f"پیام ویرایش شد: {event.text}")

app.run()
```

---

<a id="shad_on_delete_message"></a>
## [`@app.on_delete_message(*filters)`](#shad_on_delete_message)

فقط پیام‌های حذف شده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_delete_message()
async def handler(event):
    print(f"پیام حذف شد: {event.message_id}")

app.run()
```

---

<a id="shad_on_draft_message"></a>
## [`@app.on_draft_message(*filters)`](#shad_on_draft_message)

فقط پیام‌های بایگانی شده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_draft_message()
async def handler(event):
    print(f"پیش‌نویس پیام")

app.run()
```

---

<a id="shad_on_scheduled_message"></a>
## [`@app.on_scheduled_message(*filters)`](#shad_on_scheduled_message)

فقط پیام‌های زمان‌بندی شده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_scheduled_message()
async def handler(event):
    print(f"پیام زمان‌بندی شده")

app.run()
```

---

<a id="shad_on_message"></a>
## [`@app.on_message(*filters)`](#shad_on_message)

همه نوع پیام (جدید، ویرایش شده، حذف شده) را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_message()
async def handler(event):
    print(f"پیام: {event.text}")

app.run()
```

---

<a id="shad_on_add_reaction"></a>
## [`@app.on_add_reaction(*filters)`](#shad_on_add_reaction)

فقط آپدیت مربوط به اضافه شدن ری‌اکشن به پیام را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_add_reaction()
async def handler(event):
    print(f"ری‌اکشن اضافه شد: {event.reactions}")

app.run()
```

---

<a id="shad_on_remove_reaction"></a>
## [`@app.on_remove_reaction(*filters)`](#shad_on_remove_reaction)

فقط آپدیت مربوط به حذف شدن ری‌اکشن از پیام را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_remove_reaction()
async def handler(event):
    print(f"ری‌اکشن حذف شد")

app.run()
```

---

<a id="shad_on_chat_updates"></a>
## [`@app.on_chat_updates(*filters)`](#shad_on_chat_updates)

فقط آپدیت‌های چت را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_chat_updates()
async def handler(event):
    print(f"بروزرسانی چت")

app.run()
```

---

<a id="shad_on_call_signal"></a>
## [`@app.on_call_signal(*filters)`](#shad_on_call_signal)

فقط سیگنال مربوط به تماس صوتی و تصویری را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_call_signal()
async def handler(event):
    print(f"سیگنال تماس")

app.run()
```

---

<a id="shad_on_call_update"></a>
## [`@app.on_call_update(*filters)`](#shad_on_call_update)

فقط آپدیت مربوط به تماس صوتی و تصویری را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_call_update()
async def handler(event):
    print(f"بروزرسانی تماس")

app.run()
```

---

<a id="shad_on_unconfirmed_session"></a>
## [`@app.on_unconfirmed_session()`](#shad_on_unconfirmed_session)

فقط نشست‌های تایید نشده را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_unconfirmed_session()
async def handler(event):
    print(f"نشست تأیید نشده")

app.run()
```

---

<a id="shad_on_show_activities"></a>
## [`@app.on_show_activities(*filters)`](#shad_on_show_activities)

فقط اکشن‌های کاربران را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_show_activities()
async def handler(event):
    print(f"فعالیت: {event.activity}")

app.run()
```

---

<a id="shad_on_show_notifications"></a>
## [`@app.on_show_notifications(*filters)`](#shad_on_show_notifications)

فقط اعلانات را نمایش می‌دهد.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_show_notifications()
async def handler(event):
    print(f"اعلان جدید")

app.run()
```

---

<a id="shad_on_remove_notifications"></a>
## [`@app.on_remove_notifications(*filters)`](#shad_on_remove_notifications)

فقط اعلانات را حذف می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_remove_notifications()
async def handler(event):
    print(f"اعلان حذف شد")

app.run()
```

---

<a id="shad_on_voice_chat_participant"></a>
## [`@app.on_voice_chat_participant(*filters)`](#shad_on_voice_chat_participant)

فقط آپدیت مربوط به شرکت‌کنندگان در گفتگوی صوتی را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_voice_chat_participant()
async def handler(event):
    print(f"تغییر شرکت‌کننده ویس چت")

app.run()
```

---

<a id="shad_on_voice_chat_update"></a>
## [`@app.on_voice_chat_update(*filters)`](#shad_on_voice_chat_update)

فقط آپدیت مربوط به گفتگوی صوتی را دریافت می‌کند.

**مثال:**

```python
from maxrubika import Shad

app = Shad("mySession")

@app.on_voice_chat_update()
async def handler(event):
    print(f"بروزرسانی ویس چت")

app.run()
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">

<a href="../shad-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>