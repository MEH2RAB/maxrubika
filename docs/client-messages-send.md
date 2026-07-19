# ارسال پیام و مدیا

---

<a id="client_send_message"></a>
## [send_message](#client_send_message)

این متد اصلی و پایه برای ارسال هر نوع پیام (متن، فایل، مدیا و...) به یک چت است. تمام متدهای ارسال دیگر مانند `send_image`، `send_video` و... در نهایت از این متد استفاده می‌کنند.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد. اگر ورودی این پارامتر برابر با `me` باشد، پیام به پیام‌های ذخیره شده ارسال خواهد شد.
- **text:** متن پیام. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیامی که می‌خواهید به آن ریپلای بزنید. (پیش‌فرض: None)
- **via_bot:** شناسه (GUID) یا نام‌کاربری بات برای ارسال از طریق آن. (پیش‌فرض: None)
- **auto_delete:** مدت زمان حذف خودکار پیام به ثانیه. (پیش‌فرض: None)
- **metadata:** متادیتای اضافی برای قالب‌بندی متن.
- **schedule_time:** زمان‌بندی ارسال پیام. می‌تواند Unix timestamp، timedelta یا datetime باشد.
- **schedule_type:** نوع زمان‌بندی. `Default` یا `WhenOnline` (فقط برای چت کاربر).

**نکات:**

1. برای ارسال زمان‌بندی شده، `schedule_time` باید در آینده باشد.
2. `schedule_type='WhenOnline'` تنها برای چت‌های کاربر قابل استفاده است.

**مثال‌ها:**

ارسال پیام متنی ساده:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_message("u0abc123...", text="سلام! چطوری؟")
    print(result)

except Exception as e:
    print(e)
```

ارسال پیام با ریپلای:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_message(
        "u0abc123...",
        text="پاسخ شما",
        reply_to_message_id="123456"
    )
    print(result)

except Exception as e:
    print(e)
```

ارسال پیام زمان‌بندی شده:

```python
from datetime import timedelta
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_message(
        "u0abc123...",
        text="این پیام ۱ ساعت دیگر ارسال می‌شود",
        schedule_time=timedelta(hours=1)
    )
    print(result)

except Exception as e:
    print(e)
```

ارسال پیام با حذف خودکار:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_message(
        "u0abc123...",
        text="این پیام ۶۰ ثانیه دیگر حذف می‌شود",
        auto_delete=60
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_image"></a>
## [send_image](#client_send_image)

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
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_image(
        "u0abc123...",
        image="photo.jpg",
        text="عکس من"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_video"></a>
## [send_video](#client_send_video)

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
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_video(
        "u0abc123...",
        video="video.mp4",
        text="ویدئوی من"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_video_message"></a>
## [send_video_message](#client_send_video_message)

این متد برای ارسال پیام ویدئویی (ویدئوی گرد) به یک چت است.

**پارامترها:** مشابه `send_video`.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_video_message(
        "u0abc123...",
        video_message="round_video.mp4"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_gif"></a>
## [send_gif](#client_send_gif)

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
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_gif(
        "u0abc123...",
        gif="animation.mp4",
        text="گیف بامزه"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_voice"></a>
## [send_voice](#client_send_voice)

این متد برای ارسال پیام صوتی (ویس) به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **voice:** مسیر فایل صوتی یا داده‌های بایتی.
- **text:** متن همراه ویس. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **time:** مدت زمان ویس به ثانیه. (پیش‌فرض: None - تشخیص خودکار)
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_voice(
        "u0abc123...",
        voice="voice.mp3"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_music"></a>
## [send_music](#client_send_music)

این متد برای ارسال فایل موسیقی به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **music:** مسیر فایل موسیقی یا داده‌های بایتی.
- **text:** متن همراه موسیقی. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **performer:** نام هنرمند. (پیش‌فرض: None - تشخیص خودکار)
- **time:** مدت زمان آهنگ به ثانیه. (پیش‌فرض: None - تشخیص خودکار)
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_music(
        "me",
        music="song.mp3",
        performer="خواننده مورد علاقه"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_file"></a>
## [send_file](#client_send_file)

این متد برای ارسال فایل (عمومی) به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **file:** مسیر فایل یا داده‌های بایتی.
- **text:** متن همراه فایل. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **via_bot:** ارسال از طریق بات. (پیش‌فرض: None)
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_file(
        "Online_User",
        file="document.pdf",
        text="فایل مورد نظر"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_sticker"></a>
## [send_sticker](#client_send_sticker)

این متد برای ارسال استیکر به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **emoji_character:** ایموجی مرتبط با استیکر.
- **sticker_id:** شناسه استیکر.
- **sticker_set_id:** شناسه مجموعه استیکر.
- **file:** دیکشنری داده‌های فایل استیکر.
- **w_h_ratio:** نسبت عرض به ارتفاع. (پیش‌فرض: 1.0)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)
- **schedule_time:** زمان‌بندی ارسال.
- **schedule_type:** نوع زمان‌بندی.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_sticker(
        "g0abc123...",
        emoji_character="😊",
        sticker_id="sticker_123",
        sticker_set_id="set_123",
        file={"file_id": "abc", "dc_id": 1, "access_hash_rec": "hash", "mime": "image/webp", "file_name": "sticker.webp", "size": 1234}
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_poll"></a>
## [send_poll](#client_send_poll)

این متد برای ایجاد و ارسال نظرسنجی به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **question:** سوال نظرسنجی. (حداکثر ۲۵۵ کاراکتر)
- **options:** لیست گزینه‌ها. (بین ۲ تا ۱۰ گزینه، هر کدام حداکثر ۱۰۰ کاراکتر)
- **is_anonymous:** ناشناس بودن رای‌ها. (پیش‌فرض: True)
- **multiple_answers:** امکان انتخاب چند گزینه. (پیش‌فرض: False)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_poll(
        "g0abc123...",
        question="رنگ مورد علاقه شما چیست؟",
        options=["قرمز", "آبی", "سبز", "زرد"],
        is_anonymous=False,
        multiple_answers=True
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_quiz"></a>
## [send_quiz](#client_send_quiz)

این متد برای ایجاد و ارسال آزمون (نظرسنجی با پاسخ صحیح) به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **question:** سوال آزمون. (حداکثر ۲۵۵ کاراکتر)
- **options:** لیست گزینه‌ها. (بین ۲ تا ۱۰ گزینه)
- **correct_option:** ایندکس (عدد) یا متن گزینه صحیح.
- **hint:** راهنمایی برای پاسخ صحیح. (حداکثر ۲۰۰ کاراکتر، پیش‌فرض: None)
- **is_anonymous:** ناشناس بودن پاسخ‌ها. (پیش‌فرض: True)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **auto_delete:** مدت زمان حذف خودکار به ثانیه. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_quiz(
        "g0abc123...",
        question="پایتخت ایران کدام است؟",
        options=["تهران", "اصفهان", "شیراز", "تبریز"],
        correct_option="تهران",
        hint="بزرگترین شهر ایران"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_location"></a>
## [send_location](#client_send_location)

این متد برای ارسال موقعیت مکانی به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **latitude:** عرض جغرافیایی. (عددی بین ۹۰- تا ۹۰)
- **longitude:** طول جغرافیایی. (عددی بین ۱۸۰- تا ۱۸۰)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_location(
        "@Online_User",
        latitude=35.6892,
        longitude=51.3890
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_live"></a>
## [send_live](#client_send_live)

این متد برای ارسال پخش زنده به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **title:** عنوان پخش زنده. (پیش‌فرض: Live stream)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)
- **thumbnail:** تصویر بندانگشتی به صورت Base64. (پیش‌فرض: None - تصویر پیش‌فرض)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_live(
        "@TheMAXRubika",
        title="پخش زنده تستی"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_message_api_call"></a>
## [send_message_api_call](#client_send_message_api_call)

این متد برای ارسال پاسخ API Call به دکمه‌های اینلاین یک پیام است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام حاوی دکمه اینلاین.
- **button_id:** شناسه دکمه.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_message_api_call(
        chat="@RubiGuardBot",
        message_id="1499338519906784",
        button_id="101"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_rubino_post"></a>
## [send_rubino_post](#client_send_rubino_post)

این متد برای ارسال یک پست روبینو به چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **post_id:** شناسه پست.
- **post_profile_id:** شناسه پروفایل پست.
- **is_mute:** ارسال بی‌صدا بدون اعلان. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_rubino_post(
        "u0abc123...",
        post_id="post_123",
        post_profile_id="profile_123"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_rubino_story"></a>
## [send_rubino_story](#client_send_rubino_story)

این متد برای ارسال پاسخ یا پیام مستقیم به استوری روبینو است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **story_id:** شناسه استوری.
- **story_profile_id:** شناسه پروفایل استوری.
- **reply_text:** متن پاسخ. (پیش‌فرض: خالی)
- **type:** نوع ارسال. `Reply` یا `Direct`. (پیش‌فرض: Reply)
- **is_mute:** ارسال بی‌صدا بدون اعلان. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_rubino_story(
        "u0abc123...",
        story_id="story_123",
        story_profile_id="profile_123",
        reply_text="استوری قشنگی بود!"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_now_scheduled_message"></a>
## [send_now_scheduled_message](#client_send_now_scheduled_message)

این متد برای ارسال فوری یک پیام زمان‌بندی شده (قبل از موعد مقرر) است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت.
- **message_id:** شناسه پیام زمان‌بندی شده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_now_scheduled_message(
        "u0abc123...",
        message_id="123456"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_send_contact"></a>
## [send_contact](#client_send_contact)

این متد برای ارسال مخاطب به یک چت است.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری چت مقصد.
- **phone_number:** شماره تلفن مخاطب.
- **first_name:** نام مخاطب.
- **last_name:** نام خانوادگی مخاطب. (پیش‌فرض: خالی)
- **reply_to_message_id:** شناسه پیام برای ریپلای. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.send_contact(
        "u0abc123...",
        phone_number="09123456789",
        first_name="علی",
        last_name="حسینی"
    )
    print(result)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="client-methods-messages" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>