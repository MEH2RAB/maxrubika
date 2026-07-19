# تنظیمات چت

---

<a id="client_mute_chat"></a>
## [mute_chat](#client_mute_chat)

این متد برای بی‌صدا کردن (Mute) یک چت است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **duration:** مدت زمان بی‌صدا کردن به ثانیه (حداقل ۱۸۰۰ ثانیه / ۳۰ دقیقه) یا `timedelta`. (پیش‌فرض: None - بی‌صدای دائمی)

**مثال‌ها:**

۱. بی‌صدای دائمی:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.mute_chat("g0abc123...")
    print(result)

except Exception as e:
    print(e)
```

۲. بی‌صدا برای ۲ ساعت:

```python
from datetime import timedelta
from maxrubika import Client
client = Client("mySession")

try:
    result = client.mute_chat("g0abc123...", duration=timedelta(hours=2))
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_unmute_chat"></a>
## [unmute_chat](#client_unmute_chat)

این متد برای لغو بی‌صدا کردن (Unmute) یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.unmute_chat("g0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_pin_chat"></a>
## [pin_chat](#client_pin_chat)

این متد برای سنجاق کردن (Pin) یک چت در بالای لیست چت‌ها است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.pin_chat("u0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_unpin_chat"></a>
## [unpin_chat](#client_unpin_chat)

این متد برای برداشتن سنجاق (Unpin) یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.unpin_chat("u0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_pin_chat_in_folder"></a>
## [pin_chat_in_folder](#client_pin_chat_in_folder)

این متد برای سنجاق کردن یک چت در یک پوشه خاص است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **folder_id:** شناسه پوشه.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.pin_chat_in_folder("u0abc123...", folder_id="folder_123")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_unpin_chat_in_folder"></a>
## [unpin_chat_in_folder](#client_unpin_chat_in_folder)

این متد برای برداشتن سنجاق یک چت از یک پوشه خاص است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **folder_id:** شناسه پوشه.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.unpin_chat_in_folder("u0abc123...", folder_id="folder_123")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_archive_chat"></a>
## [archive_chat](#client_archive_chat)

این متد برای آرشیو کردن یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.archive_chat("u0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_unarchive_chat"></a>
## [unarchive_chat](#client_unarchive_chat)

این متد برای خارج کردن یک چت از آرشیو است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.unarchive_chat("u0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_seen_chats"></a>
## [seen_chats](#client_seen_chats)

این متد برای علامت‌گذاری چند چت به عنوان دیده‌شده است.

**پارامتر:**

- **seen_list:** دیکشنری شامل GUID چت‌ها و آخرین شناسه پیام دیده‌شده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.seen_chats({
        "u0abc123...": "123456",
        "g0xyz789...": "789012"
    })
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_set_chat_protected_content"></a>
## [set_chat_protected_content](#client_set_chat_protected_content)

این متد برای تنظیم محتوای محافظت‌شده (جلوگیری از اسکرین‌شات و ذخیره) در گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **enabled:** `True` برای فعال‌سازی، `False` برای غیرفعال‌سازی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_chat_protected_content("g0abc123...", enabled=True)
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_set_chat_auto_delete"></a>
## [set_chat_auto_delete](#client_set_chat_auto_delete)

این متد برای تنظیم حذف خودکار پیام‌ها در گروه یا کانال است.

**پارامترها:**

- **chat:** یک GUID/لینک/نام‌کاربری یا لیستی از آن‌ها.
- **auto_delete:** مدت زمان حذف خودکار. مقادیر قابل قبول:
    - عدد: ۱ تا ۳۶۵ (روز)
    - رشته: `1m` تا `60m`، `1h` تا `24h`، `1d` تا `365d`، `1w` تا `52w`، `1y`، `off`
    - کلمات: `day`, `week`, `month`, `year`, `never`, `disabled`

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_chat_auto_delete("g0abc123...", auto_delete="7d")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_set_chat_use_time"></a>
## [set_chat_use_time](#client_set_chat_use_time)

این متد برای ارسال زمان استفاده از چت به سرور است. این کار به سرور کمک می‌کند رفتار طبیعی کاربر را تشخیص دهد.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **use_time:** زمان سپری‌شده در چت به میلی‌ثانیه.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_chat_use_time("u0abc123...", use_time=5000)
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_chat_history"></a>
## [delete_chat_history](#client_delete_chat_history)

این متد برای حذف تاریخچه چت تا آخرین پیام است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت (کاربر یا گروه). برای کانال‌ها قابل استفاده نیست.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_chat_history("u0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_report_chat"></a>
## [report_chat](#client_report_chat)

این متد برای گزارش یک چت (کاربر، گروه، کانال) است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری چت.
- **report_type:** نوع گزارش.
- **description:** توضیحات اضافی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.report_chat(
        "u0abc123...",
        report_type="Spam",
        description="کاربر اسپمر"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_set_ask_spam"></a>
## [set_ask_spam](#client_set_ask_spam)

این متد برای انجام عملیات روی یک درخواست اسپم معلق است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری کاربر، گروه یا کانال.
- **action:** عملیات مورد نظر:
    - برای کاربر (u0): `AddToContact`، `BlockUser`، `Cancel`.
    - برای گروه/کانال (g0/c0): `ReportAndLeave`.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_ask_spam("u0abc123...", action="BlockUser")
    print(result)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-chat/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>