# ابزارهای پیام

---

<a id="shad_get_poll_status"></a>
## [get_poll_status](#shad_get_poll_status)

این متد برای دریافت وضعیت یک نظرسنجی به کار می‌رود.

**پارامتر:**

- **poll_id:** شناسه نظرسنجی.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    status = app.get_poll_status("poll_123")
    print(status)
```

---

<a id="shad_get_poll_option_voters"></a>
## [get_poll_option_voters](#shad_get_poll_option_voters)

این متد برای دریافت رأی‌دهندگان یک گزینه خاص از نظرسنجی به کار می‌رود.

**پارامترها:**

- **poll_id:** شناسه نظرسنجی.
- **selection_index:** ایندکس گزینه مورد نظر.
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    voters = app.get_poll_option_voters("poll_123", selection_index=0)
    print(voters)
```

---

<a id="shad_vote_poll"></a>
## [vote_poll](#shad_vote_poll)

این متد برای رأی دادن به یک گزینه نظرسنجی به کار می‌رود.

**پارامترها:**

- **poll_id:** شناسه نظرسنجی.
- **selection_index:** ایندکس گزینه مورد نظر.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.vote_poll("poll_123", selection_index=0)
    print(result)
```

---

<a id="shad_stop_poll"></a>
## [stop_poll](#shad_stop_poll)

این متد برای متوقف کردن یک نظرسنجی به کار می‌رود.

**پارامتر:**

- **poll_id:** شناسه نظرسنجی.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.stop_poll("poll_123")
    print(result)
```

---

<a id="shad_retract_poll"></a>
## [retract_poll](#shad_retract_poll)

این متد برای بازپس‌گیری رای در یک نظرسنجی به کار می‌رود.

**پارامتر:**

- **poll_id:** شناسه نظرسنجی.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.retract_poll("poll_123")
    print(result)
```

---

<a id="shad_request_send_file"></a>
## [request_send_file](#shad_request_send_file)

این متد برای درخواست ارسال یک فایل (دریافت URL آپلود) به کار می‌رود. این اولین گام در فرایند آپلود فایل است.

**پارامترها:**

- **file_name:** نام فایل.
- **size:** اندازه فایل (به بایت).
- **mime:** نوع MIME فایل. (پیش‌فرض: None - تشخیص از روی پسوند فایل)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.request_send_file(
        file_name="document.pdf",
        size=1024000
    )
    print(result)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../shad-methods-messages/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>