# ویس چت

---

<a id="messenger_get_chat_voice_chat"></a>
## [get_chat_voice_chat](#messenger_get_chat_voice_chat)

این متد برای دریافت اطلاعات ویس چت فعال یک گروه یا کانال است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        voice = app.get_chat_voice_chat("g0abc123...")
        print(voice)

    except Exception as e:
        print(e)
```

---

<a id="messenger_start_voice_chat"></a>
## [start_voice_chat](#messenger_start_voice_chat)

این متد برای شروع یک ویس چت در گروه یا کانال است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.start_voice_chat("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_join_voice_chat"></a>
## [join_voice_chat](#messenger_join_voice_chat)

این متد برای پیوستن به ویس چت فعال یک گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **sdp_offer_data:** داده‌های SDP offer. (پیش‌فرض: None - استفاده از پیش‌فرض)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.join_voice_chat("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_leave_voice_chat"></a>
## [leave_voice_chat](#messenger_leave_voice_chat)

این متد برای خروج از ویس چت فعال یک گروه یا کانال است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.leave_voice_chat("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_play_voice_chat"></a>
## [play_voice_chat](#messenger_play_voice_chat)

این متد برای پخش فایل صوتی در ویس چت است. نیاز به نصب کتابخانه `aiortc` دارد.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **media:** مسیر فایل صوتی برای پخش.

**نکته:** نصب پیش‌نیاز: `pip install aiortc`

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        connection = app.play_voice_chat("g0abc123...", media="/path/to/audio.mp3")
        # برای توقف: connection.stop()
        # برای توقف موقت: connection.pause()
        # برای ادامه: connection.resume()

    except Exception as e:
        print(e)
```

---

<a id="messenger_discard_voice_chat"></a>
## [discard_voice_chat](#messenger_discard_voice_chat)

این متد برای پایان دادن به ویس چت فعال یک گروه یا کانال است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.discard_voice_chat("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_voice_chat_participants"></a>
## [get_voice_chat_participants](#messenger_get_voice_chat_participants)

این متد برای دریافت لیست شرکت‌کنندگان ویس چت فعال است. به صورت خودکار تمام صفحات را پیمایش می‌کند.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **show_user_guids:** نمایش GUID کاربران در خروجی. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        participants = app.get_voice_chat_participants("g0abc123...")
        print(participants)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_voice_chat_updates"></a>
## [get_voice_chat_updates](#messenger_get_voice_chat_updates)

این متد برای دریافت به‌روزرسانی‌های ویس چت است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **state:** وضعیت زمانی برای دریافت به‌روزرسانی‌ها. (پیش‌فرض: ۱۵۰ ثانیه قبل از زمان فعلی)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        updates = app.get_voice_chat_updates("g0abc123...")
        print(updates)

    except Exception as e:
        print(e)
```

---

<a id="messenger_send_voice_chat_activity"></a>
## [send_voice_chat_activity](#messenger_send_voice_chat_activity)

این متد برای ارسال فعالیت در ویس چت (مانند در حال صحبت بودن) است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **activity:** نوع فعالیت. (فقط `Speaking`، پیش‌فرض: Speaking)
- **participant_chat_guid:** GUID شرکت‌کننده. (پیش‌فرض: خود کاربر)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.send_voice_chat_activity("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_set_voice_chat_setting"></a>
## [set_voice_chat_setting](#messenger_set_voice_chat_setting)

این متد برای تنظیمات ویس چت (عنوان و وضعیت بی‌صدای اعضای جدید) است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **title:** عنوان جدید ویس چت. (پیش‌فرض: None)
- **join_muted:** آیا اعضای جدید بی‌صدا وارد شوند؟ (فقط گروه، پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_voice_chat_setting(
            "g0abc123...",
            title="ویس چت عمومی",
            join_muted=True
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_set_voice_chat_state"></a>
## [set_voice_chat_state](#messenger_set_voice_chat_state)

این متد برای تنظیم وضعیت ویس چت (Mute/Unmute) است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **action:** عملیات. مقادیر: `Mute`، `Unmute`. (پیش‌فرض: Unmute)
- **participant_chat_guid:** GUID شرکت‌کننده. (پیش‌فرض: خود کاربر)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_voice_chat_state("g0abc123...", action="Mute")
        print(result)

    except Exception as e:
        print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-chat/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>