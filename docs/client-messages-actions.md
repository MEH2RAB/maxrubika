# عملیات روی پیام‌ها

---

<a id="client_edit_message"></a>
## [edit_message](#client_edit_message)

این متد برای ویرایش متن یک پیام ارسال‌شده به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام مورد نظر.
- **text:** متن جدید جایگزین.
- **metadata:** متادیتای قالب‌بندی متن (Bold، Italic و...). (پیش‌فرض: None - تشخیص خودکار)

**نکته:** در صورت عدم ارسال metadata، کتابخانه به صورت خودکار متادیتا را از متن استخراج می‌کند.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.edit_message(
        "u0abc123...",
        message_id="12345678090",
        text="متن ویرایش شده جدید"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_messages"></a>
## [delete_messages](#client_delete_messages)

این متد برای حذف یک یا چند پیام از یک چت به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_ids:** یک شناسه یا لیستی از شناسه‌های پیام برای حذف.
- **type:** نوع حذف. `Global` (حذف برای همه)، `Local` (حذف فقط برای خود)، `Scheduled` (حذف پیام زمان‌بندی شده). (پیش‌فرض: Global)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_messages(
        "u0abc123...",
        message_ids=["123", "456", "789"]
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_all_messages"></a>
## [delete_all_messages](#client_delete_all_messages)

این متد برای حذف تمام پیام‌های یک چت (به جز پیام ایجاد گروه/کانال) به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **exclude_message_ids:** شناسه پیام‌هایی که نباید حذف شوند. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_all_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_my_messages"></a>
## [delete_my_messages](#client_delete_my_messages)

این متد برای حذف تمام پیام‌های خودتان در یک چت به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **exclude_message_ids:** شناسه پیام‌هایی که نباید حذف شوند. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_my_messages("g0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_auto_delete_message"></a>
## [auto_delete_message](#client_auto_delete_message)

این متد برای حذف خودکار یک پیام پس از مدت زمان مشخص به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **time:** مدت زمان تأخیر تا حذف (به ثانیه).

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.auto_delete_message(
        "u0abc123...",
        message_id="12345674103",
        time=60
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_forward_messages"></a>
## [forward_messages](#client_forward_messages)

این متد برای فوروارد (هدایت) یک یا چند پیام از یک چت به چت دیگر به کار می‌رود.

**پارامترها:**

- **from_chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مبدأ.
- **message_ids:** شناسه پیام‌ها برای فوروارد.
- **to_chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **drop_author:** مخفی کردن فرستنده اصلی. (پیش‌فرض: False)
- **is_mute:** فوروارد بی‌صدا بدون اعلان. (پیش‌فرض: False)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.forward_messages(
        from_chat="u0abc123...",
        message_ids=["123", "456"],
        to_chat="u0xyz789..."
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_pin_message"></a>
## [pin_message](#client_pin_message)

این متد برای سنجاق کردن (پین) یک پیام در چت به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.pin_message("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", message_id=147503987410)
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_unpin_message"></a>
## [unpin_message](#client_unpin_message)

این متد برای برداشتن سنجاق (آنپین) یک پیام در چت به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.unpin_message("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", message_id=12345636971)
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_unpin_all_messages"></a>
## [unpin_all_messages](#client_unpin_all_messages)

این متد برای برداشتن سنجاق تمام پیام‌های پین شده در یک چت به کار می‌رود.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.unpin_all_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_get_pinned_messages"></a>
## [get_pinned_messages](#client_get_pinned_messages)

این متد برای دریافت تمام پیام‌های سنجاق شده یک چت به کار می‌رود.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    pinned = client.get_pinned_messages("g0abc123...")
    print(pinned)

except Exception as e:
    print(e)
```

---

<a id="client_add_reaction"></a>
## [add_reaction](#client_add_reaction)

این متد برای افزودن ری‌اکشن به یک پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **reaction_id:** شناسه ری‌اکشن.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.add_reaction(
        "u0abc123...",
        message_id="123456",
        reaction_id=1
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_remove_reaction"></a>
## [remove_reaction](#client_remove_reaction)

این متد برای حذف ری‌اکشن از یک پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **reaction_id:** شناسه ری‌اکشن.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.remove_reaction(
        "u0abc123...",
        message_id="123456",
        reaction_id=1
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_get_messages_reactions"></a>
## [get_messages_reactions](#client_get_messages_reactions)

این متد برای دریافت ری‌اکشن‌های پیام‌ها در یک بازه مشخص به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **min_id:** حداقل شناسه پیام (کران پایین).
- **max_id:** حداکثر شناسه پیام (کران بالا).

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    reactions = client.get_messages_reactions(
        "u0abc123...",
        min_id="100",
        max_id="200"
    )
    print(reactions)

except Exception as e:
    print(e)
```

---

<a id="client_report_message"></a>
## [report_message](#client_report_message)

این متد برای گزارش یک پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **report_type:** نوع گزارش.
- **description:** توضیحات اضافی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.report_message(
        "u0abc123...",
        message_id="123456",
        report_type="Spam",
        description="پیام اسپم"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_mark_as_read"></a>
## [mark_as_read](#client_mark_as_read)

این متد برای علامت‌گذاری یک چت به عنوان خوانده‌شده (با دیدن آخرین پیام) به کار می‌رود.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.mark_as_read("u0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_mark_as_seen"></a>
## [mark_as_seen](#client_mark_as_seen)

این متد برای علامت‌گذاری یک پیام خاص به عنوان دیده‌شده به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام. (پیش‌فرض: None - آخرین پیام)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.mark_as_seen("u0abc123...", message_id="123456")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_click_message_url"></a>
## [click_message_url](#client_click_message_url)

این متد برای شبیه‌سازی کلیک روی یک لینک داخل پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.
- **link_url:** آدرس لینک.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.click_message_url(
        "u0abc123...",
        message_id="123456",
        link_url="https://example.com"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_click_inline_button"></a>
## [click_inline_button](#client_click_inline_button)

این متد برای شبیه‌سازی کلیک روی دکمه اینلاین (شیشه‌ای) یک پیام به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام حاوی دکمه اینلاین.
- **button_id:** شناسه دکمه.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.click_inline_button(
        "u0abc123...",
        message_id="1499338519906784",
        button_id="b0SPm00c8ab83b689ac2eeffe16ec7db"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="/client-methods-messages" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>