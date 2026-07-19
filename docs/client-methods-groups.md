# گروه‌ها

---

<a id="client_get_group_info"></a>
## [get_group_info](#client_get_group_info)

این متد برای دریافت اطلاعات یک گروه به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**نکته:** شناسه گروه باید با `g0` شروع شده و ۳۲ کاراکتر باشد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_group_info("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD")
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_get_group_link"></a>
## [get_group_link](#client_get_group_link)

این متد برای دریافت لینک خصوصی یک گروه به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    link = client.get_group_link("g0G3R19035f77574adc0127ab97c999c")
    print(link)

except Exception as e:
    print(e)
```

---

<a id="client_set_group_link"></a>
## [set_group_link](#client_set_group_link)

این متد برای تنظیم لینک خصوصی یک گروه به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_group_link("g0G3R19035f77574adc0127ab97c999c")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_get_group_online_count"></a>
## [get_group_online_count](#client_get_group_online_count)

این متد برای دریافت تعداد اعضای آنلاین یک گروه به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    count = client.get_group_online_count("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD")
    print(count)

except Exception as e:
    print(e)
```

---

<a id="client_create_group"></a>
## [create_group](#client_create_group)

این متد برای ایجاد یک گروه جدید به کار می‌رود.

**پارامترها:**

- **title:** عنوان گروه. (حداکثر ۶۰ کاراکتر، نمی‌تواند خالی باشد)
- **members:** یک عضو یا لیستی از اعضا (GUID یا نام‌کاربری). حداقل یک عضو الزامی است.
- **description:** متن توضیحات گروه. (حداکثر ۳۰۰ کاراکتر، پیش‌فرض: None)

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن؛ کتابخانه هر دو حالت را می‌پذیرد.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.create_group(
        title="گروه تست",
        members=["Online_User", "@ShowInfoBot", "u0HryBf03dbfba68374497983bc850a0"],
        description="این یک گروه تست است."
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_delete_group"></a>
## [delete_group](#client_delete_group)

این متد برای حذف یک گروه به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**توجه:** پس از اجرای این متد، برای تکمیل عملیات حذف، باید حرف `y` را در کنسول وارد نمایید.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.delete_group("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_join_group"></a>
## [join_group](#client_join_group)

این متد برای عضویت در یک گروه از طریق لینک دعوت به کار می‌رود.

**پارامتر:**

- **group:** لینک دعوت گروه. باید با `https://rubika.ir/joing/` شروع شود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.join_group("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_leave_group"></a>
## [leave_group](#client_leave_group)

این متد برای خروج از یک گروه به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.leave_group("g0CyVlK0cae995e5b46031170a358a4e")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_edit_group_info"></a>
## [edit_group_info](#client_edit_group_info)

این متد برای ویرایش تنظیمات یک گروه به کار می‌رود.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **title:** عنوان جدید گروه. (حداکثر ۶۰ کاراکتر)
- **description:** توضیحات جدید گروه. (حداکثر ۳۰۰ کاراکتر)
- **slow_mode:** تنظیم حالت آهسته (محدودیت زمانی بین پیام‌ها).
- **event_messages:** فعال یا غیرفعال کردن پیام‌های رویدادی (ورود/خروج اعضا).
- **is_restricted_content:** محدود کردن محتوا (جلوگیری از اسکرین‌شات و ذخیره فایل).
- **reactions:** تنظیمات ری‌اکشن. مقادیر قابل قبول: `All`، `Disable`، یا لیستی از اعداد.
- **chat_history_for_new_members:** نمایش تاریخچه چت برای اعضای جدید. مقادیر: `Visible` یا `Hidden`.
- **restricted_period:** محدودیت زمانی برای ارسال پیام. لیستی از دیکشنری‌ها شامل `days_of_week`، `from_time` و `to_time`.

**مثال‌ها:**

ویرایش عنوان و توضیحات:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.edit_group_info(
        group="g0G3R19035f77574adc0127ab97c999c",
        title="گروه جدید",
        description="توضیحات جدید گروه"
    )
    print(result)

except Exception as e:
    print(e)
```

تنظیم ری‌اکشن‌های خاص:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.edit_group_info(
        group="g0G3R19035f77574adc0127ab97c999c",
        reactions=[1, 2, 6, 7, 8, 23, 44]
    )
    print(result)

except Exception as e:
    print(e)
```

تنظیم محدودیت زمانی:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.edit_group_info(
        group="g0G3R19035f77574adc0127ab97c999c",
        restricted_period=[{
            "days_of_week": ["Saturday", "Sunday"],
            "from_time": "00:00",
            "to_time": "06:00"
        }]
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_edit_group_title"></a>
## [edit_group_title](#client_edit_group_title)

این متد برای ویرایش عنوان یک گروه به کار می‌رود. این متد میانبری برای `edit_group_info` با پارامتر `title` است.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **title:** عنوان جدید گروه.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.edit_group_title("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD", "عنوان جدید")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_edit_group_timer"></a>
## [edit_group_timer](#client_edit_group_timer)

این متد برای تنظیم Slow Mode (حالت آهسته) یک گروه به کار می‌رود. این متد میانبری برای `edit_group_info` با پارامتر `slow_mode` است.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **timer:** مقدار Slow Mode جدید.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.edit_group_timer("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD", "30")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_edit_slow_mode"></a>
## [edit_slow_mode](#client_edit_slow_mode)

این متد نیز برای تنظیم Slow Mode یک گروه به کار می‌رود و عملکردی مشابه `edit_group_timer` دارد.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **slow_mode:** مقدار Slow Mode جدید.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.edit_slow_mode("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD", "60")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_get_group_admins"></a>
## [get_group_admins](#client_get_group_admins)

این متد برای دریافت فهرست کامل ادمین‌های یک گروه به کار می‌رود. این متد به صورت خودکار تمام صفحات را پیمایش می‌کند.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **show_admin_guids:** در صورت True بودن، شناسه (GUID) ادمین‌ها به صورت جداگانه در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    admins = client.get_group_admins("g0G3R19035f37574adc0127ab97c999c")
    print(admins)

except Exception as e:
    print(e)
```

---

<a id="client_get_group_admin_access"></a>
## [get_group_admin_access](#client_get_group_admin_access)

این متد برای دریافت سطح دسترسی‌های یک ادمین خاص در گروه به کار می‌رود.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **admin:** شناسه (GUID) یا نام‌کاربری ادمین مورد نظر.

**نکته:** تنها در صورتی می‌توانید دسترسی‌های یک ادمین را مشاهده کنید که خودتان ادمین یا مالک گروه باشید.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    access = client.get_group_admin_access("g0G3R19035f77574adc0127ab97c999c", "@Online_User")
    print(access)

except Exception as e:
    print(e)
```

---

<a id="client_get_group_default_access"></a>
## [get_group_default_access](#client_get_group_default_access)

این متد برای دریافت دسترسی‌های پیش‌فرض اعضای یک گروه به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    access = client.get_group_default_access("https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD")
    print(access)

except Exception as e:
    print(e)
```

---

<a id="client_set_group_default_access"></a>
## [set_group_default_access](#client_set_group_default_access)

این متد برای تنظیم دسترسی‌های پیش‌فرض اعضای یک گروه به کار می‌رود.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **access:** لیستی از دسترسی‌های مجاز. مقادیر قابل قبول:
    - `ViewMembers`: مشاهده اعضا
    - `ViewAdmins`: مشاهده ادمین‌ها
    - `SendMessages`: ارسال پیام
    - `AddMember`: افزودن عضو
    - `[]` (لیست خالی): غیرفعال کردن تمام دسترسی‌ها

**مثال‌ها:**

فقط اجازه ارسال پیام:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_group_default_access(
        "https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDSD",
        ["SendMessages"]
    )
    print(result)

except Exception as e:
    print(e)
```

بستن کامل گروه:

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.set_group_default_access(
        "g0G3R19035f77574adc0127ab97c999c",
        []
    )
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_lock_group"></a>
## [lock_group](#client_lock_group)

این متد برای قفل کردن گروه با غیرفعال کردن دسترسی ارسال پیام به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**نکته:** اگر گروه از قبل قفل باشد، پیام مناسبی بازگردانده می‌شود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.lock_group("g0G3R19035f77574adc0127ab97c999c")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_unlock_group"></a>
## [unlock_group](#client_unlock_group)

این متد برای باز کردن قفل گروه با فعال‌سازی مجدد دسترسی ارسال پیام به کار می‌رود.

**پارامتر:**

- **group:** شناسه (GUID) یا لینک گروه هدف.

**نکته:** اگر گروه از قبل باز باشد، پیام مناسبی بازگردانده می‌شود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.unlock_group("g0G3R19035f77574adc0127ab97c999c")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_get_group_members"></a>
## [get_group_members](#client_get_group_members)

این متد برای دریافت فهرست اعضای یک گروه به کار می‌رود.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **search_text:** عبارت مورد نظر برای جستجو در میان اعضا. (پیش‌فرض: None)
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال‌ها:**

۱. دریافت اعضای گروه:

```python
from maxrubika import Client
client = Client("mySession")

try:
    members = client.get_group_members("g0G3R19035f77574adc0127ab97c999c")
    print(members)

except Exception as e:
    print(e)
```

۲. جستجوی یک کاربر خاص:

```python
from maxrubika import Client
client = Client("mySession")

try:
    members = client.get_group_members("g0G3R19035f77574adc0127ab97c999c", search_text="@Online_User")
    print(members)

except Exception as e:
    print(e)
```

---

<a id="client_get_group_mention_list"></a>
## [get_group_mention_list](#client_get_group_mention_list)

این متد برای دریافت لیست منشن‌های یک گروه به کار می‌رود.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **search_mention:** عبارت جستجو برای فیلتر منشن‌ها. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    mentions = client.get_group_mention_list("g0G3R19035f77574adc0127ab97c999c")
    print(mentions)

except Exception as e:
    print(e)
```

---

<a id="client_get_unread_mentions"></a>
## [get_unread_mentions](#client_get_unread_mentions)

این متد برای دریافت منشن‌های خوانده‌نشده در یک گروه به کار می‌رود.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **max_id:** حداکثر شناسه پیام.
- **min_id:** حداقل شناسه پیام.
- **sort:** ترتیب مرتب‌سازی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    mentions = client.get_unread_mentions(
        "g0G3R19035f77574adc0127ab97c999c",
        max_id="1000",
        min_id="1"
    )
    print(mentions)

except Exception as e:
    print(e)
```

---

<a id="client_get_group_message_read_participants"></a>
## [get_group_message_read_participants](#client_get_group_message_read_participants)

این متد برای دریافت فهرست اعضایی که یک پیام خاص را در گروه خوانده‌اند به کار می‌رود.

**پارامترها:**

- **group:** شناسه (GUID) یا لینک گروه هدف.
- **message_id:** شناسه پیام مورد نظر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    participants = client.get_group_message_read_participants(
        "g0G3R19035f77574adc0127ab97c999c",
        message_id="123456"
    )
    print(participants)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>