# متدها

---

## [get_me](#get_me)

این متد برای دریافت اطلاعات هویتی بات به کار می‌رود. اطلاعاتی نظیر نام، نام‌کاربری، شناسه (ID)، پیام اولیه بات و... از طریق این متد قابل دریافت است. این متد هیچ پارامتری به عنوان ورودی دریافت نمی‌کند.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    print(bot.get_me())

except Exception as e:
    print(e)
```

---

## [get_chat_info](#get_chat_info)

این متد برای دریافت اطلاعات مربوط به یک کاربر، گروه یا کانال استفاده می‌شود. پارامتر پذیرفته‌شده توسط این متد به شرح زیر است:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.get_chat_info("chat_id")
    print(a)

except Exception as e:
    print(e)
```

---

## [get_updates](#get_updates)

این متد برای دریافت رویدادهای جدید (مانند پیام‌ها) از API به صورت دستی استفاده می‌شود، این متد عمدتاً برای حالت Polling کاربرد دارد. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **offset_id:** شناسه‌ای برای دریافت رویدادهای بعدی. (پیش‌فرض: None)
- **limit:** حداکثر تعداد رویدادهای قابل دریافت. (پیش‌فرض: ۱۰۰)

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.get_updates(limit=50)
    print(a)

except Exception as e:
    print(e)
```

---

## [send_message](#send_message)

این متد برای ارسال پیام متنی به یک گفتگو (چت) به کار می‌رود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **text:** متن پیام.
- **chat_keypad:** تنظیم کیبورد سفارشی برای گفتگو. (پیش‌فرض: None)
- **inline_keypad:** تنظیم دکمه‌های شیشه‌ای (Inline) برای پیام. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیامی که می‌خواهید به آن ریپلای بزنید. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان برای این پیام. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن اندازه دکمه‌های chat_keypad. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد گفتگو پس از کلیک کاربر روی یکی از دکمه‌ها. (پیش‌فرض: False)

**نکات:**

1. شناسه گفتگو (chat_id) باید با g0 (برای گروه)، c0 (برای کانال) یا b0 (برای کاربر) شروع شود و مجموعاً ۳۲ کاراکتر باشد. دقت کنید که chat_id کاربر (که با b0 شروع می‌شود) با sender_id کاربر (که با u0 شروع می‌شود) متفاوت است. همچنین از وارد کردن GUID که ظاهری مشابه دارد، خودداری کنید. برای دریافت chat_id گفتگوی مورد نظر، [اینجا](bot-examples.md/#bot_examples_user_info) کلیک کنید.
2. حداکثر تعداد کاراکتر مجاز برای متن پیام ۴۰۹۶ کاراکتر است.
3. برای ساخت chat_keypad و inline_keypad، می‌توانید از روش ساده‌سازی‌شده کتابخانه استفاده کنید. در این روش، نیازی به تنظیم دستی button_id و type نیست. کتابخانه به طور خودکار button_id را از عدد ۱۰۰ به ترتیب چینش دکمه‌ها مقداردهی می‌کند و نوع (type) دکمه را نیز Simple در نظر می‌گیرد. برای مشاهده انواع دکمه‌ها، [اینجا](bot-more.md/#bot_button_types) کلیک کنید.
4. پارامترهای resize_keyboard و one_time_keyboard تنها زمانی تأثیرگذار هستند که chat_keypad مقداردهی شده باشد.
5. برای استفاده از متادیتا در متن پیام (مانند برجسته، کج، منشن، هایپرلینک و...)، [اینجا](bot-more.md/#bot_metadata_guide) کلیک کنید.

**مثال‌ها:**

ارسال یک پیام متنی ساده:

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_message("chat_id", "این یک پیام تستی است.")
    print(a)

except Exception as e:
    print(e)
```

ارسال پیام با استفاده از متادیتا:

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_message("chat_id", "> **سلام** به __کتابخانه__ ||MAXRubika|| ~~خوش آمدید.~~")
    print(a)

except Exception as e:
    print(e)
```

ارسال پیام همراه با chat_keypad و inline_keypad (روش ساده):

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_message(
        chat_id="chat_id", text="این یک پیام تستی است.",
        inline_keypad=[["دکمه 1"], ["دکمه 2"]],
        chat_keypad=[["ارتباط با مدیر", "خروج"]])
    print(a)

except Exception as e:
    print(e)
```

ارسال پیام همراه با chat_keypad و inline_keypad (روش سفارشی):

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_message(
        chat_id="chat_id", text="این یک پیام تستی است.",
        inline_keypad={
            "rows": [
                {
                    "buttons": [
                        {"id": "10", "type": "Simple", "button_text": "دکمه 1"},
                        {"id": "100", "type": "Simple", "button_text": "دکمه 2"},
                        {"id": "1000", "type": "Simple", "button_text": "دکمه 3"}
                    ]
                }
            ]
        },
        chat_keypad={
            "rows": [
                {
                    "buttons": [{"id": "1", "type": "Simple", "button_text": "ارتباط با مدیر"}]
                },
                {
                    "buttons": [
                        {"id": "2", "type": "AskMyPhoneNumber", "button_text": "نمایش شماره تلفن من"},
                        {"id": "3", "type": "AskMyLocation", "button_text": "نمایش موقعیت مکانی من"}
                    ]
                }
            ]
        })
    print(a)

except Exception as e:
    print(e)
```

---

## [edit_message](#edit_message)

این متد برای ویرایش متن یک پیام از پیش ارسال‌شده در گفتگو به کار می‌رود. پارامترهای ورودی آن عبارتند از:

- **chat_id:** شناسه (چت آیدی) گفتگویی که پیام در آن قرار دارد.
- **message_id:** شناسه (مسیج آیدی) پیامی که باید ویرایش شود.
- **text:** متن جدید جایگزین.

**نکات:**

1. شناسه گفتگو باید با g0، c0 یا b0 شروع شده و مجموعاً ۳۲ کاراکتر باشد. دقت کنید که chat_id کاربر (با b0) با sender_id کاربر (با u0) متفاوت است. از GUID به جای آن استفاده نکنید. برای راهنمایی بیشتر [اینجا](bot-more.md/#bot_chat_id_guide) کلیک کنید.
2. متن جدید نیز حداکثر می‌تواند ۴۰۹۶ کاراکتر باشد.
3. بات تنها قادر به ویرایش پیام‌هایی است که خود ارسال کرده است. این محدودیت هم در گروه‌ها و هم در چت‌های خصوصی برقرار است.
4. برای آشنایی با نحوه استفاده از متادیتا در متن، [اینجا](bot-more.md/#bot_metadata_guide) کلیک کنید.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.edit_message("chat_id", "message_id", "متن جدید")
    print(a)

except Exception as e:
    print(e)
```

---

## [edit_inline_keypad](#edit_inline_keypad)

این متد برای ویرایش دکمه‌های شیشه‌ای (Inline Keypad) یک پیام در گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی حاوی پیام.
- **message_id:** شناسه (مسیج آیدی) پیامی که دکمه‌های شیشه‌ای آن باید ویرایش شوند.
- **inline_keypad:** ساختار جدید دکمه‌های شیشه‌ای.

**نکات:**

1. شناسه گفتگو در حال حاضر باید با b0 (برای کاربر) شروع شده و ۳۲ کاراکتر باشد. آن را با sender_id اشتباه نگیرید. برای راهنمایی [اینجا](bot-more.md/#bot_chat_id_guide) کلیک کنید.
2. بات تنها می‌تواند دکمه‌های پیام‌هایی را ویرایش کند که خود ارسال کرده است.
3. اگر برای هر دکمه button_id و type مشخص نکنید، کتابخانه به طور خودکار button_id را از ۱۰۰ شماره‌گذاری کرده و type را Simple قرار می‌دهد. برای مشاهده انواع type، [اینجا](bot-more.md/#bot_button_types) کلیک کنید.

**مثال‌ها:**

ویرایش inline_keypad به روش ساده:

```python
from maxrubika import Bot
bot = Bot("token")

try:
    inline_keypad = [
        ["Button 1", "Button 2"],
        ["Button 3"]
    ]
    bot.edit_inline_keypad("chat_id", "message_id", inline_keypad)

except Exception as e:
    print(e)
```

ویرایش inline_keypad به روش سفارشی (دیکشنری):

```python
from maxrubika import Bot
bot = Bot("token")

try:
    inline_keypad = {
        "rows": [
            {"buttons": [{"id": "1", "button_text": "Button 1", "type": "Simple"}]},
            {"buttons": [{"id": "2", "button_text": "Button 2", "type": "Simple"}]}
        ]
    }
    bot.edit_inline_keypad("chat_id", "message_id", inline_keypad)

except Exception as e:
    print(e)
```

حذف کامل inline_keypad از یک پیام (با ارسال یک لیست خالی):

```python
from maxrubika import Bot
bot = Bot("token")

try:
    bot.edit_inline_keypad("chat_id", "message_id", inline_keypad=[])

except Exception as e:
    print(e)
```

---

## [edit_chat_keypad](#edit_chat_keypad)

این متد برای ویرایش کیبورد اصلی (Chat Keypad) یک گفتگو به کار می‌رود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگو.
- **chat_keypad:** ساختار جدید کیبورد.
- **resize_keyboard:** تراز بودن اندازه دکمه‌ها. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از اولین کلیک کاربر. (پیش‌فرض: False)

**نکات:**

1. شناسه گفتگو باید با b0 شروع و ۳۲ کاراکتری باشد. برای راهنمایی [اینجا](bot-more.md/#bot_chat_id_guide) کلیک کنید.
2. اگر button_id و type دکمه‌ها را مشخص نکنید، کتابخانه به‌طور خودکار آن‌ها را تنظیم می‌کند (button_id از ۱۰۰ و type به صورت Simple). برای اطلاعات بیشتر [اینجا](bot-more.md/#bot_button_types) کلیک کنید.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    chat_keypad = {
        "rows": [
            {"buttons": [{"id": "1", "button_text": "Button 1", "type": "Simple"}]},
            {"buttons": [{"id": "2", "button_text": "Button 2", "type": "Simple"}]}
        ]
    }
    bot.edit_chat_keypad("chat_id", chat_keypad)

except Exception as e:
    print(e)
```

---

## [remove_chat_keypad](#remove_chat_keypad)

این متد برای حذف کیبورد سفارشی از یک گفتگو و بازگرداندن آن به حالت پیش‌فرض استفاده می‌شود. پارامتر پذیرفته‌شده توسط این متد به شرح زیر است:

- **chat_id:** شناسه (چت آیدی) گفتگویی که کیبورد آن باید حذف شود.

**نکته:** شناسه گفتگو باید با b0 شروع و ۳۲ کاراکتری باشد. برای راهنمایی [اینجا](bot-more.md/#bot_chat_id_guide) کلیک کنید.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.remove_chat_keypad("chat_id")
    print(a)

except Exception as e:
    print(e)
```

---

## [delete_message](#delete_message)

این متد برای حذف یک پیام خاص از یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی حاوی پیام.
- **message_id:** شناسه (مسیج آیدی) پیام مورد نظر برای حذف.

**نکات:**

1. شناسه گفتگو می‌تواند با b0 ، c0 یا g0 شروع شود و می‌بایست ۳۲ کاراکتری باشد. برای راهنمایی [اینجا](bot-more.md/#bot_chat_id_guide) کلیک کنید.
2. بات در چت‌های خصوصی تنها پیام‌های خود را می‌تواند حذف کند. برای حذف پیام‌ها در گروه‌ها و کانال‌ها، بات باید دسترسی "حذف پیام" را داشته باشد.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.delete_message("chat_id", "message_id")
    print(a)

except Exception as e:
    print(e)
```

---

## [auto_delete_message](#auto_delete_message)

این متد برای حذف خودکار یک پیام پس از گذشت مدت زمان مشخصی به کار می‌رود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگو.
- **message_id:** شناسه (مسیج آیدی) پیام.
- **time:** مدت زمان تأخیر تا حذف پیام (به ثانیه).

**نکات:** مشابه با محدودیت‌های متد delete_message است.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    chat_id = "chat_id"

    message = bot.send_message(chat_id, "**This is a test message!**")
    print(message)

    delete = bot.auto_delete_message(chat_id, message.message_id, time=50)
    print(delete)

except Exception as e:
    print(e)
```

---

## [forward_message](#forward_message)

این متد برای هدایت (فوروارد) یک پیام از یک گفتگو به گفتگویی دیگر استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **from_chat_id:** شناسه (چت آیدی) گفتگوی مبدأ.
- **message_id:** شناسه (مسیج آیدی) پیام مورد نظر برای فوروارد.
- **to_chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **disable_notification:** غیرفعال‌سازی اعلان برای کاربر مقصد. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    from_chat_id = "c0asc...."
    to_chat_id = "b0adf...."

    a = bot.forward_message(from_chat_id, "message_id", to_chat_id)
    print(a)

except Exception as e:
    print(e)
```

---

## [send_contact](#send_contact)

این متد برای ارسال یک مخاطب به یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **phone_number:** شماره تلفن مخاطب.
- **first_name:** نام مخاطب.
- **last_name:** نام خانوادگی مخاطب. (پیش‌فرض: خالی)
- **chat_keypad:** کیبورد سفارشی برای گفتگو. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:** مشابه نکات مربوط به chat_id و ساختار کیبوردها در بخش send_message است.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_contact(
        phone_number="+989123456789",
        first_name="MEHRAB", last_name="Farahmand",
        chat_id="chat_id")
    print(a)

except Exception as e:
    print(e)
```

---

## [send_location](#send_location)

این متد برای ارسال یک موقعیت مکانی جغرافیایی به یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **latitude:** عرض جغرافیایی (Latitude).
- **longitude:** طول جغرافیایی (Longitude).
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:** مشابه نکات مربوط به chat_id و ساختار کیبوردها در بخش send_message است.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_location(chat_id="chat_id", latitude=32.6546, longitude=51.6680)
    print(a)

except Exception as e:
    print(e)
```

---

## [send_poll](#send_poll)

این متد برای ایجاد و ارسال یک نظرسنجی ساده به یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **question:** متن سؤال نظرسنجی.
- **options:** لیستی از گزینه‌های نظرسنجی (بین ۲ تا ۱۰ گزینه).
- **is_anonymous:** ناشناس بودن رأی‌ها. (پیش‌فرض: True)
- **multi_select:** امکان انتخاب چند گزینه. (پیش‌فرض: False)
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:** مشابه نکات مربوط به chat_id و ساختار کیبوردها در بخش send_message است.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_poll(
        chat_id="chat_id", question= "شما کدام رنگ را بیشتر دوست دارید؟",
        options=["آبی", "صورتی", "زرد", "سبز", "نارنجی", "قرمز", "بنفش"],
        is_anonymous=False, multi_select=True)
    print(a)

except Exception as e:
    print(e)
```

---

## [send_quiz](#send_quiz)

این متد برای ایجاد و ارسال یک نظرسنجی به‌صورت آزمون که تنها یک پاسخ صحیح دارد، استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **question:** متن سؤال آزمون.
- **options:** لیست گزینه‌های آزمون (بین ۲ تا ۱۰ گزینه).
- **correct_option:** ایندکس عددی (شروع از ۰) یا متن دقیق گزینه صحیح.
- **hint:** متن راهنمایی برای آزمون. (پیش‌فرض: None)
- **is_anonymous:** ناشناس بودن پاسخ‌ها. (پیش‌فرض: True)
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:** مشابه نکات مربوط به chat_id و ساختار کیبوردها در بخش send_message است.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    b = bot.send_quiz(
        chat_id= "chat_id",
        question= "پایتخت کشور کره جنوبی کدام گزینه است؟",
        options= ["بوسان", "اینچئون", "سئول", "دائگو"], correct_option= "سئول",
        hint= "پایتخت و بزرگترین شهر کره جنوبی سئول می‌باشد.", is_anonymous= False)
    print(b)

except Exception as e:
    print(e)
```

---

## [send_file](#send_file)

این متد برای ارسال یک فایل (به‌صورت عمومی) به یک گفتگو استفاده می‌شود؛ برای ارسال فایل‌های خاص مانند عکس یا ویدئو، متدهای اختصاصی توصیه می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **file:** نام و پسوند فایل برای ارسال. (در صورت استفاده از file_id، این پارامتر نیاز نیست.)
- **file_id:** شناسه فایلی که از طریق متد upload_file دریافت شده است. (در صورت استفاده از file، این پارامتر نیاز نیست.)
- **type:** نوع فایل. (پیش‌فرض: File)
- **text:** کپشن یا توضیح فایل (حداکثر ۲۰۴۸ کاراکتر).
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:** مشابه نکات مربوط به chat_id و ساختار کیبوردها در بخش send_message است.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_file(chat_id= "chat_id", file= "newfile.py", text= "فایل پایتونی تقدیم به شما")
    print(a)

except Exception as e:
    print(e)
```

---

## [send_image](#send_image)

این متد برای ارسال یک تصویر به یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **image:** نام و پسوند فایل تصویری (مانند .jpg یا .png). (در صورت استفاده از file_id نیاز نیست.)
- **file_id:** شناسه تصویر دریافت‌شده از upload_file. (در صورت استفاده از image نیاز نیست.)
- **text:** کپشن یا توضیح تصویر (حداکثر ۲۰۴۸ کاراکتر).
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:**

1. نکات مربوط به chat_id و ساختار کیبوردها مشابه متد send_message است.
2. فایل واردشده باید حتماً یک تصویر با پسوندهای معتبر تصویری (.jpg ، .png و غیره) باشد، در غیر این صورت با خطا مواجه خواهید شد.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_image(chat_id= "chat_id", image= "1.jpg", disable_notification= True)
    print(a)

except Exception as e:
    print(e)
```

---

## [send_video](#send_video)

این متد برای ارسال یک ویدئو به یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **video:** نام و پسوند فایل ویدئویی (مانند .mp4). (در صورت استفاده از file_id نیاز نیست.)
- **file_id:** شناسه ویدئو دریافت‌شده از upload_file. (در صورت استفاده از video نیاز نیست.)
- **text:** کپشن یا توضیح ویدئو (حداکثر ۲۰۴۸ کاراکتر).
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:**

1. نکات مربوط به chat_id و ساختار کیبوردها مشابه متد send_message است.
2. فایل واردشده باید حتماً یک ویدئو با پسوندهای معتبر (.mp4 ، .mov و غیره) باشد.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_video(chat_id= "chat_id", video= "20260531.mp4", text= "این یک ویدئو است.")
    print(a)

except Exception as e:
    print(e)
```

---

## [send_voice](#send_voice)

این متد برای ارسال یک پیام صوتی (ویس) به یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **voice:** نام و پسوند فایل صوتی (فقط .mp3). (در صورت استفاده از file_id نیاز نیست.)
- **file_id:** شناسه فایل صوتی دریافت‌شده از upload_file. (در صورت استفاده از voice نیاز نیست.)
- **text:** کپشن یا توضیح پیام صوتی (حداکثر ۲۰۴۸ کاراکتر).
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:**

1. نکات مربوط به chat_id و ساختار کیبوردها مشابه متد send_message است.
2. پسوند فایل صوتی باید الزاماً .mp3 باشد، در غیر این صورت با خطا مواجه خواهید شد.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_voice(chat_id= "chat_id", voice= "20260531.mp3")
    print(a)

except Exception as e:
    print(e)
```

---

## [send_music](#send_music)

این متد برای ارسال یک فایل موسیقی به یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **music:** نام و پسوند فایل موسیقی (مانند .mp3). (در صورت استفاده از file_id نیاز نیست.)
- **file_id:** شناسه موسیقی دریافت‌شده از upload_file. (در صورت استفاده از music نیاز نیست.)
- **text:** کپشن یا توضیح موسیقی (حداکثر ۲۰۴۸ کاراکتر).
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:**

1. نکات مربوط به chat_id و ساختار کیبوردها مشابه متد send_message است.
2. فایل واردشده باید دارای پسوندهای معتبر موسیقی (مانند .mp3) باشد.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_music(chat_id= "chat_id", music= "Hamid Hiraad - Khaste Shodam (320).mp3")
    print(a)

except Exception as e:
    print(e)
```

---

## [send_gif](#send_gif)

این متد برای ارسال یک گیف (تصویر متحرک بی‌صدا) به یک گفتگو استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گفتگوی مقصد.
- **gif:** نام و پسوند فایل گیف (فقط .mp4 بی‌صدا). (در صورت استفاده از file_id نیاز نیست.)
- **file_id:** شناسه گیف دریافت‌شده از upload_file. (در صورت استفاده از gif نیاز نیست.)
- **text:** کپشن یا توضیح گیف (حداکثر ۲۰۴۸ کاراکتر).
- **chat_keypad:** کیبورد سفارشی. (پیش‌فرض: None)
- **inline_keypad:** دکمه‌های شیشه‌ای. (پیش‌فرض: None)
- **reply_to_message_id:** شناسه (مسیج آیدی) پیام برای ریپلای. (پیش‌فرض: None)
- **disable_notification:** غیرفعال‌سازی اعلان. (پیش‌فرض: False)
- **resize_keyboard:** تراز بودن دکمه‌های کیبورد. (پیش‌فرض: True)
- **one_time_keyboard:** محو شدن کیبورد پس از کلیک. (پیش‌فرض: False)

**نکات:**

1. نکات مربوط به chat_id و ساختار کیبوردها مشابه متد send_message است.
2. گیف باید یک فایل ویدئویی .mp4 بی‌صدا باشد، در غیر این صورت با خطا مواجه می‌شوید.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.send_gif(chat_id= "chat_id", gif= "2_5352595205864328454.mp4")
    print(a)

except Exception as e:
    print(e)
```

---

## [request_send_file](#request_send_file)

این متد برای درخواست یک URL آپلود از سرورهای روبیکا به منظور ارسال یک فایل استفاده می‌شود. این اولین گام در فرایند آپلود فایل است. پارامتر پذیرفته‌شده توسط این متد به شرح زیر است:

- **file_type:** نوع فایل برای آپلود. مقادیر قابل قبول: ['File', 'Image', 'Voice', 'Video', 'Music', 'Gif'] (پیش‌فرض: File)

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.request_send_file(file_type="Image")
    print(a)

except Exception as e:
    print(e)
```

---

## [upload_file](#upload_file)

این متد برای آپلود فایل روی سرورهای روبیکا با استفاده از URL دریافت‌شده از متد request_send_file به کار می‌رود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **url:** آدرس آپلود دریافت‌شده از مرحله قبل.
- **file_path:** مسیر فایل در سیستم شما (می‌تواند str یا Path باشد).
- **file_name:** نام فایل. (اگر این پارامتر وارد نشود، نام فایل از file_path گرفته می‌شود.)

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    # مرحله اول: دریافت URL آپلود برای نوع فایل "Image"
    upload_info = bot.request_send_file(file_type="Image")
    # مرحله دوم: آپلود فایل به سرور
    b = bot.upload_file(url= upload_info.upload_url, file_path= "IMG_20250911_220142_592.jpg")
    print(b)

except Exception as e:
    print(e)
```

---

## [download_file](#download_file)

این متد برای دانلود یک فایل از سرورهای روبیکا با استفاده از شناسه فایل (file_id) به کار می‌رود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **file_id:** شناسه فایل برای دانلود.
- **name:** نام سفارشی برای فایل ذخیره‌شده (بدون پسوند).
- **path:** مسیر سفارشی برای ذخیره‌سازی.
- **save_as:** در صورت True بودن، فایل روی دیسک ذخیره می‌شود. در صورت False بودن، محتوای فایل به صورت بایت (bytes) بازگردانده می‌شود. (پیش‌فرض: False)
- **callback:** تابعی برای گزارش پیشرفت دانلود که سه آرگومان downloaded, total, percent دریافت می‌کند. (پیش‌فرض: None)

**خروجی:**

- اگر save_as=True باشد: دیکشنری شامل وضعیت و file_path.
- اگر save_as=False باشد: محتوای فایل به صورت bytes.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    b = bot.download_file("file_id", save_as= True)
    print(b)

except Exception as e:
    print(e)
```

---

## [get_file](#get_file)

این متد برای دریافت اطلاعات یک فایل با استفاده از شناسه آن به کار می‌رود. پارامتر پذیرفته‌شده توسط این متد به شرح زیر است:

- **file_id:** شناسه فایل.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    b = bot.get_file("file_id")
    print(b)

except Exception as e:
    print(e)
```

---

## [ban_member](#ban_member) یا [remove_member](#remove_member)

این متدها برای مسدود کردن (بن کردن) یک عضو از یک گروه یا کانال استفاده می‌شوند. پارامترهای پذیرفته‌شده توسط این متدها به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گروه (با g0) یا کانال (با c0).
- **sender_id:** شناسه (سندر آیدی) کاربری که باید مسدود شود (با u0).

**نکته:** مقدار chat_id نباید با b0 (چت خصوصی) شروع شود.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.ban_member(chat_id="g0xxxxxxxxxxxxxxx", sender_id="u0xxxxxxxxxxxxxxx")
    print(a)

except Exception as e:
    print(e)
```

---

## [unban_member](#unban_member)

این متد برای رفع مسدودیت (آنبن کردن) یک عضو از یک گروه یا کانال استفاده می‌شود. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **chat_id:** شناسه (چت آیدی) گروه (با g0) یا کانال (با c0).
- **sender_id:** شناسه (سندر آیدی) کاربری که باید از مسدودیت خارج شود.

**نکته:** مقدار chat_id نباید با b0 شروع شود.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.unban_member(chat_id="g0xxxxxxxxxxxxxxx", sender_id="u0xxxxxxxxxxxxxxx")
    print(a)

except Exception as e:
    print(e)
```

---

## [set_commands](#set_commands)

این متد برای تنظیم لیست کامندهای بات که در منوی آن نمایش داده می‌شود، استفاده می‌شود. پارامتر پذیرفته‌شده توسط این متد به شرح زیر است:

- **commands:** تنظیم کامندها. می‌تواند یک لیست از دیکشنری‌ها یا یک دیکشنری ساده باشد. (اگر این پارامتر وارد نشود یا خالی باشد، تمام کامندهای قبلی حذف خواهند شد.)

**مثال‌ها:**

```python
from maxrubika import Bot
bot = Bot("token")

# روش اول: ارسال یک لیست از دیکشنری‌ها
try:
    b = bot.set_commands([{"command": "start", "description": "Start the bot"}, {"command": "help", "description": "help of bot"}])
    print(b)

except Exception as e:
    print(e)
```

```python
from maxrubika import Bot
bot = Bot("token")

# روش دوم: ارسال یک دیکشنری ساده
try:
    b = bot.set_commands({"start": "Start the bot", "help": "Show help"})
    print(b)

except Exception as e:
    print(e)
```

---

## [update_bot_endpoints](#update_bot_endpoints)

این متد برای ثبت یک یا چند URL وب‌هوک روی سرورهای روبیکا استفاده می‌شود. با این کار، رویدادهای مختلف بات به‌جای این که شما آن‌ها را دریافت (Pull) کنید، از سمت سرور به سمت URL شما ارسال (Push) می‌شوند. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **url:** آدرس کامل و عمومی که سرور روبیکا باید رویدادها را به آن ارسال کند (توصیه می‌شود از HTTPS استفاده شود).
- **endpoint_type:** نوع رویدادی که این URL مدیریت خواهد کرد. مقادیر قابل قبول:
    - "ReceiveUpdate": پیام‌های جدید، ویرایش‌ها و حذف‌ها.
    - "ReceiveInlineMessage": فشردن دکمه‌های شیشه‌ای (Inline).
    - "ReceiveQuery": نتایج جستجوی درون‌خطی (Inline Query).
    - "GetSelectionItem": انتخاب آیتم‌های منو.
    - "SearchSelectionItems": درخواست جستجو در آیتم‌های انتخابی.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.update_bot_endpoints(
        url="https://myserver.com/wk",
        endpoint_type="ReceiveUpdate"
    )
    print(a)

except Exception as e:
    print(e)
```

---

## [register_all_endpoints](#register_all_endpoints)

این متد یک میانبر برای ثبت تمامی وب‌هوک‌ها به‌طور هم‌زمان است و برای راه‌اندازی اولیه بات بسیار مفید است.

- **base_url:** URL پایه سرور شما (مثلاً "https://myserver.com"). مسیر /wk به‌طور خودکار به آن اضافه خواهد شد.
- **endpoints:** لیستی از انواع رویدادها برای ثبت. اگر None باشد، هر پنج نوع ثبت می‌شوند.

**مثال:**

```python
from maxrubika import Bot
bot = Bot("token")

try:
    a = bot.register_all_endpoints("https://myserver.com")
    print(a)

except Exception as e:
    print(e)
```

---

## [start](#start)

این متد (غیرهمگام - async) برای راه‌اندازی بات در یکی از دو حالت Polling (دریافت مداوم به‌روزرسانی‌ها) یا Webhook (دریافت رویدادها از طریق یک سرور وب) استفاده می‌شود. این متد تا زمانی که بات متوقف نشود، اجرا می‌ماند. پارامترهای پذیرفته‌شده توسط این متد به شرح زیر هستند:

- **poll_interval:** فاصله زمانی (به ثانیه) بین هر درخواست دریافت به‌روزرسانی در حالت Polling. (پیش‌فرض: ۰.۰۰۵)
- **webhook_url:** URL عمومی سرور شما برای فعال‌سازی حالت Webhook. در صورت تنظیم، حالت Polling غیرفعال می‌شود.
- **webhook_path:** مسیر مدیریت درخواست‌های وب‌هوک روی سرور. (پیش‌فرض: /wk)
- **host:** آدرس میزبان برای راه‌اندازی وب سرور. (پیش‌فرض: "0.0.0.0")
- **port:** پورت برای راه‌اندازی وب سرور. (پیش‌فرض: ۸۰۸۰)

**مثال (حالت Polling):**

```python
import asyncio
from maxrubika import Bot

async def main():
    bot = Bot("token")
    @bot.on_message()
    async def handle_message(bot, event):
        print(event)
    await bot.start()

asyncio.run(main())
```

---

## [run](#run)

این یک متد همگام (sync) است که به عنوان یک پوشش ساده برای متد start عمل می‌کند و اجرای برنامه را تا زمان فشردن Ctrl+C متوقف نگه می‌دارد. برای اسکریپت‌هایی که حلقه رویداد asyncio فعال ندارند، بسیار مناسب است.

پارامترهای این متد دقیقاً مشابه متد start هستند.

**مثال (حالت Polling):**

```python
from maxrubika import Bot

bot = Bot("token")

@bot.on_message()
async def handle_message(bot, event):
    print(event)

bot.run()
```

---

<div style="display: flex; justify-content: center; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="/bot-guide" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مستندات ربات</a>

<a href="/bot-decorators" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">صفحه بعد ←</a>

</div>