# ابزارهای پیام

---

<a id="messenger_transcribe_voice"></a>
## [transcribe_voice](#messenger_transcribe_voice)

این متد برای تبدیل صوت به متن (پیاده‌سازی متن پیام صوتی) به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام صوتی.

**نکته:** این متد ابتدا درخواست تبدیل را ارسال کرده، سپس نتیجه نهایی را دریافت و بازمی‌گرداند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        text = app.transcribe_voice("u0abc123...", message_id="123456")
        print(text)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_poll_status"></a>
## [get_poll_status](#messenger_get_poll_status)

این متد برای دریافت وضعیت یک نظرسنجی به کار می‌رود.

**پارامتر:**

- **poll_id:** شناسه نظرسنجی.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        status = app.get_poll_status("poll_123")
        print(status)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_poll_option_voters"></a>
## [get_poll_option_voters](#messenger_get_poll_option_voters)

این متد برای دریافت رأی‌دهندگان یک گزینه خاص از نظرسنجی به کار می‌رود.

**پارامترها:**

- **poll_id:** شناسه نظرسنجی.
- **selection_index:** ایندکس گزینه مورد نظر.
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        voters = app.get_poll_option_voters("poll_123", selection_index=0)
        print(voters)

    except Exception as e:
        print(e)
```

---

<a id="messenger_vote_poll"></a>
## [vote_poll](#messenger_vote_poll)

این متد برای رأی دادن به یک گزینه نظرسنجی به کار می‌رود.

**پارامترها:**

- **poll_id:** شناسه نظرسنجی.
- **selection_index:** ایندکس گزینه مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.vote_poll("poll_123", selection_index=0)
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_stop_poll"></a>
## [stop_poll](#messenger_stop_poll)

این متد برای متوقف کردن یک نظرسنجی به کار می‌رود.

**پارامتر:**

- **poll_id:** شناسه نظرسنجی.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.stop_poll("poll_123")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_retract_poll"></a>
## [retract_poll](#messenger_retract_poll)

این متد برای بازپس‌گیری (حذف) یک نظرسنجی به کار می‌رود.

**پارامتر:**

- **poll_id:** شناسه نظرسنجی.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.retract_poll("poll_123")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_request_send_file"></a>
## [request_send_file](#messenger_request_send_file)

این متد برای درخواست ارسال یک فایل (دریافت URL آپلود) به کار می‌رود. این اولین گام در فرایند آپلود فایل است.

**پارامترها:**

- **file_name:** نام فایل.
- **size:** اندازه فایل (به بایت).
- **mime:** نوع MIME فایل. (پیش‌فرض: None - تشخیص از روی پسوند فایل)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.request_send_file(
            file_name="document.pdf",
            size=1024000
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-messages/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>