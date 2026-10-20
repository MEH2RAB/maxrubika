# سایر متدها

---

## متدهای اصلی و راه‌اندازی

<a id="messenger_connect"></a>
### [connect](#messenger_connect)

برقراری ارتباط با API روبیکا. یک نمونه Api ایجاد می‌کند و اطلاعات نشست ذخیره شده (auth, guid, private_key, user_agent) را در صورت وجود بارگذاری می‌کند.

**خروجی:**

- **Messenger:** نمونه کلاینت با اتصال فعال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    app.connect()
```

---

<a id="messenger_start"></a>
### [start](#messenger_start)

شروع کلاینت، مدیریت احراز هویت و ثبت‌نام.

**پارامترها:**

- **phone_number** (str, optional): شماره تلفن برای ثبت‌نام.

**خروجی:**

- **Messenger:** نمونه کلاینت مقداردهی‌شده.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    app.start("+989123456789")
```

---

<a id="messenger_send_code"></a>
### [send_code](#messenger_send_code)

ارسال کد تأیید به یک شماره تلفن.

**پارامترها:**

- **phone_number** (str): شماره تلفن مقصد.
- **pass_key** (str, optional): رمز عبور حساب (در صورت وجود).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.send_code("+989123456789")
    print(result)
```

---

<a id="messenger_sign_in"></a>
### [sign_in](#messenger_sign_in)

ورود به حساب با استفاده از کد تأیید.

**پارامترها:**

- **phone_number** (str): شماره تلفن.
- **phone_code** (str): کد تأیید.
- **phone_code_hash** (str): هش کد تأیید.
- **public_key** (str): کلید عمومی کلاینت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.sign_in(
        phone_number="+989123456789",
        phone_code="12345",
        phone_code_hash="hash_here",
        public_key="public_key_here"
    )
    print(result)
```

---

<a id="messenger_run"></a>
### [run](#messenger_run)

شروع کلاینت و گوش دادن به به‌روزرسانی‌ها. اطمینان از برقراری اتصال، سپس اجرای اختیاری یک coroutine قبل از ورود به حلقه به‌روزرسانی. هم در محیط‌های sync و هم async کار می‌کند.

**پارامترها:**

- **coroutine** (Coroutine, optional): Coroutine اختیاری برای اجرا قبل از گوش دادن به به‌روزرسانی‌ها.

**خروجی:**

- **None:** در حالت عادی تا زمانی که متوقف نشود، اجرا می‌شود.

**مثال sync:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    app.run()
```

**مثال async:**

```python
from maxrubika import Messenger

async with Messenger("mySession") as app:
    await app.run()
```

---

<a id="messenger_disconnect"></a>
### [disconnect](#messenger_disconnect)

قطع ارتباط با سرور روبیکا (نسخه sync). این متد در واقع متد `close` را در پس‌زمینه فراخوانی می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    app.start()
    # ... انجام عملیات ...
    app.disconnect()
```

---

<a id="messenger_close"></a>
### [close](#messenger_close)

بستن اتصال به سرور (نسخه async). این متد معادل async متد `disconnect` است.

**نکته:** برای قطع ارتباط در محیط async از این متد استفاده کنید. برای محیط sync از `disconnect` استفاده کنید.

**مثال:**

```python
from maxrubika import Messenger

async with Messenger("mySession") as app:
    await app.close()
```

---

<a id="messenger_get_string_session"></a>
### [get_string_session](#messenger_get_string_session)

خروجی گرفتن از نشست فعلی به صورت یک StringSession رمزنگاری‌شده.

**پارامترها:**

- **password** (str, optional): رمز اختیاری برای رمزنگاری. در صورت ارائه، StringSession فقط با همین رمز باز می‌شود.

**خروجی:**

- **str:** StringSession رمزنگاری‌شده که می‌توان بعداً با `Messenger(string_session=..., password=...)` استفاده کرد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    string_session = app.get_string_session()
    print(string_session)
```

---

## متدهای دریافت به‌روزرسانی

<a id="messenger_get_updates"></a>
### [get_updates](#messenger_get_updates)

دریافت به‌روزرسانی‌ها از WebSocket روبیکا.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    # این متد به صورت نامحدود اجرا می‌شود و به‌روزرسانی‌ها را دریافت می‌کند
    app.get_updates()
```

---

## متدهای درخواست

<a id="messenger_request"></a>
### [request](#messenger_request)

ساخت و ارسال درخواست به API روبیکا.

**پارامترها:**

- **method** (str): نام متد API (مانند 'sendMessage', 'getUserInfo').
- **input** (dict, optional): داده‌های ورودی برای متد.
- **tmp_session** (bool): استفاده از نشست موقت به جای auth (پیش‌فرض: False). در صورت True بودن، اگر کلاینت متصل نباشد، خودکار متصل می‌شود.
- **encrypt** (bool): رمزگذاری داده‌های درخواست (پیش‌فرض: True).

**خروجی:**

- **Data or None:** پاسخ API.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.request(
        method="getUserInfo",
        input={"user_guid": "u0abc123..."}
    )
    print(result)
```

---

## متدهای فایل

<a id="messenger_upload_file"></a>
### [upload_file](#messenger_upload_file)

آپلود فایل به روبیکا.

**پارامترها:**

- **file** (str or bytes or None): مسیر فایل، bytes، یا URL برای آپلود.
- **base64_data** (str, optional): داده‌های فایل به صورت base64.
- **mime** (str, optional): نوع MIME فایل.
- **file_name** (str, optional): نام فایل.
- **chunk** (int, optional): اندازه هر بخش به بایت (پیش‌فرض: 1MB).
- **callback** (callable, optional): تابع پیشرفت آپلود (total_size, uploaded_bytes).

**نکته:** باید یا `file` یا `base64_data` ارسال شود.

**خروجی:**

- متادیتای فایل آپلود شده شامل mime, size, dc_id, file_id, file_name, access_hash_rec.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.upload_file(
        file="file.jpg",
        mime="image/jpeg",
        file_name="my_image.jpg"
    )
    print(result)
```

---

<a id="messenger_download_file"></a>
### [download_file](#messenger_download_file)

دانلود فایل از سرورهای روبیکا با استفاده از شناسه فایل و access hash.

**پارامترها:**

- **file_inline:** دیکشنری حاوی اطلاعات فایل (dc_id, file_id, access_hash_rec, size, file_name).
- **dc_id** (int, optional): شناسه دیتاسنتر (در صورت عدم ارسال file_inline).
- **file_id** (int, optional): شناسه یکتای فایل.
- **access_hash** (str, optional): هش دسترسی مرتبط با فایل.
- **size** (int, optional): اندازه کل فایل به بایت.
- **chunk** (int, optional): اندازه هر بخش دانلود (پیش‌فرض: 131072).
- **callback** (callable, optional): تابع پیشرفت دانلود (total_size, downloaded_size).
- **gather** (bool, optional): دانلود بخش‌ها به صورت موازی (پیش‌فرض: False).
- **save_as** (str or bool, optional): مسیر دایرکتوری یا True برای دایرکتوری جاری. اگر None باشد، بایت‌ها را برمی‌گرداند.
- **file_name** (str, optional): نام سفارشی فایل.
- **as_base64** (bool, optional): بازگرداندن فایل به صورت base64 (پیش‌فرض: False).

**خروجی:**

- **bytes, str, or Data:** محتوای فایل (bytes)، رشته base64 یا Data (زمانی که save_as استفاده می‌شود).

**مثال‌ها:**

۱. دانلود با file_inline:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.download_file(
        file_inline={"dc_id": 1, "file_id": 123456, "access_hash_rec": "hash_example", "size": 1024000},
        save_as=True,
        file_name="my_file.jpg"
    )
    print(result)
```

۲. دانلود با پارامترهای جداگانه و دریافت bytes:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.download_file(
        dc_id=1,
        file_id=123456,
        access_hash="hash_example",
        size=1024000
    )
    print(result)
```

---

## متدهای کمکی

<a id="messenger_get_time"></a>
### [get_time](#messenger_get_time)

این متد برای دریافت زمان فعلی سرور به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    time = app.get_time()
    print(time)
```

---

<a id="messenger_get_available_reactions"></a>
### [get_available_reactions](#messenger_get_available_reactions)

این متد برای دریافت لیست ری‌اکشن‌های قابل استفاده در چت‌ها به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    reactions = app.get_available_reactions()
    print(reactions)
```

---

<a id="messenger_get_location_view"></a>
### [get_location_view](#messenger_get_location_view)

این متد برای دریافت نقشه یک موقعیت جغرافیایی به کار می‌رود.

**پارامترها:**

- **latitude:** عرض جغرافیایی. (عددی بین ۹۰- تا ۹۰)
- **longitude:** طول جغرافیایی. (عددی بین ۱۸۰- تا ۱۸۰)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    view = app.get_location_view(latitude=35.6892, longitude=51.3890)
    print(view)
```

---

<a id="messenger_set_current_live_location"></a>
### [set_current_live_location](#messenger_set_current_live_location)

این متد برای تنظیم موقعیت زنده فعلی به کار می‌رود.

**پارامترها:**

- **longitude:** طول جغرافیایی.
- **latitude:** عرض جغرافیایی.
- **tile_side_count:** تعداد تایل‌ها در هر ضلع.
- **tile_urls:** لیست URLهای تایل‌های نقشه.
- **x_loc:** موقعیت X روی نقشه.
- **y_loc:** موقعیت Y روی نقشه.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.set_current_live_location(
        longitude=51.3890,
        latitude=35.6892,
        tile_side_count=1,
        tile_urls=["https://..."],
        x_loc=0.5,
        y_loc=0.5
    )
    print(result)
```

---

<a id="messenger_get_wallpapers"></a>
### [get_wallpapers](#messenger_get_wallpapers)

این متد برای دریافت تنظیمات فعلی تصویر پس‌زمینه چت به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    wallpapers = app.get_wallpapers()
    print(wallpapers)
```

---

<a id="messenger_reset_wallpapers"></a>
### [reset_wallpapers](#messenger_reset_wallpapers)

این متد برای بازنشانی تمام تصاویر پس‌زمینه چت‌ها به حالت پیش‌فرض به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.reset_wallpapers()
    print(result)
```

---

<a id="messenger_get_link_from_app_url"></a>
### [get_link_from_app_url](#messenger_get_link_from_app_url)

این متد برای دریافت لینک مستقیم از یک URL اپلیکیشن به کار می‌رود.

**پارامتر:**

- **url:** URL اپلیکیشن برای استخراج لینک.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.get_link_from_app_url("https://...")
    print(result)
```

---

<a id="messenger_get_wallet_transaction_message"></a>
### [get_wallet_transaction_message](#messenger_get_wallet_transaction_message)

این متد برای دریافت پیام مرتبط با یک تراکنش کیف پول به کار می‌رود.

**پارامترها:**

- **transfer_id:** شناسه تراکنش کیف پول.
- **access_transfer:** هش دسترسی تراکنش.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.get_wallet_transaction_message(
        transfer_id="transfer_123",
        access_transfer="access_hash_here"
    )
    print(result)
```

---

## متدهای استیکر

<a id="messenger_get_sticker_setting"></a>
### [get_sticker_setting](#messenger_get_sticker_setting)

این متد برای دریافت تنظیمات استیکر کاربر فعلی به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    settings = app.get_sticker_setting()
    print(settings)
```

---

<a id="messenger_get_my_sticker_sets"></a>
### [get_my_sticker_sets](#messenger_get_my_sticker_sets)

این متد برای دریافت مجموعه استیکرهای متعلق به کاربر به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    stickers = app.get_my_sticker_sets()
    print(stickers)
```

---

<a id="messenger_get_my_archived_sticker_sets"></a>
### [get_my_archived_sticker_sets](#messenger_get_my_archived_sticker_sets)

این متد برای دریافت مجموعه استیکرهای آرشیو شده کاربر به کار می‌رود.

**پارامتر:**

- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    archived = app.get_my_archived_sticker_sets()
    print(archived)
```

---

<a id="messenger_get_sticker_set_by_id"></a>
### [get_sticker_set_by_id](#messenger_get_sticker_set_by_id)

این متد برای دریافت یک مجموعه استیکر با شناسه آن به کار می‌رود.

**پارامتر:**

- **sticker_set_id:** شناسه مجموعه استیکر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    sticker_set = app.get_sticker_set_by_id("sticker_set_id_123")
    print(sticker_set)
```

---

<a id="messenger_get_stickers_by_set_ids"></a>
### [get_stickers_by_set_ids](#messenger_get_stickers_by_set_ids)

این متد برای دریافت استیکرها با شناسه مجموعه‌های آن‌ها به کار می‌رود.

**پارامتر:**

- **sticker_set_ids:** یک شناسه یا لیستی از شناسه‌های مجموعه استیکر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    stickers = app.get_stickers_by_set_ids(["id1", "id2", "id3"])
    print(stickers)
```

---

<a id="messenger_get_stickers_by_emoji"></a>
### [get_stickers_by_emoji](#messenger_get_stickers_by_emoji)

این متد برای دریافت استیکرها بر اساس ایموجی به کار می‌رود.

**پارامترها:**

- **emoji:** کاراکتر ایموجی.
- **suggest_by:** نوع پیشنهاد. (پیش‌فرض: All)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    stickers = app.get_stickers_by_emoji("😊")
    print(stickers)
```

---

<a id="messenger_search_stickers"></a>
### [search_stickers](#messenger_search_stickers)

این متد برای جستجوی استیکرها به کار می‌رود.

**پارامترها:**

- **search_text:** متن جستجو. (پیش‌فرض: خالی)
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    results = app.search_stickers(search_text="سلام")
    print(results)
```

---

<a id="messenger_get_trend_sticker_sets"></a>
### [get_trend_sticker_sets](#messenger_get_trend_sticker_sets)

این متد برای دریافت مجموعه استیکرهای پرطرفدار به کار می‌رود.

**پارامتر:**

- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    trending = app.get_trend_sticker_sets()
    print(trending)
```

---

<a id="messenger_add_sticker_set"></a>
### [add_sticker_set](#messenger_add_sticker_set)

این متد برای افزودن یک مجموعه استیکر به مجموعه‌های کاربر به کار می‌رود.

**پارامتر:**

- **sticker_set_id:** شناسه مجموعه استیکر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.add_sticker_set("sticker_set_id_123")
    print(result)
```

---

<a id="messenger_delete_sticker_set"></a>
### [delete_sticker_set](#messenger_delete_sticker_set)

این متد برای حذف یک مجموعه استیکر از مجموعه‌های کاربر به کار می‌رود.

**پارامتر:**

- **sticker_set_id:** شناسه مجموعه استیکر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.delete_sticker_set("sticker_set_id_123")
    print(result)
```

---

<a id="messenger_archive_sticker_set"></a>
### [archive_sticker_set](#messenger_archive_sticker_set)

این متد برای آرشیو کردن یک مجموعه استیکر به کار می‌رود.

**پارامتر:**

- **sticker_set_id:** شناسه مجموعه استیکر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.archive_sticker_set("sticker_set_id_123")
    print(result)
```

---

<a id="messenger_reorder_sticker_sets"></a>
### [reorder_sticker_sets](#messenger_reorder_sticker_sets)

این متد برای تغییر ترتیب مجموعه استیکرها در مجموعه کاربر به کار می‌رود.

**پارامتر:**

- **ordered_sticker_set_ids:** یک شناسه یا لیستی از شناسه‌های مجموعه استیکر به ترتیب دلخواه.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.reorder_sticker_sets(["id3", "id1", "id2"])
    print(result)
```

---

## متدهای گیف

<a id="messenger_get_my_gif_set"></a>
### [get_my_gif_set](#messenger_get_my_gif_set)

این متد برای دریافت مجموعه گیف‌های شخصی کاربر به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    gifs = app.get_my_gif_set()
    print(gifs)
```

---

<a id="messenger_add_to_my_gif_set"></a>
### [add_to_my_gif_set](#messenger_add_to_my_gif_set)

این متد برای افزودن یک گیف به مجموعه گیف‌های شخصی کاربر به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت حاوی گیف.
- **message_id:** شناسه پیام گیف.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.add_to_my_gif_set("g0abc123...", message_id="123456")
    print(result)
```

---

<a id="messenger_delete_my_gif_set"></a>
### [delete_my_gif_set](#messenger_delete_my_gif_set)

این متد برای حذف یک گیف از مجموعه گیف‌های شخصی کاربر به کار می‌رود.

**پارامتر:**

- **file_id:** شناسه فایل گیف.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.delete_my_gif_set("file_id_123")
    print(result)
```

---

<a id="messenger_delete_all_my_gif_set"></a>
### [delete_all_my_gif_set](#messenger_delete_all_my_gif_set)

این متد برای حذف تمام گیف‌ها از مجموعه گیف‌های شخصی کاربر به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.delete_all_my_gif_set()
    print(result)
```

---

## متدهای پخش زنده

<a id="messenger_get_live_status"></a>
### [get_live_status](#messenger_get_live_status)

این متد برای دریافت وضعیت یک پخش زنده به کار می‌رود.

**پارامترها:**

- **live_id:** شناسه پخش زنده.
- **access_token:** توکن دسترسی دریافت‌شده از پاسخ send_live.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    status = app.get_live_status(live_id="live_123", access_token="token_abc")
    print(status)
```

---

<a id="messenger_get_live_comments"></a>
### [get_live_comments](#messenger_get_live_comments)

این متد برای دریافت نظرات یک پخش زنده به کار می‌رود.

**پارامترها:**

- **live_id:** شناسه پخش زنده.
- **access_token:** توکن دسترسی.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    comments = app.get_live_comments(live_id="live_123", access_token="token_abc")
    print(comments)
```

---

<a id="messenger_get_live_play_url"></a>
### [get_live_play_url](#messenger_get_live_play_url)

این متد برای دریافت URL پخش یک لایو به کار می‌رود.

**پارامترها:**

- **access_token:** توکن دسترسی.
- **live_id:** شناسه پخش زنده.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    url = app.get_live_play_url(access_token="token_abc", live_id="live_123")
    print(url)
```

---

<a id="messenger_add_live_comment"></a>
### [add_live_comment](#messenger_add_live_comment)

این متد برای افزودن نظر به یک پخش زنده به کار می‌رود.

**پارامترها:**

- **access_token:** توکن دسترسی.
- **live_id:** شناسه پخش زنده.
- **comment:** متن نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.add_live_comment(
        access_token="token_abc",
        live_id="live_123",
        comment="نظر تستی"
    )
    print(result)
```

---

<a id="messenger_report_live"></a>
### [report_live](#messenger_report_live)

این متد برای گزارش یک پخش زنده به کار می‌رود.

**پارامترها:**

- **live_id:** شناسه پخش زنده برای گزارش.
- **report_type:** دلیل گزارش. می‌تواند:
  - عدد بین ۱۰۰ تا ۱۰۶
  - نام رشته‌ای (بدون حساسیت به حروف بزرگ/کوچک): `Other`، `Violence`، `Spam`، `Porn`، `ChildAbuse`، `Copyright`، `Fraud`
- **description:** توضیحات گزارش. **الزامی** وقتی `report_type` برابر ۱۰۰ (Other) باشد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.report_live(
        live_id="live_123",
        report_type="Spam"
    )
    print(result)
```

---

## متدهای بازخورد

<a id="messenger_feedback_voice_transcription"></a>
### [feedback_voice_transcription](#messenger_feedback_voice_transcription)

این متد برای ارسال بازخورد برای تبدیل صوت به متن به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام صوتی.
- **feedback_type:** نوع بازخورد. مقادیر قابل قبول: `OK` یا `Incorrect`.
- **feedback_text:** متن بازخورد. (اختیاری - در صورت عدم ارسال، از متن تبدیل‌شده استفاده می‌شود)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    result = app.feedback_voice_transcription(
        chat="u0abc123...",
        message_id="123456",
        feedback_type="OK"
    )
    print(result)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>