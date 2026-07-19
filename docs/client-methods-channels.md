# کانال‌ها

---

<a id="client_check_channel_username"></a>
## [check_channel_username](#client_check_channel_username)

این متد برای بررسی وضعیت یک نام‌کاربری به کار می‌رود. با استفاده از آن می‌توان تعیین کرد که نام‌کاربری مورد نظر آزاد است یا پیش‌تر ثبت شده است.

**پارامتر:**

- **username:** نام‌کاربری مورد نظر برای بررسی.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    check = client.check_channel_username("@Undefined")
    print(check)

except Exception as e:
    print(e)
```

---

<a id="client_create_channel"></a>
## [create_channel](#client_create_channel)

این متد برای ایجاد یک کانال جدید به کار می‌رود.

**پارامترها:**

- **title:** عنوان کانال. (حداکثر ۶۰ کاراکتر، نمی‌تواند خالی باشد)
- **members:** لیست اعضای اولیه کانال. نام‌کاربری و GUID هر دو قابل قبول هستند. (پیش‌فرض: None)
- **channel_type:** نوع کانال. مقادیر قابل قبول: `Public` یا `Private`. (پیش‌فرض: Public)
- **description:** متن بیوگرافی کانال. (حداکثر ۳۰۰ کاراکتر، پیش‌فرض: None)

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.create_channel(
        title="کانال تست",
        members=["Online_User", "@ShowInfoBot", "@Cipher", "ir_maxware", "u0HryBf03dbfba68374497983bc850a0"],
        channel_type="Public",
        description="این یک کانال تست است."
    )
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_delete_channel"></a>
## [delete_channel](#client_delete_channel)

این متد برای حذف یک کانال به کار می‌رود.

**پارامتر:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**توجه:** پس از اجرای این متد، برای تکمیل عملیات حذف، باید حرف `y` را در کنسول وارد نمایید.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.delete_channel("c0CyVlK0cae995e5b46031170a358a4e")
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_edit_channel_info"></a>
## [edit_channel_info](#client_edit_channel_info)

این متد برای ویرایش تنظیمات یک کانال به کار می‌رود.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **title:** عنوان جدید کانال. (حداکثر ۶۰ کاراکتر، نمی‌تواند خالی باشد)
- **description:** بیوگرافی جدید کانال. (حداکثر ۳۰۰ کاراکتر)
- **username:** نام‌کاربری جدید کانال. (حداقل ۷ و حداکثر ۳۲ کاراکتر)
- **channel_type:** نوع کانال (`Public` یا `Private`).
- **sign_messages:** تعیین می‌کند که نام نویسندگان زیر پیام‌های کانال نمایش داده شود یا خیر.
- **is_restricted_content:** تعیین می‌کند که امکان اسکرین‌شات یا ذخیره محتوای کانال برای اعضا محدود شود یا خیر.
- **reactions:** تنظیمات ری‌اکشن. مقادیر قابل قبول: `All` (فعال‌سازی همه)، `Disable` (غیرفعال‌سازی همه)، یا لیستی از اعداد (فعال‌سازی ری‌اکشن‌های خاص).

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.edit_channel_info(
        channel="https://rubika.ir/joinc/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD",
        title="کانال من",
        username="infoChannel1234",
        channel_type="Public",
        description="درباره‌ی من.",
        reactions=[1, 2, 3, 5, 7, 9, 12, 20],
        sign_messages=True
    )
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_edit_channel_title"></a>
## [edit_channel_title](#client_edit_channel_title)

این متد برای ویرایش عنوان یک کانال به کار می‌رود. این متد میانبری برای `edit_channel_info` با پارامتر `title` است.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **title:** عنوان جدید کانال.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.edit_channel_title("@TheProgrammer", "new title")
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_get_channel_admin_access"></a>
## [get_channel_admin_access](#client_get_channel_admin_access)

این متد برای دریافت سطح دسترسی‌های یک ادمین در کانال هدف به کار می‌رود.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **admin:** نام‌کاربری یا شناسه (GUID) ادمین مورد نظر.

**نکات:**

1. تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.
2. تنها در صورتی می‌توانید دسترسی‌های یک ادمین را مشاهده کنید که شما او را ادمین کرده باشید یا مالک کانال باشید؛ در غیر این صورت با خطا مواجه خواهید شد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.get_channel_admin_access("@TheProgrammer", "@Online_User")
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_get_channel_admins"></a>
## [get_channel_admins](#client_get_channel_admins)

این متد برای دریافت فهرست کامل ادمین‌های یک کانال به کار می‌رود. این متد به صورت خودکار تمام صفحات را پیمایش می‌کند و همه ادمین‌ها را بازمی‌گرداند.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **show_admin_guids:** در صورت True بودن، شناسه (GUID) ادمین‌ها نیز به صورت جداگانه در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.get_channel_admins("CodeYaran")
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_get_channel_info"></a>
## [get_channel_info](#client_get_channel_info)

این متد برای دریافت اطلاعات یک کانال به کار می‌رود.

**پارامتر:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.get_channel_info("MEH2RAB")
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_get_channel_link"></a>
## [get_channel_link](#client_get_channel_link)

این متد برای دریافت لینک خصوصی یک کانال به کار می‌رود.

**پارامتر:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.get_channel_link("g0G3R19035f77574adc0127ab97c999c")
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_get_channel_members"></a>
## [get_channel_members](#client_get_channel_members)

این متد برای دریافت فهرست اعضای یک کانال به کار می‌رود.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **search_text:** عبارت مورد نظر برای جستجو در میان اعضا، مانند نام‌کاربری. (پیش‌فرض: None)
- **start_id:** شناسه شروع برای دریافت صفحه‌بندی‌شده اعضا. (پیش‌فرض: None)

**نکات:**

1. تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.
2. به دلیل محدودیت‌های سرور روبیکا، این متد فقط 100 عضو آخر را نمایش می‌دهد.

**مثال‌ها:**

نمایش اعضای کانال:

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.get_channel_members("g0G3R19035f77574adc0127ab97c999c")
    print(action)

except Exception as e:
    print(e)
```

جستجوی یک کاربر خاص:

```python
from maxrubika import Client
client = Client("mySession")

try:
    action = client.get_channel_members("PythonChannel", search_text="@ir_MAXWare")
    print(action)

except Exception as e:
    print(e)
```

---

<a id="client_get_channel_post_by_link"></a>
## [get_channel_post_by_link](#client_get_channel_post_by_link)

این متد برای دریافت اطلاعات یک پیام کانال از طریق لینک آن پیام به کار می‌رود. خروجی شامل اطلاعات کانال، متن پیام و زمان ارسال است.

**پارامتر:**

- **url:** لینک پیام کانال.

**نکته:** فرمت معتبر لینک پیام کانال به صورت زیر است:
`https://rubika.ir/RubiFAQ/BICEGHDGFBGJHCCD`

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_channel_post_by_link("https://rubika.ir/RubiFAQ/BICEGHDGFBGJHCCD")
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_get_channel_seen_count"></a>
## [get_channel_seen_count](#client_get_channel_seen_count)

این متد برای دریافت آمار بازدید بازه‌ای از پیام‌های یک کانال به کار می‌رود.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **min_id:** شناسه (message_id) پیام آغازین بازه.
- **max_id:** شناسه (message_id) پیام پایانی بازه.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.get_channel_seen_count("CodeYaran", 157896351047, 189720063713)
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_get_channel_statistics"></a>
## [get_channel_statistics](#client_get_channel_statistics)

این متد برای دریافت تمام آمارهای یک کانال به کار می‌رود.

**پارامتر:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    stats = client.get_channel_statistics("CodeYaran")
    print(stats)

except Exception as e:
    print(e)
```

---

<a id="client_join_channel"></a>
## [join_channel](#client_join_channel)

این متد برای عضویت در یک کانال به کار می‌رود. هم لینک دعوت و هم روش مستقیم را پشتیبانی می‌کند.

**پارامتر:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.join_channel("@TheComputeriha")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_leave_channel"></a>
## [leave_channel](#client_leave_channel)

این متد برای خروج از یک کانال به کار می‌رود.

**پارامتر:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.leave_channel("@Rubika")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_seen_channel_messages"></a>
## [seen_channel_messages](#client_seen_channel_messages)

این متد برای علامت‌گذاری بازه‌ای از پیام‌های یک کانال به عنوان دیده‌شده به کار می‌رود.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **min_id:** شناسه (message_id) پیام آغازین بازه.
- **max_id:** شناسه (message_id) پیام پایانی بازه.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.seen_channel_messages("@PythonChannel", 11231014101, 52415414554)
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_set_channel_link"></a>
## [set_channel_link](#client_set_channel_link)

این متد برای تنظیم لینک خصوصی یک کانال به کار می‌رود.

**پارامتر:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_channel_link("@PC_and_Mobile")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_set_channel_type"></a>
## [set_channel_type](#client_set_channel_type)

این متد برای تغییر نوع کانال (عمومی یا خصوصی) به کار می‌رود. این متد میانبری برای `edit_channel_info` با پارامتر `channel_type` است.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **channel_type:** نوع کانال. مقادیر قابل قبول: `Public` یا `Private`.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_channel_type("@Undefined", channel_type="Private")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_update_channel_username"></a>
## [update_channel_username](#client_update_channel_username)

این متد برای به‌روزرسانی نام‌کاربری یک کانال به کار می‌رود.

**پارامترها:**

- **channel:** لینک، نام‌کاربری یا شناسه (GUID) کانال هدف.
- **username:** نام‌کاربری جدید. (حداقل ۷ و حداکثر ۳۲ کاراکتر، فقط حروف انگلیسی، اعداد و زیرخط)

**نکات:**

1. تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.
2. نام‌کاربری نمی‌تواند با عدد یا زیرخط شروع شود یا به زیرخط ختم شود و باید حداقل شامل یک حرف باشد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.update_channel_username("TheProgrammer", username="TheProgrammer2")
    print(result)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>