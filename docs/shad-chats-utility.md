# ابزارهای چت

---

<a id="shad_send_chat_activity"></a>
## [send_chat_activity](#shad_send_chat_activity)

این متد برای ارسال وضعیت فعالیت در چت (در حال تایپ، ضبط یا آپلود) است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کاربر.
- **activity:** نوع فعالیت. مقادیر قابل قبول: `Typing`، `Recording`، `Uploading`. (پیش‌فرض: Typing)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_chat_activity("u0abc123...", activity="Typing")
    print(result)
```

---

<a id="shad_click_keypad_button"></a>
## [click_keypad_button](#shad_click_keypad_button)

این متد برای کلیک روی دکمه‌های کیپاد یک بات است.

**پارامترها:**

- **chat:** GUID یا نام‌کاربری بات.
- **button_id:** شناسه دکمه.

**نکته:** چت باید یک بات (`b0`) باشد. متد ابتدا اطلاعات کیپاد بات را دریافت می‌کند و سپس دکمه مورد نظر را پیدا و کلیک می‌کند. اگر دکمه‌ای با آن شناسه وجود نداشته باشد، خطا برمی‌گردد.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.click_keypad_button("@MyBot", button_id="100")
    print(result)
```

---

<a id="shad_get_all_drafts"></a>
## [get_all_drafts](#shad_get_all_drafts)

این متد برای دریافت تمام پیش‌نویس‌های ذخیره شده پیام‌ها است.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    drafts = app.get_all_drafts()
    print(drafts)
```

---

<a id="shad_clear_chat_draft"></a>
## [clear_chat_draft](#shad_clear_chat_draft)

این متد برای پاک کردن پیش‌نویس یک چت خاص است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.clear_chat_draft("u0abc123...")
    print(result)
```

---

<a id="shad_clear_all_drafts"></a>
## [clear_all_drafts](#shad_clear_all_drafts)

این متد برای پاک کردن تمام پیش‌نویس‌ها است.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.clear_all_drafts()
    print(result)
```

---

<a id="shad_seen_chats"></a>
## [seen_chats](#shad_seen_chats)

این متد برای علامت‌گذاری چند چت به عنوان دیده‌شده است.

**پارامتر:**

- **seen_list:** دیکشنری شامل GUID چت‌ها و آخرین شناسه پیام دیده‌شده.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.seen_chats({
        "u0abc123...": "123456",
        "g0xyz789...": "789012"
    })
    print(result)
```

---

<a id="shad_set_chat_use_time"></a>
## [set_chat_use_time](#shad_set_chat_use_time)

این متد برای ارسال زمان استفاده از چت به سرور است. این کار به سرور کمک می‌کند رفتار طبیعی کاربر را تشخیص دهد.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **use_time:** زمان سپری‌شده در چت به **ثانیه**.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.set_chat_use_time("u0abc123...", use_time=60)
    print(result)
```

---

<a id="shad_report_chat"></a>
## [report_chat](#shad_report_chat)

این متد برای گزارش یک چت (کاربر، گروه، کانال) است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **report_type:** نوع گزارش. می‌تواند:
    - عدد بین ۱۰۰ تا ۱۰۶
    - نام رشته‌ای (بدون حساسیت به حروف بزرگ/کوچک): `Other`، `Violence`، `Spam`، `Porn`، `ChildAbuse`، `Copyright`، `Fraud`
- **description:** توضیحات گزارش. **الزامی** وقتی `report_type` برابر ۱۰۰ (Other) باشد. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.report_chat(
        "u0abc123...",
        report_type="Other",
        description="ارسال تصویر حاوی الفاظ نامناسب"
    )
    print(result)
```

---

<a id="shad_click_chat_ads"></a>
## [click_chat_ads](#shad_click_chat_ads)

این متد برای ثبت کلیک روی یک تبلیغ چت است. مقدار `chat_ads_id` از متد `get_chat_ads` به دست می‌آید.

**پارامتر:**

- **chat_ads_id:** شناسه تبلیغ چت.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.click_chat_ads("ads_123")
    print(result)
```

---

<a id="shad_dont_show_chat_ads"></a>
## [dont_show_chat_ads](#shad_dont_show_chat_ads)

این متد برای ثبت درخواست «نمایش نده» روی یک تبلیغ چت است. مقدار `chat_ads_id` از متد `get_chat_ads` به دست می‌آید.

**پارامتر:**

- **chat_ads_id:** شناسه تبلیغ چت.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.dont_show_chat_ads("ads_123")
    print(result)
```

---

<a id="shad_report_chat_ads"></a>
## [report_chat_ads](#shad_report_chat_ads)

این متد برای ثبت گزارش روی یک تبلیغ چت است. مقدار `chat_ads_id` از متد `get_chat_ads` به دست می‌آید.

**پارامتر:**

- **chat_ads_id:** شناسه تبلیغ چت.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.report_chat_ads("ads_123")
    print(result)
```

---

<a id="shad_view_chat_ads"></a>
## [view_chat_ads](#shad_view_chat_ads)

این متد برای ثبت بازدید یک تبلیغ چت است. مقدار `chat_ads_id` از متد `get_chat_ads` به دست می‌آید.

**پارامتر:**

- **chat_ads_id:** شناسه تبلیغ چت.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.view_chat_ads("ads_123")
    print(result)
```

---

<a id="shad_download_profile_picture"></a>
## [download_profile_picture](#shad_download_profile_picture)

این متد برای دانلود تصویر پروفایل یک کاربر، گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **file_id:** شناسه فایل برای دانلود مستقیم. (پیش‌فرض: None)
- **access_hash_rec:** هش دسترسی فایل. (پیش‌فرض: None)
- **dc_id:** شناسه دیتاسنتر. (پیش‌فرض: None)
- **save_as:** مسیر دایرکتوری موجود برای ذخیره فایل. `True` برای ذخیره در مسیر فعلی، `str` برای مسیر دلخواه (باید از قبل وجود داشته باشد)، `None` برای بازگرداندن بایت. (پیش‌فرض: None)
- **save_all:** دانلود تمام آواتارها به جای آخرین مورد. (پیش‌فرض: False)

**نکته:** اگر هیچ عکس پروفایلی وجود نداشته باشد، `bytes()` خالی بازگردانده می‌شود.

**مثال‌ها:**

۱. دریافت آخرین عکس پروفایل به صورت بایت:

```python
from maxrubika import Shad

with Shad("mySession") as app:
    image_bytes = app.download_profile_picture("@Online_User")
    print(len(image_bytes))
```

۲. ذخیره در مسیر دلخواه:

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.download_profile_picture("@Online_User", save_as="/path/to/folder")
    print(result)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../shad-methods-chat/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>