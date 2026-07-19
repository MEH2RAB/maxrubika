# اطلاعات و دریافت چت

---

<a id="client_get_guid"></a>
## [get_guid](#client_get_guid)

این متد برای دریافت شناسه (GUID) یک کاربر، گروه، کانال یا بات از روی نام‌کاربری یا لینک است. این متد پایه‌ای و پرکاربرد است و بسیاری از متدهای دیگر از آن استفاده می‌کنند.

**پارامتر:**

- **chat:** نام‌کاربری، لینک گروه (`joing`)، لینک کانال (`joinc`) یا خود GUID.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    guid = client.get_guid("@Online_User")
    print(guid)

except Exception as e:
    print(e)
```

---

<a id="client_get_info_by_username"></a>
## [get_info_by_username](#client_get_info_by_username)

این متد برای دریافت اطلاعات اولیه یک چت (کاربر، بات یا کانال) از طریق نام‌کاربری است.

**پارامتر:**

- **username:** نام‌کاربری مورد نظر. (حداقل ۳ و حداکثر ۳۲ کاراکتر)

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_info_by_username("Online_User")
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_get_info_by_link"></a>
## [get_info_by_link](#client_get_info_by_link)

این متد برای دریافت پیش‌نمایش اطلاعات گروه یا کانال از طریق لینک دعوت است.

**پارامتر:**

- **link:** لینک دعوت. باید با `https://rubika.ir/joing/` یا `https://rubika.ir/joinc/` شروع شود.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_info_by_link("https://rubika.ir/joing/ABC123")
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_get_chat_info"></a>
## [get_chat_info](#client_get_chat_info)

این متد جامع برای دریافت اطلاعات کامل یک چت (کاربر، گروه، کانال، بات یا سرویس) است. با تشخیص خودکار نوع چت، متد مناسب را فراخوانی می‌کند.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**نکته:** این متد هوشمند است و بر اساس ورودی، به صورت خودکار از متدهای `get_user_info`، `get_bot_info`، `get_channel_info`، `get_group_info` یا `get_service_info` استفاده می‌کند.

**مثال‌ها:**

۱. دریافت اطلاعات کاربر:

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_chat_info("@Online_User")
    print(info)

except Exception as e:
    print(e)
```

۲. دریافت اطلاعات گروه از لینک:

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_chat_info("https://rubika.ir/joing/ABC123")
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_get_chats_info"></a>
## [get_chats_info](#client_get_chats_info)

این متد برای دریافت اطلاعات چند چت به صورت هم‌زمان با استفاده از GUID آنها است.

**پارامتر:**

- **chats:** یک GUID یا لیستی از GUIDهای چت‌ها.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    info = client.get_chats_info(["u0abc123...", "g0xyz789...", "c0def456..."])
    print(info)

except Exception as e:
    print(e)
```

---

<a id="client_get_chats"></a>
## [get_chats](#client_get_chats)

این متد برای دریافت لیست تمام چت‌های حساب کاربری است. به صورت خودکار تمام صفحات را پیمایش می‌کند.

**پارامتر:**

- **show_chat_guids:** در صورت True بودن، GUID چت‌ها در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    chats = client.get_chats()
    print(chats)

except Exception as e:
    print(e)
```

---

<a id="client_get_chats_updates"></a>
## [get_chats_updates](#client_get_chats_updates)

این متد برای دریافت به‌روزرسانی‌های چت‌ها (مانند پیام‌های جدید، تغییرات و...) است.

**پارامتر:**

- **state:** وضعیت زمانی برای دریافت به‌روزرسانی‌ها. (پیش‌فرض: ۱۵۰ ثانیه قبل از زمان فعلی)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    updates = client.get_chats_updates()
    print(updates)

except Exception as e:
    print(e)
```

---

<a id="client_get_related_chats"></a>
## [get_related_chats](#client_get_related_chats)

این متد برای دریافت چت‌های مرتبط با یک چت خاص (مانند گروه‌ها و کانال‌های مرتبط) است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    related = client.get_related_chats("g0abc123...")
    print(related)

except Exception as e:
    print(e)
```

---

<a id="client_get_profile_link_items"></a>
## [get_profile_link_items](#client_get_profile_link_items)

این متد برای دریافت آیتم‌های لینک پروفایل یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    items = client.get_profile_link_items("u0abc123...")
    print(items)

except Exception as e:
    print(e)
```

---

<a id="client_get_chat_ads"></a>
## [get_chat_ads](#client_get_chat_ads)

این متد برای دریافت اطلاعات تبلیغاتی چت‌ها است.

**پارامتر:**

- **state:** وضعیت زمانی برای فیلتر. (پیش‌فرض: ۱۵۰ ثانیه قبل از زمان فعلی)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    ads = client.get_chat_ads()
    print(ads)

except Exception as e:
    print(e)
```

---

<a id="client_search_global_chats"></a>
## [search_global_chats](#client_search_global_chats)

این متد برای جستجوی سراسری در میان چت‌ها (کاربران، کانال‌ها و...) بر اساس متن است.

**پارامتر:**

- **text:** متن مورد جستجو.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    results = client.search_global_chats("برنامه‌نویس")
    print(results)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-chat/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>