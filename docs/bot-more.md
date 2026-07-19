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
| هایپرلینک | `(متن)[لینک]` | `(کلیک کنید)[https://example.com]` |
| منشن (Mention) | `(متن)[sender_id]` | `(مدیر)[u0...]` |

### نمونه‌های ترکیبی پیشرفته

**مثال ۱ - ترکیب چند متادیتا:**

    "> __سلام__ (کاربر عزیز)[u0] --به کتابخانه‌ی-- **MAXRubika** ||خوش آمدید||!"

**مثال ۲ - متادیتای تودرتو:**

    "> ||__**این یک جمله از کتابخانه --MAXRubika-- است.**__||"

**مثال ۳ - بلاک کد کامل:**

    """```from maxrubika import Client
    client = Client("mySession")
    info = client.get_channel_post_by_link("https://rubika.ir/RubiFAQ/BEFIDIFGBJHJECCD")
    print(info)```"""

**توجه:** حداکثر تعداد متادیتا در هر پیام ۳۰ مورد است و می‌توانید از ترکیب‌های مختلف به‌صورت همزمان استفاده کنید.

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

<a href="bot-plugins" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">→ صفحه قبل</a>

<a href="bot-guide" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مستندات ربات</a>

</div>