# توضیحات بیشتر

---

<a id="bot_chat_id_guide"></a>
## [راهنمای شناسه‌های گفتگو (Chat ID)](#bot_chat_id_guide)

شناسه‌های گفتگو در پلتفرم روبیکا از قاعده‌ی مشخصی پیروی می‌کنند که آگاهی از آن برای عملکرد صحیح بات ضروری است:

| نوع گفتگو | پیشوند | طول | مثال |
|------|------|------|------|
| گروه | g0 | ۳۲ کاراکتر | g0G3R190567fa33c5f5ee7d399a104e8 |
| کانال | c0 | ۳۲ کاراکتر | c0Hzgbk0ac24729c1d1a5d55c26ac3ef |
| گفتگوی خصوصی | b0 | ۳۲ کاراکتر | b0Hzgbk0ac24729c1d1a5d55c29ac5ag |

### نکات کلیدی:

1. **تمایز شناسه‌ها:** شناسهٔ فرستنده (Sender ID) که با u0 شروع می‌شود، کاملاً با شناسهٔ گفتگوی خصوصی کاربر (b0) متفاوت است. این دو را هرگز با یکدیگر اشتباه نگیرید.
2. **ماهیت پویای شناسهٔ خصوصی:** شناسهٔ گفتگوی خصوصی (b0) برای هر بات منحصربه‌فرد است. به عبارت دیگر، شناسه‌ای که از بات A دریافت می‌کنید، در بات B قابل استفاده نخواهد بود.
3. **تمایز از GUID:** شناسهٔ گفتگو را با GUID (گوید) اشتباه نگیرید. اگرچه از نظر ظاهری مشابه هستند، اما کاربردهای کاملاً متفاوتی دارند:
    - **GUID:** در کلاینت و سرورهای پیام‌رسان مورد استفاده قرار می‌گیرد.
    - **Chat ID:** مختص سرور بات است و برای ارتباط با API استفاده می‌شود.

---

<a id="bot_init_params"></a>
## [راهنمای ساخت و پیکربندی بات](#bot_init_params)

هنگام ساخت نمونه ربات، می‌توانید پارامترهای زیر را به سازنده کلاس `Bot` بدهید:

| پارامتر | نوع | پیش‌فرض | توضیح |
|------|------|:------:|------|
| `token` | str | `None` | توکن احراز هویت بات. اگر خالی یا نامعتبر باشد، از کاربر در ترمینال درخواست می‌شود. |
| `token_string` | str | `None` | نسخهٔ رمزنگاری‌شدهٔ توکن. **اولویت آن از `token` بیشتر است.** |
| `password` | str | `None` | رمز عبور برای رمزگشایی `token_string` (در صورت استفاده). |
| `base_url` | str | `"https://botapi.rubika.ir/v3"` | آدرس پایهٔ API. |
| `timeout` | int/float | `30` | مدت زمان انتظار برای هر درخواست (ثانیه). |
| `max_retries` | int | `5` | حداکثر تعداد تلاش مجدد در صورت خطای شبکه. |
| `show_welcome` | bool | `True` | نمایش پیام خوش‌آمدگویی کتابخانه هنگام راه‌اندازی. |
| `run_all_handlers` | bool | `True` | اگر `True` باشد، همهٔ هندلرهایی که شرطشان با رویداد مطابقت دارد اجرا می‌شوند. اگر `False` باشد، تنها اولین هندلر مطابق اجرا می‌شود. |

**نکات مهم:**

1. **اولویت `token_string`:** اگر هم `token` و هم `token_string` را بدهید، `token_string` استفاده می‌شود (و در صورت نیاز با `password` رمزگشایی می‌شود).
2. **`run_all_handlers`:** اگر چند هندلر با یک رویداد مطابقت داشته باشند، با `True` همه اجرا می‌شوند و با `False` فقط اولی.

---

<a id="bot_token_string"></a>
## [توکن استرینگ (TokenString) و امنیت آن](#bot_token_string)

توکن بات یکی از حساس‌ترین اطلاعات پروژه است. اگر توکن شما به دست شخص دیگری بیفتد، می‌تواند از طرف بات شما به کاربران پیام بفرستد، اطلاعات گروه‌ها را بخواند یا حتی بات را مختل کند.

**TokenString** یک راهکار امنیتی برای ذخیره و انتقال توکن است. این قابلیت توکن خام بات را به یک رشتهٔ رمزنگاری‌شده تبدیل می‌کند و می‌توانید آن را جای توکن اصلی استفاده کنید.

### مزایای امنیتی TokenString:

1. **رمزنگاری:** توکن اصلی بات هرگز به‌صورت متن ساده ذخیره یا ارسال نمی‌شود.
2. **رمز عبور اختیاری:** می‌توانید TokenString را با یک رمز عبور محافظت کنید. در این صورت، حتی اگر رشتهٔ رمزنگاری‌شده لو برود، بدون رمز عبور قابل استفاده نیست.
3. **دور ماندن از مخازن:** می‌توانید TokenString را در فایل‌های تنظیمات، متغیرهای محیطی یا مخزن کد قرار دهید بدون نگرانی از افشای توکن اصلی.
4. **چرخش توکن:** در صورت نیاز، می‌توانید TokenString جدید بسازید بدون اینکه توکن اصلی بات تغییر کند.

### ساخت TokenString از توکن فعلی:

با متد `get_token_string()` می‌توانید توکن فعلی بات را به یک TokenString رمزنگاری‌شده تبدیل کنید:

```python
from maxrubika import Bot

with Bot("TOKEN") as bot:
    # بدون رمز عبور
    token_string = bot.get_token_string()

    # با رمز عبور (امن‌تر)
    token_string = bot.get_token_string(password="my_secret_password")

    print(token_string)
```

### استفاده از TokenString برای ساخت ربات:

```python
from maxrubika import Bot

with Bot(token_string="ENCRYPTED_STRING", password="my_secret_password") as bot:
    print(bot.get_me())
```

**پارامترهای `get_token_string`:**

| پارامتر | نوع | پیش‌فرض | توضیح |
|------|------|:------:|------|
| `password` | str | `None` | رمز عبور اختیاری برای رمزنگاری. اگر بدهید، TokenString فقط با همین رمز قابل باز شدن است. |

**نکات مهم:**

1. اگر TokenString را با رمز عبور بسازید، **حتماً رمز را جای امنی نگه دارید.** بدون آن، TokenString قابل بازیابی نیست.
2. TokenString در واقع توکن اصلی نیست، بلکه یک نسخهٔ رمزنگاری‌شده است. توکن اصلی همچنان در سمت سرور روبیکا معتبر است.

---

<a id="bot_connect_disconnect"></a>
## [نحوه اتصال و قطع اتصال](#bot_connect_disconnect)

برای برقراری و قطع اتصال در کتابخانه MAXRubika، دو روش اصلی وجود دارد که بسته به نوع استفاده (Sync یا Async) و نیاز پروژه، می‌توانید یکی را انتخاب کنید.

### روش اول: استفاده از Context Manager

در این روش نیازی به صدا زدن متد اضافه‌ای برای قطع اتصال نیست؛ کافی است از `with` (در حالت Sync) یا `async with` (در حالت Async) استفاده کنید. اتصال به‌صورت خودکار برقرار می‌شود و در پایان بلوک، به‌درستی بسته خواهد شد.

#### حالت Sync:

```python
from maxrubika import Bot

with Bot("Token") as bot:
    me = bot.get_me()
    print(me)
```

همچنین می‌توانید ابتدا شیء را بسازید و سپس از `with` استفاده کنید:

```python
from maxrubika import Bot

bot = Bot("Token")

with bot:
    me = bot.get_me()
    print(me)
```

#### حالت Async:

```python
import asyncio
from maxrubika import Bot

async def main():
    async with Bot("Token") as bot:
        me = await bot.get_me()
        print(me)

asyncio.run(main())
```

یا ساخت جداگانه‌ی شیء و سپس استفاده از `async with`:

```python
import asyncio
from maxrubika import Bot

async def main():
    bot = Bot("Token")

    async with bot:
        me = await bot.get_me()
        print(me)

asyncio.run(main())
```

### روش دوم: صدا زدن متد disconnect یا close

در این روش، خودتان به‌صورت دستی اتصال را برقرار می‌کنید و در انتهای عملیات، با صدا زدن متد مناسب، اتصال را می‌بندید.

#### حالت Sync:

در کدهای Sync از متد `disconnect` استفاده کنید:

```python
from maxrubika import Bot

bot = Bot("Token")

me = bot.get_me()
print(me)

bot.disconnect()  # قطع اتصال در پایان عملیات
```

#### حالت Async:

در کدهای Async از متد `close` استفاده کنید:

```python
import asyncio
from maxrubika import Bot

async def main():
    bot = Bot("Token")
    me = await bot.get_me()
    print(me)
    await bot.close()  # قطع اتصال در پایان عملیات

asyncio.run(main())
```

**نکته مهم:**

استفاده از این روش‌ها فقط زمانی لازم است که بخواهید یک عملیات موقت با کتابخانه انجام دهید (مثلاً دریافت اطلاعات یک‌باره‌ی یک شیء).

اگر از دکوراتورها، لانگ‌پولینگ یا وب‌هوک استفاده می‌کنید، نیازی به صدا زدن `disconnect` یا `close` یا استفاده از Context Manager نیست؛ زیرا کتابخانه خودش مدیریت اتصال را در طول اجرا به عهده دارد.

#### مثال: استفاده از دکوراتور (بدون نیاز به قطع دستی)

```python
from maxrubika import Bot

bot = Bot("Token")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("سلام، پیام شما دریافت شد.")

bot.run()
```

در این حالت، کتابخانه به‌طور خودکار اتصال را در طول اجرای ربات مدیریت می‌کند و نیازی به فراخوانی متدهای `disconnect` یا `close` نخواهد بود.

---

<a id="bot_metadata_guide"></a>
## [راهنمای متادیتا در متن پیام](#bot_metadata_guide)

برای غنی‌سازی متن پیام‌ها و ایجاد قالب‌بندی پیشرفته، می‌توانید از متادیتاهای زیر استفاده کنید. هر متادیتا با علامت‌های مشخصی در ابتدا و انتهای عبارت اعمال می‌شود:

| نوع قالب‌بندی | علامت‌ها | مثال |
|------|------|------|
| برجسته (Bold) | `**` | `**سلام دوست عزیز!**` |
| کج (Italic) | `__` | `__این یک جمله تست است.__` |
| اسپویل (Spoiler) | `||` | `||متن اسپویل شده||` |
| نقل قول (Quote) | `>` (فقط ابتدا) | `> سلام!` |
| زیرخط (Underline) | `--` | `--تست--` |
| خط‌خورده (Strikethrough) | `~~` | `~~عالی و قوی~~` |
| مونو (Monospace) | `` ` `` | `` `بی‌نظیر` `` |
| بلاک کد (Code Block) | `` ``` `` | `` ``` کد ``` `` |
| هایپرلینک | `[متن](لینک)` | `[کلیک کنید](https://example.com)` |
| منشن (Mention) | `[متن](sender_id)` | `[مدیر](u0...)` |

### نمونه‌های ترکیبی پیشرفته

**مثال ۱ - ترکیب چند متادیتا:**

    "> __سلام__ (کاربر عزیز)[u0] --به کتابخانه‌ی-- **MAXRubika** ||خوش آمدید||!"

**مثال ۲ - متادیتای تودرتو:**

    "> ||__**این یک جمله از کتابخانه --MAXRubika-- است.**__||"

**مثال ۳ - بلاک کد کامل:**

    """```from maxrubika import Messenger
    with Messenger("mySession") as app:
        info = client.get_channel_post_by_link("https://rubika.ir/RubiFAQ/BEFIDIFGBJHJECCD")
        print(info)```"""

**توجه:**

- حداکثر تعداد متادیتا در هر پیام ۳۰ مورد است و می‌توانید از ترکیب‌های مختلف به‌صورت همزمان استفاده کنید.

- برای اعمال متادیتا بر روی پیام، می‌بایست علامت‌ها را اول و آخر **جمله** قرار دهید، اگر در اول و آخر متن قرار دهید، متادیتا اعمال نمی‌شود. (به جز علامت های بلاک کد)

---

<a id="bot_button_structure"></a>
## [ساختار و انواع دکمه‌های کیپاد](#bot_button_structure)

دکمه‌های تعاملی در روبیکا به دو دستهٔ کلی تقسیم می‌شوند:

- **Inline Keypad:** دکمه‌های شیشه‌ای که در زیر پیام نمایش داده می‌شوند.
- **Chat Keypad:** دکمه‌های صفحه‌کلید که در پایین صفحهٔ گفتگو قرار می‌گیرند.

---

<a id="bot_button_models"></a>
### [مدل‌های پایه دکمه‌ها](#bot_button_models)

#### ۱. ButtonSelectionItem

هر گزینه از لیست انتخابی را تعریف می‌کند.

| فیلد | نوع | توضیحات |
|------|------|------|
| text | string | متن نمایشی گزینه |
| image_url | string | آدرس تصویر مرتبط (اختیاری) |
| type | ButtonSelectionTypeEnum | نوع نمایش دکمه |

#### ۲. ButtonSelection

تنظیمات کامل دکمهٔ انتخاب (type = Selection).

| فیلد | نوع | توضیحات |
|------|------|------|
| selection_id | string | شناسهٔ یکتای لیست |
| search_type | ButtonSelectionSearchEnum | نحوهٔ جستجو در لیست |
| get_type | ButtonSelectionGetEnum | نحوهٔ دریافت آیتم‌ها |
| items | list[ButtonSelectionItem] | آرایه‌ای از گزینه‌ها |
| is_multi_selection | bool | امکان انتخاب چندگانه |
| columns_count | string | تعداد ستون‌های نمایش |
| title | string | عنوان لیست |

#### ۳. ButtonCalendar

تنظیمات دکمهٔ تقویم (type = Calendar).

| فیلد | نوع | توضیحات |
|------|------|------|
| default_value | Optional[string] | تاریخ پیش‌فرض |
| type | ButtonCalendarTypeEnum | نوع تقویم (شمسی/میلادی) |
| min_year | string | حداقل سال قابل انتخاب |
| max_year | string | حداکثر سال قابل انتخاب |
| title | string | عنوان دکمه |

#### ۴. ButtonNumberPicker

تنظیمات دکمهٔ انتخاب عدد (type = NumberPicker).

| فیلد | نوع | توضیحات |
|------|------|------|
| min_value | string | حداقل مقدار |
| max_value | string | حداکثر مقدار |
| default_value | Optional[string] | مقدار پیش‌فرض |
| title | string | عنوان دکمه |

#### ۵. ButtonStringPicker

تنظیمات دکمهٔ انتخاب رشته (type = StringPicker).

| فیلد | نوع | توضیحات |
|------|------|------|
| items | list[string] | لیست گزینه‌های قابل انتخاب |
| default_value | Optional[string] | مقدار پیش‌فرض |
| title | Optional[string] | عنوان دکمه |

#### ۶. ButtonTextbox

تنظیمات دکمهٔ ورودی متن (type = Textbox).

| فیلد | نوع | توضیحات |
|------|------|------|
| type_line | ButtonTextboxTypeLineEnum | تک‌خطی یا چندخطی |
| type_keypad | ButtonTextboxTypeKeypadEnum | نوع صفحه‌کلید (عددی/متنی) |
| place_holder | Optional[string] | متن راهنما در فیلد |
| title | Optional[string] | عنوان دکمه |
| default_value | Optional[string] | مقدار پیش‌فرض |

#### ۷. ButtonLocation

تنظیمات دکمهٔ موقعیت مکانی (type = Location).

| فیلد | نوع | توضیحات |
|------|------|------|
| default_pointer_location | Location | مختصات نقطهٔ پیش‌فرض |
| default_map_location | Location | مرکز نقشه در نمای اولیه |
| type | ButtonLocationTypeEnum | حالت (انتخاب/مشاهده) |
| title | Optional[string] | عنوان دکمه |

---

<a id="bot_button_model"></a>
### [مدل اصلی Button](#bot_button_model)

مدل Button نمایانگر یک دکمهٔ تعاملی در رابط کاربری است که در کیپادهای شیشه‌ای یا صفحه‌کلید قابل استفاده است.

| فیلد | نوع | توضیحات |
|------|------|------|
| id | string | شناسهٔ یکتای دکمه |
| type | ButtonTypeEnum | نوع دکمه (تعیین‌کنندهٔ رفتار) |
| button_text | string | متن نمایشی روی دکمه |
| button_selection | ButtonSelection | تنظیمات دکمهٔ انتخابی |
| button_calendar | ButtonCalendar | تنظیمات دکمهٔ تقویم |
| button_number_picker | ButtonNumberPicker | تنظیمات دکمهٔ انتخاب عدد |
| button_string_picker | ButtonStringPicker | تنظیمات دکمهٔ انتخاب رشته |
| button_location | ButtonLocation | تنظیمات دکمهٔ موقعیت |
| button_textbox | ButtonTextbox | تنظیمات دکمهٔ ورودی متن |

**نکته مهم:** فیلدهای تخصصی دکمه (مانند button_selection و button_calendar) تنها زمانی معتبر هستند که نوع دکمه (type) با آن مدل سازگاری داشته باشد.

---

<a id="bot_button_types"></a>
### [انواع دکمه‌ها (ButtonTypeEnum)](#bot_button_types)

| نوع | توضیحات |
|------|------|
| Simple | دکمهٔ معمولی با متن ثابت |
| Selection | نمایش لیست انتخابی |
| Calendar | نمایش تقویم |
| NumberPicker | انتخاب عدد از محدودهٔ مشخص |
| StringPicker | انتخاب مقدار از لیست رشته‌ها |
| Location | اشتراک‌گذاری موقعیت مکانی |
| CameraImage | گرفتن عکس با دوربین |
| CameraVideo | گرفتن ویدئو با دوربین |
| GalleryImage | انتخاب عکس از گالری |
| GalleryVideo | انتخاب ویدئو از گالری |
| File | انتخاب فایل |
| Audio | انتخاب فایل صوتی |
| RecordAudio | ضبط صدا |
| Textbox | باز کردن ورودی متن |
| Link | باز کردن لینک |
| AskMyPhoneNumber | درخواست شماره تلفن کاربر |
| AskMyLocation | درخواست موقعیت کاربر |
| Barcode | اسکن بارکد |

---

<a id="bot_selection_types"></a>
### [انواع نمایش دکمه‌های انتخابی (ButtonSelectionTypeEnum)](#bot_selection_types)

| مقدار | توضیحات |
|------|------|
| TextOnly | نمایش فقط به صورت متن |
| TextImgThu | نمایش متن به همراه تصویر کوچک |
| TextImgBig | نمایش متن به همراه تصویر بزرگ |

---

<a id="bot_search_types"></a>
### [نحوهٔ جستجو در لیست انتخابی (ButtonSelectionSearchEnum)](#bot_search_types)

| مقدار | توضیحات |
|------|------|
| None | حالت پیش‌فرض (بدون جستجو) |
| Local | جستجو در آیتم‌های ارسالی در فیلد items |
| Api | جستجو از طریق API |

---

<a id="bot_get_types"></a>
### [نحوهٔ دریافت آیتم‌های لیست (ButtonSelectionGetEnum)](#bot_get_types)

| مقدار | توضیحات |
|------|------|
| Local | نمایش آیتم‌های ارسالی در فیلد items |
| Api | دریافت آیتم‌ها از طریق API |

---

<a id="bot_calendar_types"></a>
### [انواع تقویم (ButtonCalendarTypeEnum)](#bot_calendar_types)

| مقدار | توضیحات |
|------|------|
| DatePersian | تقویم شمسی |
| DateGregorian | تقویم میلادی |

---

<a id="bot_textbox_types"></a>
### [انواع صفحه‌کلید ورودی (ButtonTextboxTypeKeypadEnum)](#bot_textbox_types)

| مقدار | توضیحات |
|------|------|
| String | ورودی متنی (همهٔ کاراکترها) |
| Number | ورودی عددی (فقط اعداد) |

---

<a id="bot_line_types"></a>
### [انواع خطوط ورودی (ButtonTextboxTypeLineEnum)](#bot_line_types)

| مقدار | توضیحات |
|------|------|
| SingleLine | تک‌خطی |
| MultiLine | چندخطی |

---

<a id="bot_location_types"></a>
### [انواع موقعیت مکانی (ButtonLocationTypeEnum)](#bot_location_types)

| مقدار | توضیحات |
|------|------|
| Picker | کاربر می‌تواند موقعیت را انتخاب کند |
| View | موقعیت فقط به صورت نمایشی نشان داده می‌شود |

---

<a id="bot_button_examples"></a>
## [نمونه‌های عملی](#bot_button_examples)

### ساخت دکمهٔ ساده

```python
simple_button = {
    "id": "1",
    "type": "Simple",
    "button_text": "کلیک کنید"
}
```

### ساخت دکمهٔ انتخاب از لیست

```python
selection_button = {
    "id": "2",
    "type": "Selection",
    "button_text": "انتخاب رنگ",
    "button_selection": {
        "selection_id": "color_picker",
        "search_type": "Local",
        "get_type": "Local",
        "is_multi_selection": False,
        "columns_count": "2",
        "title": "رنگ مورد نظر را انتخاب کنید",
        "items": [
            {"text": "قرمز", "type": "TextOnly"},
            {"text": "آبی", "type": "TextOnly"},
            {"text": "سبز", "type": "TextOnly"}
        ]
    }
}
```

### ساخت دکمهٔ تقویم

```python
calendar_button = {
    "id": "3",
    "type": "Calendar",
    "button_text": "انتخاب تاریخ",
    "button_calendar": {
        "type": "DatePersian",
        "min_year": "1400",
        "max_year": "1410",
        "title": "تاریخ تولد خود را انتخاب کنید"
    }
}
```

### ساخت دکمهٔ ورودی متن

```python
textbox_button = {
    "id": "4",
    "type": "Textbox",
    "button_text": "نظر خود را بنویسید",
    "button_textbox": {
        "type_line": "MultiLine",
        "type_keypad": "String",
        "place_holder": "نظر خود را اینجا وارد کنید...",
        "title": "فرم نظرسنجی"
    }
}
```

---

<div style="display: flex; justify-content: center; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-plugins/" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">→ صفحه قبل</a>

<a href="../bot-guide/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مستندات ربات</a>

</div>