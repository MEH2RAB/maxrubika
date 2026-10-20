# دریافت و جستجوی پیام

---

<a id="messenger_get_message_info"></a>
## [get_message_info](#messenger_get_message_info)

این متد برای دریافت اطلاعات کامل یک پیام خاص به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    info = app.get_message_info("@Online_User", message_id="12345678900")
    print(info)
```

---

<a id="messenger_get_messages"></a>
## [get_messages](#messenger_get_messages)

این متد برای دریافت پیام‌های یک چت با قابلیت فیلتر بر اساس نوع پیام یا فرستنده است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **types:** نوع یا لیستی از انواع پیام برای فیلتر. انواع قابل قبول:
    - `text`, `image`, `video`, `video_message`, `voice`, `music`, `file`, `gif`
    - `live`, `location`, `poll`, `contact`, `event`, `edited`, `forwarded`
    - `sticker`, `me`, `bots`, `users`
    - همچنین می‌توانید GUID یا نام‌کاربری یک عضو را برای فیلتر پیام‌های او وارد کنید.

**نکات:**

1. فیلتر `contact` تنها در چت‌های خصوصی قابل استفاده است.
2. در کانال‌ها (`c0`) نمی‌توان بر اساس `member_guids` (GUID اعضا) فیلتر کرد.

**مثال‌ها:**

دریافت تمام پیام‌ها:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    messages = app.get_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD")
    print(messages)
```

دریافت فقط تصاویر و ویدیوها:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    images = app.get_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", types=["image", "video"])
    print(images)
```

دریافت پیام‌های یک کاربر خاص:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    user_msgs = app.get_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", types="u0xyz789...")
    print(user_msgs)
```

---

<a id="messenger_get_all_messages"></a>
## [get_all_messages](#messenger_get_all_messages)

این متد برای دریافت تمام پیام‌های یک چت از ابتدا تا انتها است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **show_message_ids:** در صورت True بودن، شناسه پیام‌ها در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**نکته:** این متد ممکن است برای چت‌های با پیام‌های زیاد زمان‌بر باشد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    all_msgs = app.get_all_messages("u0abc123...")
    print(all_msgs)
```

---

<a id="messenger_get_first_message"></a>
## [get_first_message](#messenger_get_first_message)

این متد برای دریافت اولین پیام یک چت است.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    first = app.get_first_message("@MyGroup")
    print(first)
```

---

<a id="messenger_get_first_messages"></a>
## [get_first_messages](#messenger_get_first_messages)

این متد برای دریافت اولین پیام‌های یک چت تا سقف مشخص است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **limit:** حداکثر تعداد پیام. (حداکثر ۱۰۰، پیش‌فرض: ۱۰۰)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    first_msgs = app.get_first_messages("@MyGroup", limit=50)
    print(first_msgs)
```

---

<a id="messenger_get_last_message"></a>
## [get_last_message](#messenger_get_last_message)

این متد برای دریافت آخرین پیام یک چت است.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    last = app.get_last_message("Cipher")
    print(last)
```

---

<a id="messenger_get_last_messages"></a>
## [get_last_messages](#messenger_get_last_messages)

این متد برای دریافت آخرین پیام‌های یک چت تا سقف مشخص است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **limit:** حداکثر تعداد پیام. (حداکثر ۵۰۰، پیش‌فرض: ۱۰۰)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    last_msgs = app.get_last_messages("Cipher", limit=20)
    print(last_msgs)
```

---

<a id="messenger_get_messages_by_id"></a>
## [get_messages_by_id](#messenger_get_messages_by_id)

این متد برای دریافت پیام‌ها با شناسه‌های مشخص است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_ids:** یک شناسه یا لیستی از شناسه‌های پیام.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    msgs = app.get_messages_by_id("https://rubika.ir/joing/CHAT123", message_ids=["12345678099", "45612378900", "12288762148"])
    print(msgs)
```

---

<a id="messenger_get_messages_interval"></a>
## [get_messages_interval](#messenger_get_messages_interval)

این متد برای دریافت بازه‌ای از پیام‌ها حول یک پیام میانی است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **middle_message_id:** شناسه پیام میانی.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    interval = app.get_messages_interval("u0abc123...", middle_message_id="14523674102")
    print(interval)
```

---

<a id="messenger_get_messages_updates"></a>
## [get_messages_updates](#messenger_get_messages_updates)

این متد برای دریافت به‌روزرسانی‌های پیام‌های یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **state:** وضعیت زمانی برای دریافت به‌روزرسانی‌ها. (پیش‌فرض: ۱۵۰ ثانیه قبل از زمان فعلی)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    updates = app.get_messages_updates("Undefined")
    print(updates)
```

---

<a id="messenger_get_chat_messages"></a>
## [get_chat_messages](#messenger_get_chat_messages)

این متد برای دریافت پیام‌های چت با قابلیت فیلتر و صفحه‌بندی است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **max_id:** حداکثر شناسه پیام برای شروع صفحه‌بندی. (پیش‌فرض: None)
- **sort:** جهت مرتب‌سازی. `FromMax` یا `FromMin`. (پیش‌فرض: FromMin)
- **filter_type:** فیلتر بر اساس نوع. مقادیر: `Voice`, `File`, `Music`, `Gif`, `Media`, `Link`. (پیش‌فرض: None)
- **limit:** حداکثر تعداد پیام. (پیش‌فرض: None - دریافت همه)

**مثال‌ها:**

دریافت پیام‌ها از جدیدترین:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    msgs = app.get_chat_messages("u0abc123...", sort="FromMax", limit=50)
    print(msgs)
```

دریافت فقط فایل‌ها:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    files = app.get_chat_messages("@MyChannel", filter_type="File")
    print(files)
```

---

<a id="messenger_search_messages"></a>
## [search_messages](#messenger_search_messages)

این متد برای جستجوی پیام‌ها بر اساس متن در یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **text:** متن مورد جستجو.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    results = app.search_messages("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD", text="سلام")
    print(results)
```

---

<a id="messenger_search_chat_messages"></a>
## [search_chat_messages](#messenger_search_chat_messages)

این متد برای جستجوی پیام‌ها در چت با استفاده از API سرور است. از هشتگ نیز پشتیبانی می‌کند.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **search_text:** متن مورد جستجو. اگر با `#` شروع شود، جستجو بر اساس هشتگ انجام می‌شود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    results = app.search_chat_messages("u0abc123...", search_text="#مهم")
    print(results)
```

---

<a id="messenger_search_global_messages"></a>
## [search_global_messages](#messenger_search_global_messages)

این متد برای جستجوی سراسری پیام‌ها در تمام چت‌ها است. از هشتگ نیز پشتیبانی می‌کند.

**پارامترها:**

- **search_text:** متن یا هشتگ مورد جستجو.
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    results = app.search_global_messages("#مهم")
    print(results)
```

---

<a id="messenger_get_message_url"></a>
## [get_message_url](#messenger_get_message_url)

این متد برای دریافت لینک قابل اشتراک‌گذاری یک پیام است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    url = app.get_message_url("@Online_User", message_id="12345674187")
    print(url)
```

---

<a id="messenger_get_scheduled_messages"></a>
## [get_scheduled_messages](#messenger_get_scheduled_messages)

این متد برای دریافت پیام‌های زمان‌بندی شده یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    scheduled = app.get_scheduled_messages("@CodeYaran")
    print(scheduled)
```

---

<a id="messenger_get_pinned_messages"></a>
## [get_pinned_messages](#messenger_get_pinned_messages)

این متد برای دریافت پیام‌های پین‌شده یک چت است.

**پارامتر:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    pinned = app.get_pinned_messages("@MyGroup")
    print(pinned)
```

---

<a id="messenger_get_messages_reactions"></a>
## [get_messages_reactions](#messenger_get_messages_reactions)

این متد برای دریافت ری‌اکشن‌های پیام‌های یک چت در یک بازه مشخص است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **min_id:** حداقل شناسه پیام (کران پایین).
- **max_id:** حداکثر شناسه پیام (کران بالا).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    reactions = app.get_messages_reactions("u0abc123...", min_id="100", max_id="200")
    print(reactions)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-messages/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>