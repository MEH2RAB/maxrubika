# سایر متدها

---

## متدهای اصلی و راه‌اندازی

<a id="client_connect"></a>
### [connect](#client_connect)

برقراری ارتباط با API روبیکا. یک نمونه Api ایجاد می‌کند و اطلاعات نشست ذخیره شده (auth, guid, private_key, user_agent) را در صورت وجود بارگذاری می‌کند.

**خروجی:**

- **Client:** نمونه کلاینت با اتصال فعال.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")
client.connect()
```

---

<a id="client_start"></a>
### [start](#client_start)

شروع کلاینت، مدیریت احراز هویت و ثبت‌نام.

**پارامترها:**

- **phone_number** (str, optional): شماره تلفن برای ثبت‌نام.

**خروجی:**

- **Client:** نمونه کلاینت مقداردهی‌شده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")
client.start("+989123456789")
```

---

<a id="client_run"></a>
### [run](#client_run)

شروع کلاینت و گوش دادن به به‌روزرسانی‌ها. اطمینان از برقراری اتصال، سپس اجرای اختیاری یک coroutine قبل از ورود به حلقه به‌روزرسانی. هم در محیط‌های sync و هم async کار می‌کند.

**پارامترها:**

- **coroutine** (Coroutine, optional): Coroutine اختیاری برای اجرا قبل از گوش دادن به به‌روزرسانی‌ها.

**خروجی:**

- **None:** در حالت عادی تا زمانی که متوقف نشود، اجرا می‌شود.

**مثال sync:**

```python
from maxrubika import Client

client = Client("mySession")
client.run()
```

**مثال async:**

```python
from maxrubika import Client

async with Client("mySession") as app:
    await app.run()
```

---

<a id="client_disconnect"></a>
### [disconnect](#client_disconnect)

قطع ارتباط با سرور روبیکا.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")
client.start()
# ... انجام عملیات ...
client.disconnect()
```

---

## متدهای دریافت به‌روزرسانی

<a id="client_get_updates"></a>
### [get_updates](#client_get_updates)

دریافت به‌روزرسانی‌ها از WebSocket روبیکا.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    # این متد به صورت نامحدود اجرا می‌شود و به‌روزرسانی‌ها را دریافت می‌کند
    client.get_updates()

except Exception as e:
    print(e)
```

---

## متدهای درخواست

<a id="client_request"></a>
### [request](#client_request)

ساخت و ارسال درخواست به API روبیکا.

**پارامترها:**

- **method** (str): نام متد API (مانند 'sendMessage', 'getUserInfo').
- **input** (dict, optional): داده‌های ورودی برای متد.
- **tmp_session** (bool): استفاده از نشست موقت به جای auth (پیش‌فرض: False).
- **encrypt** (bool): رمزگذاری داده‌های درخواست (پیش‌فرض: True).

**خروجی:**

- **Data or None:** پاسخ API.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.request(
        method="getUserInfo",
        input={"user_guid": "u0abc123..."}
    )
    print(result)

except Exception as e:
    print(e)
```

---

## متدهای فایل

<a id="client_upload_file"></a>
### [upload_file](#client_upload_file)

آپلود فایل به روبیکا.

**پارامترها:**

- **file** (str or bytes): مسیر فایل یا bytes برای آپلود.
- **mime** (str, optional): نوع MIME فایل.
- **file_name** (str, optional): نام فایل.
- **chunk** (int, optional): اندازه هر بخش به بایت (پیش‌فرض: 1MB).
- **callback** (callable, optional): تابع پیشرفت آپلود (total_size, uploaded_bytes).

**خروجی:**

- متادیتای فایل آپلود شده شامل mime, size, dc_id, file_id, file_name, access_hash_rec.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.upload_file(
        file="file.jpg",
        mime="image/jpeg",
        file_name="my_image.jpg"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_download_file"></a>
### [download_file](#client_download_file)

دانلود فایل از سرورهای روبیکا با استفاده از شناسه فایل و access hash.

**پارامترها:**

- **dc_id** (int): شناسه دیتاسنتر.
- **file_id** (int): شناسه یکتای فایل.
- **access_hash** (str): هش دسترسی مرتبط با فایل.
- **size** (int): اندازه کل فایل به بایت.
- **chunk** (int, optional): اندازه هر بخش دانلود (پیش‌فرض: 131072).
- **callback** (callable, optional): تابع پیشرفت دانلود (total_size, downloaded_size).
- **gather** (bool, optional): دانلود بخش‌ها به صورت موازی (پیش‌فرض: False).
- **save_as** (str or bool, optional): مسیر دایرکتوری یا True برای دایرکتوری جاری. اگر None باشد، بایت‌ها را برمی‌گرداند.
- **file_name** (str, optional): نام سفارشی فایل.

**خروجی:**

- **bytes or str:** محتوای فایل (bytes) یا مسیر ذخیره شده (str).

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.download_file(
        dc_id=1,
        file_id=123456,
        access_hash="hash_example",
        size=1024000,
        save_as=True,
        file_name="my_file.jpg"
    )
    print(result)

except Exception as e:
    print(e)
```

---

## متدهای کمکی

<a id="client_get_time"></a>
### [get_time](#client_get_time)

این متد برای دریافت زمان فعلی سرور به کار می‌رود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    time = client.get_time()
    print(time)

except Exception as e:
    print(e)
```

---

<a id="client_get_available_reactions"></a>
### [get_available_reactions](#client_get_available_reactions)

این متد برای دریافت لیست ری‌اکشن‌های قابل استفاده در چت‌ها به کار می‌رود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    reactions = client.get_available_reactions()
    print(reactions)

except Exception as e:
    print(e)
```

---

<a id="client_get_location_view"></a>
### [get_location_view](#client_get_location_view)

این متد برای دریافت نقشه یک موقعیت جغرافیایی به کار می‌رود.

**پارامترها:**

- **latitude:** عرض جغرافیایی. (عددی بین ۹۰- تا ۹۰)
- **longitude:** طول جغرافیایی. (عددی بین ۱۸۰- تا ۱۸۰)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    view = client.get_location_view(latitude=35.6892, longitude=51.3890)
    print(view)

except Exception as e:
    print(e)
```

---

<a id="client_get_wallpapers"></a>
### [get_wallpapers](#client_get_wallpapers)

این متد برای دریافت تنظیمات فعلی تصویر پس‌زمینه چت به کار می‌رود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    wallpapers = client.get_wallpapers()
    print(wallpapers)

except Exception as e:
    print(e)
```

---

<a id="client_reset_wallpapers"></a>
### [reset_wallpapers](#client_reset_wallpapers)

این متد برای بازنشانی تمام تصاویر پس‌زمینه چت‌ها به حالت پیش‌فرض به کار می‌رود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.reset_wallpapers()
    print(result)

except Exception as e:
    print(e)
```

---

## متدهای استیکر و گیف

<a id="client_get_sticker_setting"></a>
### [get_sticker_setting](#client_get_sticker_setting)

این متد برای دریافت تنظیمات استیکر کاربر فعلی به کار می‌رود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    settings = client.get_sticker_setting()
    print(settings)

except Exception as e:
    print(e)
```

---

<a id="client_get_my_sticker_sets"></a>
### [get_my_sticker_sets](#client_get_my_sticker_sets)

این متد برای دریافت مجموعه استیکرهای متعلق به کاربر به کار می‌رود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    stickers = client.get_my_sticker_sets()
    print(stickers)

except Exception as e:
    print(e)
```

---

<a id="client_get_my_archived_sticker_sets"></a>
### [get_my_archived_sticker_sets](#client_get_my_archived_sticker_sets)

این متد برای دریافت مجموعه استیکرهای آرشیو شده کاربر به کار می‌رود.

**پارامتر:**

- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    archived = client.get_my_archived_sticker_sets()
    print(archived)

except Exception as e:
    print(e)
```

---

<a id="client_get_sticker_set_by_id"></a>
### [get_sticker_set_by_id](#client_get_sticker_set_by_id)

این متد برای دریافت یک مجموعه استیکر با شناسه آن به کار می‌رود.

**پارامتر:**

- **sticker_set_id:** شناسه مجموعه استیکر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    sticker_set = client.get_sticker_set_by_id("sticker_set_id_123")
    print(sticker_set)

except Exception as e:
    print(e)
```

---

<a id="client_get_stickers_by_set_ids"></a>
### [get_stickers_by_set_ids](#client_get_stickers_by_set_ids)

این متد برای دریافت استیکرها با شناسه مجموعه‌های آن‌ها به کار می‌رود.

**پارامتر:**

- **sticker_set_ids:** یک شناسه یا لیستی از شناسه‌های مجموعه استیکر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    stickers = client.get_stickers_by_set_ids(["id1", "id2", "id3"])
    print(stickers)

except Exception as e:
    print(e)
```

---

<a id="client_get_stickers_by_emoji"></a>
### [get_stickers_by_emoji](#client_get_stickers_by_emoji)

این متد برای دریافت استیکرها بر اساس ایموجی به کار می‌رود.

**پارامترها:**

- **emoji:** کاراکتر ایموجی.
- **suggest_by:** نوع پیشنهاد. (پیش‌فرض: All)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    stickers = client.get_stickers_by_emoji("😊")
    print(stickers)

except Exception as e:
    print(e)
```

---

<a id="client_search_stickers"></a>
### [search_stickers](#client_search_stickers)

این متد برای جستجوی استیکرها به کار می‌رود.

**پارامترها:**

- **search_text:** متن جستجو. (پیش‌فرض: خالی)
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    results = client.search_stickers(search_text="سلام")
    print(results)

except Exception as e:
    print(e)
```

---

<a id="client_get_trend_sticker_sets"></a>
### [get_trend_sticker_sets](#client_get_trend_sticker_sets)

این متد برای دریافت مجموعه استیکرهای پرطرفدار به کار می‌رود.

**پارامتر:**

- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    trending = client.get_trend_sticker_sets()
    print(trending)

except Exception as e:
    print(e)
```

---

<a id="client_add_sticker_set"></a>
### [add_sticker_set](#client_add_sticker_set)

این متد برای افزودن یک مجموعه استیکر به مجموعه‌های کاربر به کار می‌رود.

**پارامتر:**

- **sticker_set_id:** شناسه مجموعه استیکر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.add_sticker_set("sticker_set_id_123")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_sticker_set"></a>
### [delete_sticker_set](#client_delete_sticker_set)

این متد برای حذف یک مجموعه استیکر از مجموعه‌های کاربر به کار می‌رود.

**پارامتر:**

- **sticker_set_id:** شناسه مجموعه استیکر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_sticker_set("sticker_set_id_123")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_get_my_gif_set"></a>
### [get_my_gif_set](#client_get_my_gif_set)

این متد برای دریافت مجموعه گیف‌های شخصی کاربر به کار می‌رود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    gifs = client.get_my_gif_set()
    print(gifs)

except Exception as e:
    print(e)
```

---

<a id="client_add_to_my_gif_set"></a>
### [add_to_my_gif_set](#client_add_to_my_gif_set)

این متد برای افزودن یک گیف به مجموعه گیف‌های شخصی کاربر به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت حاوی گیف.
- **message_id:** شناسه پیام گیف.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.add_to_my_gif_set("g0abc123...", message_id="123456")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_my_gif_set"></a>
### [delete_my_gif_set](#client_delete_my_gif_set)

این متد برای حذف یک گیف از مجموعه گیف‌های شخصی کاربر به کار می‌رود.

**پارامتر:**

- **file_id:** شناسه فایل گیف.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_my_gif_set("file_id_123")
    print(result)

except Exception as e:
    print(e)
```

---

## متدهای پخش زنده

<a id="client_get_live_status"></a>
### [get_live_status](#client_get_live_status)

این متد برای دریافت وضعیت یک پخش زنده به کار می‌رود.

**پارامترها:**

- **live_id:** شناسه پخش زنده.
- **access_token:** توکن دسترسی دریافت‌شده از پاسخ send_live.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    status = client.get_live_status(live_id="live_123", access_token="token_abc")
    print(status)

except Exception as e:
    print(e)
```

---

<a id="client_get_live_comments"></a>
### [get_live_comments](#client_get_live_comments)

این متد برای دریافت نظرات یک پخش زنده به کار می‌رود.

**پارامترها:**

- **live_id:** شناسه پخش زنده.
- **access_token:** توکن دسترسی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    comments = client.get_live_comments(live_id="live_123", access_token="token_abc")
    print(comments)

except Exception as e:
    print(e)
```

---

<a id="client_get_live_play_url"></a>
### [get_live_play_url](#client_get_live_play_url)

این متد برای دریافت URL پخش یک لایو به کار می‌رود.

**پارامترها:**

- **access_token:** توکن دسترسی.
- **live_id:** شناسه پخش زنده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    url = client.get_live_play_url(access_token="token_abc", live_id="live_123")
    print(url)

except Exception as e:
    print(e)
```

---

<a id="client_add_live_comment"></a>
### [add_live_comment](#client_add_live_comment)

این متد برای افزودن نظر به یک پخش زنده به کار می‌رود.

**پارامترها:**

- **access_token:** توکن دسترسی.
- **live_id:** شناسه پخش زنده.
- **comment:** متن نظر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.add_live_comment(
        access_token="token_abc",
        live_id="live_123",
        comment="نظر تستی"
    )
    print(result)

except Exception as e:
    print(e)
```

---

## متدهای بازخورد

<a id="client_feedback_voice_transcription"></a>
### [feedback_voice_transcription](#client_feedback_voice_transcription)

این متد برای ارسال بازخورد برای تبدیل صوت به متن به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام صوتی.
- **feedback_type:** نوع بازخورد. مقادیر قابل قبول: `OK` یا `Incorrect`.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.feedback_voice_transcription(
        chat="u0abc123...",
        message_id="123456",
        feedback_type="OK"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="client-methods" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>