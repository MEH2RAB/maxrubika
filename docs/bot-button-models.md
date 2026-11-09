# ساختار و انواع دکمه‌های کیپاد

---

دکمه‌های تعاملی در شاد به دو دستهٔ کلی تقسیم می‌شوند:

- **Inline Keypad:** دکمه‌های شیشه‌ای که در زیر پیام نمایش داده می‌شوند.
- **Chat Keypad:** دکمه‌های صفحه‌کلید که در پایین صفحهٔ گفتگو قرار می‌گیرند.

---

## مدل‌های پایه دکمه‌ها

### ۱. ButtonSelectionItem

هر گزینه از لیست انتخابی را تعریف می‌کند.

| فیلد | نوع | توضیحات |
|------|------|------|
| text | string | متن نمایشی گزینه |
| image_url | string | آدرس تصویر مرتبط (اختیاری) |
| type | ButtonSelectionTypeEnum | نوع نمایش دکمه |

---

### ۲. ButtonSelection

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

---

### ۳. ButtonCalendar

تنظیمات دکمهٔ تقویم (type = Calendar).

| فیلد | نوع | توضیحات |
|------|------|------|
| default_value | Optional[string] | تاریخ پیش‌فرض |
| type | ButtonCalendarTypeEnum | نوع تقویم (شمسی/میلادی) |
| min_year | string | حداقل سال قابل انتخاب |
| max_year | string | حداکثر سال قابل انتخاب |
| title | string | عنوان دکمه |

---

### ۴. ButtonNumberPicker

تنظیمات دکمهٔ انتخاب عدد (type = NumberPicker).

| فیلد | نوع | توضیحات |
|------|------|------|
| min_value | string | حداقل مقدار |
| max_value | string | حداکثر مقدار |
| default_value | Optional[string] | مقدار پیش‌فرض |
| title | string | عنوان دکمه |

---

### ۵. ButtonStringPicker

تنظیمات دکمهٔ انتخاب رشته (type = StringPicker).

| فیلد | نوع | توضیحات |
|------|------|------|
| items | list[string] | لیست گزینه‌های قابل انتخاب |
| default_value | Optional[string] | مقدار پیش‌فرض |
| title | Optional[string] | عنوان دکمه |

---

### ۶. ButtonTextbox

تنظیمات دکمهٔ ورودی متن (type = Textbox).

| فیلد | نوع | توضیحات |
|------|------|------|
| type_line | ButtonTextboxTypeLineEnum | تک‌خطی یا چندخطی |
| type_keypad | ButtonTextboxTypeKeypadEnum | نوع صفحه‌کلید (عددی/متنی) |
| place_holder | Optional[string] | متن راهنما در فیلد |
| title | Optional[string] | عنوان دکمه |
| default_value | Optional[string] | مقدار پیش‌فرض |

---

### ۷. ButtonLocation

تنظیمات دکمهٔ موقعیت مکانی (type = Location).

| فیلد | نوع | توضیحات |
|------|------|------|
| default_pointer_location | Location | مختصات نقطهٔ پیش‌فرض |
| default_map_location | Location | مرکز نقشه در نمای اولیه |
| type | ButtonLocationTypeEnum | حالت (انتخاب/مشاهده) |
| title | Optional[string] | عنوان دکمه |

---

## مدل اصلی Button

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

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-more/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به توضیحات بیشتر</a>

</div>