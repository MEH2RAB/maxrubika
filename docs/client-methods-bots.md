# بات‌ها

---

<a id="client_get_bot_info"></a>
## [get_bot_info](#client_get_bot_info)

این متد برای دریافت اطلاعات یک بات به کار می‌رود.

**پارامتر:**

- **bot:** شناسه (GUID) یا نام‌کاربری بات مورد نظر.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_bot_info("@ShowInfoBot")
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_get_service_info"></a>
## [get_service_info](#client_get_service_info)

این متد برای دریافت اطلاعات یک سرویس به کار می‌رود.

**پارامتر:**

- **service:** شناسه (GUID) سرویس مورد نظر. باید با `s0` شروع شده و ۳۲ کاراکتر باشد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_service_info("s0abcdefghijklmnopqrstuvwxyz12")
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_start_bot"></a>
## [start_bot](#client_start_bot)

این متد برای ارسال دستور `/start` به یک بات و راه‌اندازی آن به کار می‌رود.

**پارامتر:**

- **bot:** شناسه (GUID) یا نام‌کاربری بات مورد نظر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.start_bot("@TestBot")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_stop_bot"></a>
## [stop_bot](#client_stop_bot)

این متد برای متوقف کردن یک بات به کار می‌رود.

**پارامتر:**

- **bot:** شناسه (GUID) یا نام‌کاربری بات مورد نظر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.stop_bot("@TestBot")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_bot_chat"></a>
## [delete_bot_chat](#client_delete_bot_chat)

این متد برای حذف تاریخچه چت با یک بات به کار می‌رود.

**پارامترها:**

- **bot:** شناسه (GUID) یا نام‌کاربری بات مورد نظر.
- **last_deleted_message_id:** شناسه آخرین پیام حذف‌شده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_bot_chat("@TestBot", last_deleted_message_id="12345678900")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_service_chat"></a>
## [delete_service_chat](#client_delete_service_chat)

این متد برای حذف تاریخچه چت با یک سرویس به کار می‌رود.

**پارامترها:**

- **service:** شناسه (GUID) سرویس مورد نظر. باید با `s0` شروع شده و ۳۲ کاراکتر باشد.
- **last_deleted_message_id:** شناسه آخرین پیام حذف‌شده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_service_chat("s0abcdefghijklmnopqrstuvwxyz12", last_deleted_message_id="12345678900")
    print(result)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>