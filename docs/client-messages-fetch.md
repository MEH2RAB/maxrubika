# دریافت و جستجوی پیام

---

<a id="client_get_message_info"></a>
## [get_message_info](#client_get_message_info)

این متد برای دریافت اطلاعات کامل یک پیام خاص به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام مورد نظر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_message_info("u0abc123...", message_id="12345678900")
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_get_messages"></a>
## [get_messages](#client_get_messages)

این متد برای دریافت پیام‌های یک چت با قابلیت فیلتر بر اساس نوع پیام یا فرستنده است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **types:** نوع یا لیستی از انواع پیام برای فیلتر. انواع قابل قبول:
    - `text`, `image`, `video`, `video_message`, `voice`, `music`, `file`, `gif`
    - `live`, `location`, `poll`, `contact`, `event`, `edited`, `forwarded`
    - `sticker`, `me`, `bots`, `users`
    - همچنین می‌توانید GUID یا نام‌کاربری یک عضو را برای فیلتر پیام‌های او وارد کنید.

**نکته:** فیلتر `contact` تنها در چت‌های خصوصی قابل استفاده است.

**مثال‌ها:**

دریافت تمام پیام‌ها:

```python
from maxrubika import Client
client = Client("mySession")

try:
    messages = client.get_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD")
    print(messages)

except Exception as e:
    print(e)
```

دریافت فقط تصاویر و فقط ویدیو:

```python
from maxrubika import Client
client = Client("mySession")

try:
    images = client.get_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", types=["image", "vodeo"])
    print(images)

except Exception as e:
    print(e)
```

دریافت پیام‌های یک کاربر خاص:

```python
from maxrubika import Client
client = Client("mySession")

try:
    user_msgs = client.get_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", types="u0xyz789...")
    print(user_msgs)

except Exception as e:
    print(e)
```

---

<a id="client_get_all_messages"></a>
## [get_all_messages](#client_get_all_messages)

این متد برای دریافت تمام پیام‌های یک چت از ابتدا تا انتها است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **show_message_ids:** در صورت True بودن، شناسه پیام‌ها در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**نکته:** این متد ممکن است برای چت‌های با پیام‌های زیاد زمان‌بر باشد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    all_msgs = client.get_all_messages("u0abc123...")
    print(all_msgs)

except Exception as e:
    print(e)
```

---

<a id="client_get_first_message"></a>
## [get_first_message](#client_get_first_message)

این متد برای دریافت اولین پیام یک چت است.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    first = client.get_first_message("u0abc123...")
    print(first)

except Exception as e:
    print(e)
```

---

<a id="client_get_first_messages"></a>
## [get_first_messages](#client_get_first_messages)

این متد برای دریافت اولین پیام‌های یک چت تا سقف مشخص است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **limit:** حداکثر تعداد پیام. (حداکثر ۱۰۰، پیش‌فرض: ۱۰۰)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    first_msgs = client.get_first_messages("u0abc123...", limit=50)
    print(first_msgs)

except Exception as e:
    print(e)
```

---

<a id="client_get_last_message"></a>
## [get_last_message](#client_get_last_message)

این متد برای دریافت آخرین پیام یک چت است.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    last = client.get_last_message("Cipher")
    print(last)

except Exception as e:
    print(e)
```

---

<a id="client_get_last_messages"></a>
## [get_last_messages](#client_get_last_messages)

این متد برای دریافت آخرین پیام‌های یک چت تا سقف مشخص است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **limit:** حداکثر تعداد پیام. (حداکثر ۱۰۰، پیش‌فرض: ۱۰۰)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    last_msgs = client.get_last_messages("Cipher", limit=20)
    print(last_msgs)

except Exception as e:
    print(e)
```

---

<a id="client_get_messages_by_id"></a>
## [get_messages_by_id](#client_get_messages_by_id)

این متد برای دریافت پیام‌ها با شناسه‌های مشخص است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_ids:** یک شناسه یا لیستی از شناسه‌های پیام.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    msgs = client.get_messages_by_id("u0abc123...", message_ids=["12345678099", "45612378900", "12288762148"])
    print(msgs)

except Exception as e:
    print(e)
```

---

<a id="client_get_messages_interval"></a>
## [get_messages_interval](#client_get_messages_interval)

این متد برای دریافت بازه‌ای از پیام‌ها حول یک پیام میانی است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **middle_message_id:** شناسه پیام میانی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    interval = client.get_messages_interval("u0abc123...", middle_message_id="14523674102")
    print(interval)

except Exception as e:
    print(e)
```

---

<a id="client_get_messages_updates"></a>
## [get_messages_updates](#client_get_messages_updates)

این متد برای دریافت به‌روزرسانی‌های پیام‌های یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **state:** وضعیت زمانی برای دریافت به‌روزرسانی‌ها. (پیش‌فرض: ۱۵۰ ثانیه قبل از زمان فعلی)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    updates = client.get_messages_updates("Undefined")
    print(updates)

except Exception as e:
    print(e)
```

---

<a id="client_get_chat_messages"></a>
## [get_chat_messages](#client_get_chat_messages)

این متد برای دریافت پیام‌های چت با قابلیت فیلتر و صفحه‌بندی است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **sort:** جهت مرتب‌سازی. `FromMax` یا `FromMin`. (پیش‌فرض: FromMin)
- **filter_type:** فیلتر بر اساس نوع. مقادیر: `Voice`, `File`, `Music`, `Gif`, `Media`, `Link`. (پیش‌فرض: None)
- **limit:** حداکثر تعداد پیام. (پیش‌فرض: None - دریافت همه)

**مثال‌ها:**

دریافت پیام‌ها از جدیدترین:

```python
from maxrubika import Client
client = Client("mySession")

try:
    msgs = client.get_chat_messages("u0abc123...", sort="FromMax", limit=50)
    print(msgs)

except Exception as e:
    print(e)
```

دریافت فقط فایل‌ها:

```python
from maxrubika import Client
client = Client("mySession")

try:
    files = client.get_chat_messages("u0abc123...", filter_type="File")
    print(files)

except Exception as e:
    print(e)
```

---

<a id="client_search_messages"></a>
## [search_messages](#client_search_messages)

این متد برای جستجوی پیام‌ها بر اساس متن در یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **text:** متن مورد جستجو.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    results = client.search_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", text="سلام")
    print(results)

except Exception as e:
    print(e)
```

---

<a id="client_search_chat_messages"></a>
## [search_chat_messages](#client_search_chat_messages)

این متد برای جستجوی پیام‌ها در چت با استفاده از API سرور است. از هشتگ نیز پشتیبانی می‌کند.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **search_text:** متن مورد جستجو. اگر با `#` شروع شود، جستجو بر اساس هشتگ انجام می‌شود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    results = client.search_chat_messages("u0abc123...", search_text="#مهم")
    print(results)

except Exception as e:
    print(e)
```

---

<a id="client_get_message_url"></a>
## [get_message_url](#client_get_message_url)

این متد برای دریافت لینک قابل اشتراک‌گذاری یک پیام است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    url = client.get_message_url("u0abc123...", message_id="12345674187")
    print(url)

except Exception as e:
    print(e)
```

---

<a id="client_get_scheduled_messages"></a>
## [get_scheduled_messages](#client_get_scheduled_messages)

این متد برای دریافت پیام‌های زمان‌بندی شده یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    scheduled = client.get_scheduled_messages("@CodeYaran")
    print(scheduled)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="client-methods-messages" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>