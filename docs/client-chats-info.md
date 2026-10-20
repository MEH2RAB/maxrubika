# اطلاعات و دریافت چت

---

<a id="messenger_get_guid"></a>
## [get_guid](#messenger_get_guid)

این متد برای دریافت شناسه (GUID) یک کاربر، گروه، کانال یا بات از روی نام‌کاربری یا لینک است. این متد پایه‌ای و پرکاربرد است و بسیاری از متدهای دیگر از آن استفاده می‌کنند.

**پارامتر:**

- **chat:** نام‌کاربری، لینک گروه (`joing`)، لینک کانال (`joinc`) یا خود GUID.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    guid = app.get_guid("@Online_User")
    print(guid)
```

---

<a id="messenger_get_my_guid"></a>
## [get_my_guid](#messenger_get_my_guid)

این متد برای دریافت شناسه (GUID) اکانت خود کاربر استفاده می‌شود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    my_guid = app.get_my_guid()
    print(my_guid)
```

---

<a id="messenger_get_info_by_username"></a>
## [get_info_by_username](#messenger_get_info_by_username)

این متد برای دریافت اطلاعات اولیه یک چت (کاربر، بات یا کانال) از طریق نام‌کاربری است.

**پارامتر:**

- **username:** نام‌کاربری مورد نظر. (حداقل ۳ و حداکثر ۳۲ کاراکتر، فقط حروف انگلیسی، اعداد و زیرخط)

**نکته:** نام‌کاربری نمی‌تواند با عدد یا زیرخط شروع شود یا به زیرخط ختم شود و باید حداقل شامل یک حرف باشد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    info = app.get_info_by_username("Online_User")
    print(info)
```

---

<a id="messenger_get_info_by_link"></a>
## [get_info_by_link](#messenger_get_info_by_link)

این متد برای دریافت پیش‌نمایش اطلاعات گروه یا کانال از طریق لینک دعوت است.

**پارامتر:**

- **link:** لینک دعوت. باید با `https://rubika.ir/joing/` یا `https://rubika.ir/joinc/` شروع شود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    info = app.get_info_by_link("https://rubika.ir/joing/ABC123")
    print(info)
```

---

<a id="messenger_get_chat_info"></a>
## [get_chat_info](#messenger_get_chat_info)

این متد جامع برای دریافت اطلاعات کامل یک چت (کاربر، گروه، کانال، بات یا سرویس) است. با تشخیص خودکار نوع چت، متد مناسب را فراخوانی می‌کند.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**نکته:** این متد هوشمند است و بر اساس ورودی، به صورت خودکار از متدهای `get_user_info`، `get_bot_info`، `get_channel_info`، `get_group_info` یا `get_service_info` استفاده می‌کند.

**مثال‌ها:**

۱. دریافت اطلاعات کاربر:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    info = app.get_chat_info("@Online_User")
    print(info)
```

۲. دریافت اطلاعات گروه از لینک:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    info = app.get_chat_info("https://rubika.ir/joing/ABC123")
    print(info)
```

---

<a id="messenger_get_chats_info"></a>
## [get_chats_info](#messenger_get_chats_info)

این متد برای دریافت اطلاعات چند چت به صورت هم‌زمان با استفاده از GUID آنها است.

**پارامتر:**

- **chats:** یک GUID یا لیستی از GUIDهای چت‌ها.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    info = app.get_chats_info(["u0abc123...", "g0xyz789...", "c0def456..."])
    print(info)
```

---

<a id="messenger_get_chats"></a>
## [get_chats](#messenger_get_chats)

این متد برای دریافت لیست تمام چت‌های حساب کاربری است. به صورت خودکار تمام صفحات را پیمایش می‌کند.

**پارامترها:**

- **show_chat_guids:** در صورت True بودن، GUID چت‌ها در خروجی نمایش داده می‌شود. (پیش‌فرض: False)
- **auto_start_id:** در صورت True بودن، تمام صفحات به صورت خودکار دریافت می‌شوند. در صورت False بودن، فقط یک صفحه با `start_id` دریافت می‌شود. (پیش‌فرض: True)
- **start_id:** شناسه شروع برای صفحه‌بندی. فقط زمانی استفاده می‌شود که `auto_start_id=False` باشد. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    chats = app.get_chats()
    print(chats)
```

---

<a id="messenger_get_chats_updates"></a>
## [get_chats_updates](#messenger_get_chats_updates)

این متد برای دریافت به‌روزرسانی‌های چت‌ها (مانند پیام‌های جدید، تغییرات و...) است.

**پارامتر:**

- **state:** وضعیت زمانی برای دریافت به‌روزرسانی‌ها. (پیش‌فرض: ۱۵۰ ثانیه قبل از زمان فعلی)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    updates = app.get_chats_updates()
    print(updates)
```

---

<a id="messenger_get_related_chats"></a>
## [get_related_chats](#messenger_get_related_chats)

این متد برای دریافت چت‌های مرتبط با یک چت خاص (مانند گروه‌ها و کانال‌های مرتبط) است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    related = app.get_related_chats("g0abc123...")
    print(related)
```

---

<a id="messenger_get_profile_link_items"></a>
## [get_profile_link_items](#messenger_get_profile_link_items)

این متد برای دریافت آیتم‌های لینک پروفایل یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری چت.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    items = app.get_profile_link_items("u0abc123...")
    print(items)
```

---

<a id="messenger_get_chat_ads"></a>
## [get_chat_ads](#messenger_get_chat_ads)

این متد برای دریافت اطلاعات تبلیغاتی چت‌ها است.

**پارامتر:**

- **state:** وضعیت زمانی برای فیلتر. (پیش‌فرض: ۱۵۰ ثانیه قبل از زمان فعلی)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    ads = app.get_chat_ads()
    print(ads)
```

---

<a id="messenger_search_global_chats"></a>
## [search_global_chats](#messenger_search_global_chats)

این متد برای جستجوی سراسری در میان چت‌ها (کاربران، کانال‌ها و...) بر اساس متن است.

**پارامترها:**

- **text:** متن مورد جستجو.
- **filter_type:** فیلتر نتایج بر اساس نوع. مقادیر قابل قبول: `User`، `Channel`، `Bot` یا لیستی از آن‌ها. (پیش‌فرض: None)
- **start_id:** شناسه شروع برای صفحه‌بندی. (پیش‌فرض: None)

**مثال‌ها:**

جستجوی ساده:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    results = app.search_global_chats("برنامه‌نویس")
    print(results)
```

جستجو با فیلتر نوع:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    results = app.search_global_chats(
        "برنامه‌نویس",
        filter_type=["Channel", "Bot"]
    )
    print(results)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-chat/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>