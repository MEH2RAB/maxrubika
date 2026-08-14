# عملیات روی پیام‌ها

---

<a id="messenger_edit_message"></a>
## [edit_message](#messenger_edit_message)

این متد برای ویرایش متن یک پیام ارسال‌شده به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام مورد نظر.
- **text:** متن جدید جایگزین.
- **metadata:** متادیتای قالب‌بندی متن (Bold، Italic و...). (پیش‌فرض: None - تشخیص خودکار)

**نکته:** در صورت عدم ارسال metadata، کتابخانه به صورت خودکار متادیتا را از متن استخراج می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.edit_message(
            "@Online_User",
            message_id="12345678090",
            text="متن ویرایش شده جدید"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_messages"></a>
## [delete_messages](#messenger_delete_messages)

این متد برای حذف یک یا چند پیام از یک چت به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_ids:** یک شناسه یا لیستی از شناسه‌های پیام برای حذف.
- **type:** نوع حذف. `Global` (حذف برای همه)، `Local` (حذف فقط برای خود)، `Scheduled` (حذف پیام زمان‌بندی شده). (پیش‌فرض: Global)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_messages(
            "https://rubika.ir/joing/ABC123",
            message_ids=["123", "456", "789"]
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_all_messages"></a>
## [delete_all_messages](#messenger_delete_all_messages)

این متد برای حذف تمام پیام‌های یک چت (به جز پیام ایجاد گروه/کانال) به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **exclude_message_ids:** شناسه پیام‌هایی که نباید حذف شوند. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_all_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_my_messages"></a>
## [delete_my_messages](#messenger_delete_my_messages)

این متد برای حذف تمام پیام‌های خودتان در یک چت به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **exclude_message_ids:** شناسه پیام‌هایی که نباید حذف شوند. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_my_messages("@MyGroup")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_auto_delete_message"></a>
## [auto_delete_message](#messenger_auto_delete_message)

این متد برای حذف خودکار یک پیام پس از مدت زمان مشخص به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **time:** مدت زمان تأخیر تا حذف (به ثانیه).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.auto_delete_message(
            "u0abc123...",
            message_id="12345674103",
            time=60
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_forward_messages"></a>
## [forward_messages](#messenger_forward_messages)

این متد برای فوروارد (هدایت) یک یا چند پیام از یک چت به چت دیگر به کار می‌رود.

**پارامترها:**

- **from_chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مبدأ.
- **message_ids:** شناسه پیام‌ها برای فوروارد.
- **to_chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **hide_author:** مخفی کردن فرستنده اصلی. (پیش‌فرض: False)
- **is_mute:** فوروارد بی‌صدا بدون اعلان. (پیش‌فرض: False)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.forward_messages(
            from_chat="@SourceUser",
            message_ids=["123", "456"],
            to_chat="https://rubika.ir/joing/DEST123"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_pin_message"></a>
## [pin_message](#messenger_pin_message)

این متد برای سنجاق کردن (پین) یک پیام در چت به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.pin_message("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", message_id=147503987410)
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_unpin_message"></a>
## [unpin_message](#messenger_unpin_message)

این متد برای برداشتن سنجاق (آنپین) یک پیام در چت به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unpin_message("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", message_id=12345636971)
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_unpin_all_messages"></a>
## [unpin_all_messages](#messenger_unpin_all_messages)

این متد برای برداشتن سنجاق تمام پیام‌های پین شده در یک چت به کار می‌رود.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unpin_all_messages("@MyChannel")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_pinned_messages"></a>
## [get_pinned_messages](#messenger_get_pinned_messages)

این متد برای دریافت تمام پیام‌های سنجاق شده یک چت به کار می‌رود.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        pinned = app.get_pinned_messages("https://rubika.ir/joinc/CH123")
        print(pinned)

    except Exception as e:
        print(e)
```

---

<a id="messenger_add_reaction"></a>
## [add_reaction](#messenger_add_reaction)

این متد برای افزودن ری‌اکشن به یک پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **reaction_id:** شناسه ری‌اکشن.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.add_reaction(
            "@Online_User",
            message_id="123456",
            reaction_id=1
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_remove_reaction"></a>
## [remove_reaction](#messenger_remove_reaction)

این متد برای حذف ری‌اکشن از یک پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **reaction_id:** شناسه ری‌اکشن.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.remove_reaction(
            "https://rubika.ir/joing/GROUP123",
            message_id="123456",
            reaction_id=1
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_messages_reactions"></a>
## [get_messages_reactions](#messenger_get_messages_reactions)

این متد برای دریافت ری‌اکشن‌های پیام‌ها در یک بازه مشخص به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **min_id:** حداقل شناسه پیام (کران پایین).
- **max_id:** حداکثر شناسه پیام (کران بالا).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        reactions = app.get_messages_reactions(
            "u0abc123...",
            min_id="100",
            max_id="200"
        )
        print(reactions)

    except Exception as e:
        print(e)
```

---

<a id="messenger_report_message"></a>
## [report_message](#messenger_report_message)

این متد برای گزارش یک پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **report_type:** نوع گزارش.
- **description:** توضیحات اضافی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.report_message(
            "@Spammer",
            message_id="123456",
            report_type="Spam",
            description="پیام اسپم"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_mark_as_read"></a>
## [mark_as_read](#messenger_mark_as_read)

این متد برای علامت‌گذاری یک چت به عنوان خوانده‌شده (با دیدن آخرین پیام) به کار می‌رود.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.mark_as_read("u0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_mark_as_seen"></a>
## [mark_as_seen](#messenger_mark_as_seen)

این متد برای علامت‌گذاری یک پیام خاص به عنوان دیده‌شده به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام. (پیش‌فرض: None - آخرین پیام)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.mark_as_seen("@MyFriend", message_id="123456")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_click_message_url"></a>
## [click_message_url](#messenger_click_message_url)

این متد برای شبیه‌سازی کلیک روی یک لینک داخل پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **link_url:** آدرس لینک.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.click_message_url(
            "https://rubika.ir/joing/CHAT123",
            message_id="123456",
            link_url="https://example.com"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_click_inline_button"></a>
## [click_inline_button](#messenger_click_inline_button)

این متد برای شبیه‌سازی کلیک روی دکمه اینلاین (شیشه‌ای) یک پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام حاوی دکمه اینلاین.
- **button_id:** شناسه دکمه.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.click_inline_button(
            "@MyBot",
            message_id="1499338519906784",
            button_id="b0SPm00c8gb83b689ac2eeffe16ec7db"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-messages/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>