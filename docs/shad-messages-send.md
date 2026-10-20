# ارسال پیام و مدیا

---

<a id="shad_send_message"></a>
## [send_message](#shad_send_message)

این متد اصلی و پایه برای ارسال هر نوع پیام (متن، فایل، مدیا و...) به یک چت است. تمام متدهای ارسال دیگر مانند `send_image`، `send_video` و... در نهایت از این متد استفاده می‌کنند.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد. اگر ورودی این پارامتر برابر با `me` باشد، پیام به پیام‌های ذخیره شده ارسال خواهد شد.
- **text:** متن پیام. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیامی که می‌خواهید به آن ریپلای بزنید. (پیش‌فرض: None)
- **via_bot:** شناسه (GUID) یا نام‌کاربری بات برای ارسال از طریق آن. (پیش‌فرض: None)
- **metadata:** متادیتای اضافی برای قالب‌بندی متن.
- **schedule_time:** زمان‌بندی ارسال پیام. می‌تواند Unix timestamp، timedelta یا datetime باشد.
- **schedule_type:** نوع زمان‌بندی. `Default` یا `WhenOnline` (فقط برای چت کاربر).

**نکات:**

1. برای ارسال زمان‌بندی شده، `schedule_time` باید در آینده باشد.
2. `schedule_type='WhenOnline'` تنها برای چت‌های کاربر قابل استفاده است.

**مثال‌ها:**

ارسال پیام متنی ساده:

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_message("@Online_User", text="سلام! چطوری؟")
    print(result)
```

ارسال پیام با ریپلای:

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_message(
        "u0abc123...",
        text="پاسخ شما",
        reply_to_message_id="123456"
    )
    print(result)
```

ارسال پیام زمان‌بندی شده:

```python
from datetime import timedelta
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_message(
        "https://shad.ir/joing/GROUP123",
        text="این پیام ۱ ساعت دیگر ارسال می‌شود",
        schedule_time=timedelta(hours=1)
    )
    print(result)
```

---

<a id="shad_send_image"></a>
## [send_image](#shad_send_image)

این متد برای ارسال تصویر به یک چت است. این متد از `send_message` با `type='Image'` استفاده می‌کند.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **image:** مسیر فایل تصویر یا داده‌های بایتی.
- **text:** متن همراه تصویر. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **is_spoil:** علامت‌گذاری به عنوان اسپویلر. (پیش‌فرض: False)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **thumb:** تصویر بندانگشتی. (پیش‌فرض: None)
- **width:** عرض سفارشی. (پیش‌فرض: None - تشخیص خودکار)
- **height:** ارتفاع سفارشی. (پیش‌فرض: None - تشخیص خودکار)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.
- **base64:** داده‌های تصویر به صورت base64. (به جای `image`)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_image(
        "https://shad.ir/joinc/CHANNEL123",
        image="photo.jpg",
        text="عکس من"
    )
    print(result)
```

---

<a id="shad_send_video"></a>
## [send_video](#shad_send_video)

این متد برای ارسال ویدئو به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **video:** مسیر فایل ویدئو یا داده‌های بایتی.
- **text:** متن همراه ویدئو. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **is_spoil:** علامت‌گذاری به عنوان اسپویلر. (پیش‌فرض: False)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **thumb:** تصویر بندانگشتی. (پیش‌فرض: None)
- **width:** عرض سفارشی. (پیش‌فرض: None - تشخیص خودکار)
- **height:** ارتفاع سفارشی. (پیش‌فرض: None - تشخیص خودکار)
- **time:** مدت زمان ویدئو به ثانیه. (پیش‌فرض: None - تشخیص خودکار)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.
- **base64:** داده‌های ویدئو به صورت base64. (به جای `video`)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_video(
        "u0abc123...",
        video="video.mp4",
        text="ویدئوی من"
    )
    print(result)
```

---

<a id="shad_send_video_message"></a>
## [send_video_message](#shad_send_video_message)

این متد برای ارسال پیام ویدئویی (ویدئوی گرد) به یک چت است.

**پارامترها:** مشابه `send_video` (به جای `video` از `video_message` استفاده می‌شود).

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_video_message(
        "https://shad.ir/joing/GROUP123",
        video_message="round_video.mp4"
    )
    print(result)
```

---

<a id="shad_send_gif"></a>
## [send_gif](#shad_send_gif)

این متد برای ارسال گیف به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **gif:** مسیر فایل گیف یا داده‌های بایتی.
- **text:** متن همراه گیف. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **thumb:** تصویر بندانگشتی. (پیش‌فرض: None)
- **width:** عرض سفارشی. (پیش‌فرض: None - تشخیص خودکار)
- **height:** ارتفاع سفارشی. (پیش‌فرض: None - تشخیص خودکار)
- **time:** مدت زمان گیف به ثانیه. (پیش‌فرض: None - تشخیص خودکار)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.
- **base64:** داده‌های گیف به صورت base64. (به جای `gif`)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_gif(
        "@Online_User",
        gif="animation.mp4",
        text="گیف بامزه"
    )
    print(result)
```

---

<a id="shad_send_voice"></a>
## [send_voice](#shad_send_voice)

این متد برای ارسال پیام صوتی (ویس) به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **voice:** مسیر فایل صوتی یا داده‌های بایتی.
- **text:** متن همراه ویس. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **time:** مدت زمان ویس به ثانیه. (پیش‌فرض: None - تشخیص خودکار)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.
- **base64:** داده‌های ویس به صورت base64. (به جای `voice`)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_voice(
        "https://shad.ir/joing/GROUP123",
        voice="voice.mp3"
    )
    print(result)
```

---

<a id="shad_send_music"></a>
## [send_music](#shad_send_music)

این متد برای ارسال فایل موسیقی به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **music:** مسیر فایل موسیقی یا داده‌های بایتی.
- **text:** متن همراه موسیقی. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **performer:** نام هنرمند. (پیش‌فرض: None - تشخیص خودکار)
- **time:** مدت زمان آهنگ به ثانیه. (پیش‌فرض: None - تشخیص خودکار)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.
- **base64:** داده‌های موسیقی به صورت base64. (به جای `music`)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_music(
        "me",
        music="song.mp3",
        performer="خواننده مورد علاقه"
    )
    print(result)
```

---

<a id="shad_send_file"></a>
## [send_file](#shad_send_file)

این متد برای ارسال فایل (عمومی) به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **file:** مسیر فایل یا داده‌های بایتی.
- **text:** متن همراه فایل. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.
- **base64:** داده‌های فایل به صورت base64. (به جای `file`)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_file(
        "Online_User",
        file="document.pdf",
        text="فایل مورد نظر"
    )
    print(result)
```

---

<a id="shad_send_sticker"></a>
## [send_sticker](#shad_send_sticker)

این متد برای ارسال استیکر به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **emoji_character:** ایموجی مرتبط با استیکر.
- **sticker_id:** شناسه استیکر.
- **sticker_set_id:** شناسه مجموعه استیکر.
- **file:** دیکشنری داده‌های فایل استیکر.
- **w_h_ratio:** نسبت عرض به ارتفاع. (پیش‌فرض: 1.0)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_sticker(
        "https://shad.ir/joing/GROUP123",
        emoji_character="😊",
        sticker_id="sticker_123",
        sticker_set_id="set_123",
        file={"file_id": "abc", "dc_id": 1, "access_hash_rec": "hash", "mime": "image/webp", "file_name": "sticker.webp", "size": 1234}
    )
    print(result)
```

---

<a id="shad_send_poll"></a>
## [send_poll](#shad_send_poll)

این متد برای ایجاد و ارسال نظرسنجی به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **question:** سوال نظرسنجی. (حداکثر ۲۵۵ کاراکتر)
- **options:** لیست گزینه‌ها. (بین ۲ تا ۱۰ گزینه، هر کدام حداکثر ۱۰۰ کاراکتر)
- **is_anonymous:** ناشناس بودن رای‌ها. (پیش‌فرض: True)
- **multiple_answers:** امکان انتخاب چند گزینه. (پیش‌فرض: False)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_poll(
        "https://shad.ir/joing/GROUP123",
        question="رنگ مورد علاقه شما چیست؟",
        options=["قرمز", "آبی", "سبز", "زرد"],
        is_anonymous=False,
        multiple_answers=True
    )
    print(result)
```

---

<a id="shad_send_quiz"></a>
## [send_quiz](#shad_send_quiz)

این متد برای ایجاد و ارسال آزمون (نظرسنجی با پاسخ صحیح) به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **question:** سوال آزمون. (حداکثر ۲۵۵ کاراکتر)
- **options:** لیست گزینه‌ها. (بین ۲ تا ۱۰ گزینه)
- **correct_option:** ایندکس (عدد) یا متن گزینه صحیح.
- **hint:** راهنمایی برای پاسخ صحیح. (حداکثر ۲۰۰ کاراکتر، پیش‌فرض: None)
- **is_anonymous:** ناشناس بودن پاسخ‌ها. (پیش‌فرض: True)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_quiz(
        "https://shad.ir/joinc/CHANNEL123",
        question="پایتخت ایران کدام است؟",
        options=["تهران", "اصفهان", "شیراز", "تبریز"],
        correct_option="تهران",
        hint="بزرگترین شهر ایران"
    )
    print(result)
```

---

<a id="shad_send_location"></a>
## [send_location](#shad_send_location)

این متد برای ارسال موقعیت مکانی به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **latitude:** عرض جغرافیایی. (عددی بین ۹۰- تا ۹۰)
- **longitude:** طول جغرافیایی. (عددی بین ۱۸۰- تا ۱۸۰)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_location(
        "@Online_User",
        latitude=35.6892,
        longitude=51.3890
    )
    print(result)
```

---

<a id="shad_send_live"></a>
## [send_live](#shad_send_live)

این متد برای ارسال پخش زنده به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **title:** عنوان پخش زنده. (پیش‌فرض: Live stream)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **thumb:** تصویر بندانگشتی. می‌تواند Base64، مسیر فایل، URL یا bytes باشد. (پیش‌فرض: None - تصویر پیش‌فرض)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_live(
        "@TheMAXShad",
        title="پخش زنده تستی"
    )
    print(result)
```

---

<a id="shad_send_message_api_call"></a>
## [send_message_api_call](#shad_send_message_api_call)

این متد برای ارسال پاسخ API Call به دکمه‌های اینلاین یک پیام است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام حاوی دکمه اینلاین.
- **button_id:** شناسه دکمه.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_message_api_call(
        chat="@RubiGuardBot",
        message_id="1499338519906784",
        button_id="101"
    )
    print(result)
```

---

<a id="shad_send_now_scheduled_message"></a>
## [send_now_scheduled_message](#shad_send_now_scheduled_message)

این متد برای ارسال فوری یک پیام زمان‌بندی شده (قبل از موعد مقرر) است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام زمان‌بندی شده.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_now_scheduled_message(
        "@Online_User",
        message_id="123456"
    )
    print(result)
```

---

<a id="shad_send_contact"></a>
## [send_contact](#shad_send_contact)

این متد برای ارسال مخاطب به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID) یا نام‌کاربری کاربر یا بات مقصد. **فقط چت خصوصی** (`u0` یا `b0`) مجاز است.
- **phone_number:** شماره تلفن مخاطب.
- **user:** شناسه (GUID) یا نام‌کاربری کاربر مخاطب. باید `u0` باشد.
- **first_name:** نام مخاطب.
- **last_name:** نام خانوادگی مخاطب. (پیش‌فرض: خالی)
- **vcard:** رشته vCard سفارشی. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.send_contact(
        "u0abc123...",
        phone_number="09123456789",
        user="@Online_User",
        first_name="علی",
        last_name="حسینی"
    )
    print(result)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../shad-methods-messages/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>