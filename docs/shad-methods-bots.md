# بات‌ها

---

<a id="shad_get_bot_info"></a>
## [get_bot_info](#shad_get_bot_info)

این متد برای دریافت اطلاعات یک بات به کار می‌رود.

**پارامتر:**

- **bot:** شناسه (GUID) یا نام‌کاربری بات مورد نظر.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد. همچنین می‌توانید مستقیماً GUID بات (که با `b0` شروع می‌شود) را نیز پاس دهید.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    info = app.get_bot_info("@ShowInfoBot")
    print(info)
```

---

<a id="shad_get_inline_bots"></a>
## [get_inline_bots](#shad_get_inline_bots)

این متد برای دریافت اطلاعات یک یا چند بات اینلاین به کار می‌رود.

**پارامتر:**

- **bots:** یک بات یا لیستی از بات‌ها (شناسه GUID یا نام‌کاربری).

**نکته:** اگر یک رشته پاس دهید، کتابخانه به‌صورت خودکار آن را در یک لیست قرار می‌دهد.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    # یک بات
    info = app.get_inline_bots("@ShowInfoBot")
    print(info)

    # چند بات
    infos = app.get_inline_bots(["@ShowInfoBot", "@TestBot"])
    print(infos)
```

---

<a id="shad_get_service_info"></a>
## [get_service_info](#shad_get_service_info)

این متد برای دریافت اطلاعات یک سرویس به کار می‌رود.

**پارامتر:**

- **service:** شناسه (GUID) سرویس مورد نظر. باید با `s0` شروع شده و مجموعاً ۳۲ کاراکتر باشد.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    info = app.get_service_info("s0abcdefghijklmnopqrstuvwxyz12")
    print(info)
```

---

<a id="shad_start_bot"></a>
## [start_bot](#shad_start_bot)

این متد برای ارسال دستور `/start` به یک بات و راه‌اندازی آن به کار می‌رود.

**پارامتر:**

- **bot:** شناسه (GUID) یا نام‌کاربری بات مورد نظر.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.start_bot("@TestBot")
    print(result)
```

---

<a id="shad_stop_bot"></a>
## [stop_bot](#shad_stop_bot)

این متد برای متوقف کردن یک بات به کار می‌رود.

**پارامتر:**

- **bot:** شناسه (GUID) یا نام‌کاربری بات مورد نظر.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.stop_bot("@TestBot")
    print(result)
```

---

<a id="shad_delete_bot_chat"></a>
## [delete_bot_chat](#shad_delete_bot_chat)

این متد برای حذف تاریخچه چت با یک بات به کار می‌رود.

**پارامتر:**

- **bot:** شناسه (GUID) یا نام‌کاربری بات مورد نظر.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.delete_bot_chat("@TestBot")
    print(result)
```

---

<a id="shad_delete_service_chat"></a>
## [delete_service_chat](#shad_delete_service_chat)

این متد برای حذف تاریخچه چت با یک سرویس به کار می‌رود.

**پارامتر:**

- **service:** شناسه (GUID) سرویس مورد نظر. باید با `s0` شروع شده و مجموعاً ۳۲ کاراکتر باشد.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.delete_service_chat("s0abcdefghijklmnopqrstuvwxyz12")
    print(result)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../shad-methods/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>