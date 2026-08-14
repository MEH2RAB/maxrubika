# کاربران

---

<a id="messenger_get_me"></a>
## [get_me](#messenger_get_me)

این متد برای دریافت اطلاعات کاربر احراز هویت شده (خودتان) به کار می‌رود. اطلاعات بازگشتی شامل داده‌های کاربر به همراه اطلاعات احراز هویت می‌باشد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        me = app.get_me()
        print(me)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_user_info"></a>
## [get_user_info](#messenger_get_user_info)

این متد برای دریافت اطلاعات یک کاربر خاص به کار می‌رود. در صورت فراخوانی بدون پارامتر، اطلاعات کاربر فعلی بازگردانده می‌شود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر. (پیش‌فرض: None - اطلاعات خود کاربر)

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        info = app.get_user_info("@Online_User")
        print(info)

    except Exception as e:
        print(e)
```

---

<a id="messenger_check_user_username"></a>
## [check_user_username](#messenger_check_user_username)

این متد برای بررسی وضعیت یک نام‌کاربری به کار می‌رود. با استفاده از آن می‌توان تعیین کرد که نام‌کاربری مورد نظر آزاد است یا پیش‌تر ثبت شده است.

**پارامتر:**

- **username:** نام‌کاربری مورد نظر برای بررسی.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        check = app.check_user_username("@Undefined")
        print(check)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_last_online"></a>
## [get_last_online](#messenger_get_last_online)

این متد برای دریافت آخرین وضعیت آنلاین بودن یک کاربر به کار می‌رود. خروجی شامل نوع آنلاین بودن (دقیق یا تقریبی) و زمان مربوطه است.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        online = app.get_last_online("@Online_User")
        print(online)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_contacts_last_online"></a>
## [get_contacts_last_online](#messenger_get_contacts_last_online)

این متد برای دریافت آخرین وضعیت آنلاین بودن چند کاربر به صورت هم‌زمان به کار می‌رود.

**پارامتر:**

- **users:** یک کاربر یا لیستی از کاربران (GUID یا نام‌کاربری).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        online = app.get_contacts_last_online(["@User1", "@User2", "u0abc123..."])
        print(online)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_contacts"></a>
## [get_contacts](#messenger_get_contacts)

این متد برای دریافت فهرست کامل مخاطبان ذخیره شده به کار می‌رود.

**پارامتر:**

- **show_user_guids:** در صورت True بودن، شناسه (GUID) کاربران به صورت جداگانه در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        contacts = app.get_contacts()
        print(contacts)

    except Exception as e:
        print(e)
```

---

<a id="messenger_add_contact"></a>
## [add_contact](#messenger_add_contact)

این متد برای افزودن یک مخاطب جدید به دفترچه تلفن به کار می‌رود.

**پارامترها:**

- **phone_number:** شماره تلفن مخاطب.
- **first_name:** نام مخاطب.
- **last_name:** نام خانوادگی مخاطب. (پیش‌فرض: خالی)

**نکته:** شماره تلفن می‌تواند با فرمت‌های مختلفی (مانند `09123456789`، `+989123456789` یا `989123456789`) وارد شود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.add_contact(
            phone_number="09123456789",
            first_name="علی",
            last_name="حسینی"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_contact"></a>
## [delete_contact](#messenger_delete_contact)

این متد برای حذف یک مخاطب از دفترچه تلفن به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری مخاطب مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_contact("@Online_User")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_reset_contacts"></a>
## [reset_contacts](#messenger_reset_contacts)

این متد برای حذف تمام مخاطبین ذخیره شده از سرور به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.reset_contacts()
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_contacts_updates"></a>
## [get_contacts_updates](#messenger_get_contacts_updates)

این متد برای دریافت به‌روزرسانی‌های مربوط به مخاطبین (مانند تغییر نام، عکس پروفایل و ...) به کار می‌رود.

**پارامتر:**

- **state:** پارامتر فیلتر برای دریافت به‌روزرسانی‌ها. (پیش‌فرض: زمان فعلی منهای ۱۵۰ ثانیه)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        updates = app.get_contacts_updates()
        print(updates)

    except Exception as e:
        print(e)
```

---

<a id="messenger_block_user"></a>
## [block_user](#messenger_block_user)

این متد برای مسدود کردن یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.block_user("@SpamUser")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_unblock_user"></a>
## [unblock_user](#messenger_unblock_user)

این متد برای رفع مسدودیت یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unblock_user("@SpamUser")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_blocked_users"></a>
## [get_blocked_users](#messenger_get_blocked_users)

این متد برای دریافت فهرست کامل کاربران مسدود شده به کار می‌رود.

**پارامتر:**

- **show_user_guids:** در صورت True بودن، شناسه (GUID) کاربران به صورت جداگانه در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        blocked = app.get_blocked_users()
        print(blocked)

    except Exception as e:
        print(e)
```

---

<a id="messenger_unblock_all_users"></a>
## [unblock_all_users](#messenger_unblock_all_users)

این متد برای رفع مسدودیت تمام کاربران مسدود شده به کار می‌رود. امکان مستثنی کردن برخی کاربران نیز وجود دارد.

**پارامتر:**

- **exclude:** یک کاربر یا لیستی از کاربران (GUID یا نام‌کاربری) که نباید از حالت مسدود خارج شوند. (پیش‌فرض: None)

**مثال‌ها:**

رفع مسدودیت همه کاربران:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unblock_all_users()
        print(result)

    except Exception as e:
        print(e)
```

رفع مسدودیت همه به جز یک کاربر خاص:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unblock_all_users(exclude="@ImportantUser")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_common_groups"></a>
## [get_common_groups](#messenger_get_common_groups)

این متد برای دریافت گروه‌های مشترک با یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        groups = app.get_common_groups("@Online_User")
        print(groups)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_user_chat"></a>
## [delete_user_chat](#messenger_delete_user_chat)

این متد برای حذف تاریخچه چت با یک کاربر به کار می‌رود.

**پارامترها:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.
- **last_deleted_message_id:** شناسه آخرین پیام حذف‌شده.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_user_chat("@TestUser", last_deleted_message_id="123456")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_request_voice_call"></a>
## [request_voice_call](#messenger_request_voice_call)

این متد برای درخواست تماس صوتی با یک کاربر به کار می‌رود.

**پارامترها:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.
- **library_versions:** لیست نسخه‌های کتابخانه پشتیبانی شده. (پیش‌فرض: `['2.7.7', '2.4.4']`)
- **max_layer:** حداکثر لایه پروتکل. (پیش‌فرض: 92)
- **min_layer:** حداقل لایه پروتکل. (پیش‌فرض: 65)
- **sip_version:** نسخه SIP. (پیش‌فرض: 1)
- **support_call_out:** پشتیبانی از تماس خروجی. (پیش‌فرض: True)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        call = app.request_voice_call("@Online_User")
        print(call)

    except Exception as e:
        print(e)
```

---

<a id="messenger_request_video_call"></a>
## [request_video_call](#messenger_request_video_call)

این متد برای درخواست تماس تصویری با یک کاربر به کار می‌رود.

**پارامترها:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.
- **library_versions:** لیست نسخه‌های کتابخانه پشتیبانی شده. (پیش‌فرض: `['2.7.7', '2.4.4']`)
- **max_layer:** حداکثر لایه پروتکل. (پیش‌فرض: 92)
- **min_layer:** حداقل لایه پروتکل. (پیش‌فرض: 65)
- **sip_version:** نسخه SIP. (پیش‌فرض: 1)
- **support_call_out:** پشتیبانی از تماس خروجی. (پیش‌فرض: True)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        call = app.request_video_call("@Online_User")
        print(call)

    except Exception as e:
        print(e)
```

---

<a id="messenger_discard_call"></a>
## [discard_call](#messenger_discard_call)

این متد برای پایان دادن به یک تماس در حال انجام به کار می‌رود.

**پارامترها:**

- **call_id:** شناسه تماس.
- **duration:** مدت زمان تماس به ثانیه.
- **reason:** دلیل پایان تماس. مقادیر رایج: `Missed` و `Disconnect`. (پیش‌فرض: Disconnect)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.discard_call(
            call_id="call_abc123",
            duration=120,
            reason="Disconnect"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_top_users"></a>
## [get_top_users](#messenger_get_top_users)

این متد برای دریافت لیست کاربران برتر (Top Users) به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        top = app.get_top_users()
        print(top)

    except Exception as e:
        print(e)
```

---

<a id="messenger_remove_from_top_users"></a>
## [remove_from_top_users](#messenger_remove_from_top_users)

این متد برای حذف یک کاربر از لیست کاربران برتر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.remove_from_top_users("@TestUser")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_set_ask_spam"></a>
## [set_ask_spam](#messenger_set_ask_spam)

این متد برای انجام عملیات روی یک درخواست اسپم معلق به کار می‌رود.

**پارامترها:**

- **chat:** شناسه (GUID)، لینک یا نام‌کاربری کاربر، گروه یا کانال.
- **action:** عملیات مورد نظر:
    - برای کاربر: `AddToContact`، `BlockUser`، `Cancel`.
    - برای گروه/کانال: `ReportAndLeave`، `Cancel`.

**مثال‌ها:**

افزودن کاربر به مخاطبین:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_ask_spam("@UnknownUser", action="AddToContact")
        print(result)

    except Exception as e:
        print(e)
```

مسدود کردن کاربر:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_ask_spam("@SpamUser", action="BlockUser")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_saved_music_playlist"></a>
## [get_saved_music_playlist](#messenger_get_saved_music_playlist)

این متد برای دریافت لیست موسیقی‌های ذخیره شده یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر. همچنین می‌توان از `me` برای دریافت لیست خود استفاده کرد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        playlist = app.get_saved_music_playlist("me")
        print(playlist)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_contacts_stories"></a>
## [get_contacts_stories](#messenger_get_contacts_stories)

این متد برای دریافت استوری‌های مخاطبین از صفحه چت به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        stories = app.get_contacts_stories()
        print(stories)

    except Exception as e:
        print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>