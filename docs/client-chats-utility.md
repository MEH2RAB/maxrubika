# ابزارهای چت

---

<a id="messenger_send_chat_activity"></a>
## [send_chat_activity](#messenger_send_chat_activity)

این متد برای ارسال وضعیت فعالیت در چت (در حال تایپ، ضبط یا آپلود) است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کاربر.
- **activity:** نوع فعالیت. مقادیر: `Typing`، `Recording`، `Uploading`. (پیش‌فرض: Typing)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.send_chat_activity("u0abc123...", activity="Typing")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_click_keypad_button"></a>
## [click_keypad_button](#messenger_click_keypad_button)

این متد برای کلیک روی دکمه‌های کیپاد یک بات است.

**پارامترها:**

- **chat:** GUID یا نام‌کاربری بات.
- **button_id:** شناسه دکمه.

**نکته:** چت باید یک بات (b0) باشد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.click_keypad_button("@MyBot", button_id="100")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_all_drafts"></a>
## [get_all_drafts](#messenger_get_all_drafts)

این متد برای دریافت تمام پیش‌نویس‌های ذخیره شده پیام‌ها است.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        drafts = app.get_all_drafts()
        print(drafts)

    except Exception as e:
        print(e)
```

---

<a id="messenger_upload_avatar"></a>
## [upload_avatar](#messenger_upload_avatar)

این متد برای آپلود تصویر پروفایل (آواتار) برای یک چت (خود، گروه یا کانال) است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت. همچنین می‌توان از `me` برای پروفایل خود استفاده کرد.
- **main_image:** مسیر فایل یا داده‌های بایتی تصویر اصلی.
- **thumbnail_image:** مسیر فایل یا داده‌های بایتی تصویر بندانگشتی. (پیش‌فرض: None - استفاده از تصویر اصلی)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.upload_avatar(
            "me",
            main_image="/path/to/avatar.jpg"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_avatars"></a>
## [get_avatars](#messenger_get_avatars)

این متد برای دریافت لیست آواتارهای یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت. همچنین می‌توان از `me` برای پروفایل خود استفاده کرد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        avatars = app.get_avatars("g0abc123...")
        print(avatars)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_avatar"></a>
## [delete_avatar](#messenger_delete_avatar)

این متد برای حذف یک آواتار خاص از چت است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **avatar_id:** شناسه آواتار مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_avatar("me", avatar_id="avatar_123")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_all_avatars"></a>
## [delete_all_avatars](#messenger_delete_all_avatars)

این متد برای حذف تمام آواتارهای یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_all_avatars("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_download_profile_picture"></a>
## [download_profile_picture](#messenger_download_profile_picture)

این متد برای دانلود تصویر پروفایل یک کاربر، گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **file_id:** شناسه فایل برای دانلود مستقیم. (پیش‌فرض: None)
- **access_hash_rec:** هش دسترسی فایل. (پیش‌فرض: None)
- **dc_id:** شناسه دیتاسنتر. (پیش‌فرض: None)
- **save_as:** مسیر ذخیره فایل. `True` برای ذخیره در مسیر فعلی، `str` برای مسیر دلخواه، `None` برای بازگرداندن بایت. (پیش‌فرض: None)
- **save_all:** دانلود تمام آواتارها به جای آخرین مورد. (پیش‌فرض: False)

**مثال‌ها:**

۱. دریافت آخرین عکس پروفایل به صورت بایت:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        image_bytes = app.download_profile_picture("@Online_User")
        print(len(image_bytes))

    except Exception as e:
        print(e)
```

۲. ذخیره در مسیر دلخواه:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.download_profile_picture("@Online_User", save_as="/path/to/folder")
        print(result)

    except Exception as e:
        print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-chat/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>