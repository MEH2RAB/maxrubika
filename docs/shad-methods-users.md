# کاربران

---

<a id="shad_get_me"></a>
## [get_me](#shad_get_me)

این متد برای دریافت اطلاعات کاربر احراز هویت شده (خودتان) به کار می‌رود. اطلاعات بازگشتی شامل داده‌های کاربر به همراه اطلاعات احراز هویت می‌باشد.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    me = app.get_me()
    print(me)
```

---

<a id="shad_get_user_info"></a>
## [get_user_info](#shad_get_user_info)

این متد برای دریافت اطلاعات یک کاربر خاص به کار می‌رود. در صورت فراخوانی بدون پارامتر، اطلاعات کاربر فعلی بازگردانده می‌شود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر. (پیش‌فرض: None - اطلاعات خود کاربر)

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    info = app.get_user_info("@Online_User")
    print(info)
```

---

<a id="shad_check_user_username"></a>
## [check_user_username](#shad_check_user_username)

این متد برای بررسی وضعیت یک نام‌کاربری به کار می‌رود. با استفاده از آن می‌توان تعیین کرد که نام‌کاربری مورد نظر آزاد است یا پیش‌تر ثبت شده است.

**پارامتر:**

- **username:** نام‌کاربری مورد نظر برای بررسی.

**نکته:** تفاوتی ندارد که نام‌کاربری با `@` نوشته شود یا بدون آن.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    check = app.check_user_username("@Undefined")
    print(check)
```

---

<a id="shad_get_last_online"></a>
## [get_last_online](#shad_get_last_online)

این متد برای دریافت آخرین وضعیت آنلاین بودن یک کاربر به کار می‌رود. خروجی شامل نوع آنلاین بودن (دقیق یا تقریبی) و زمان مربوطه است.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    online = app.get_last_online("@Online_User")
    print(online)
```

---

<a id="shad_get_contacts_last_online"></a>
## [get_contacts_last_online](#shad_get_contacts_last_online)

این متد برای دریافت آخرین وضعیت آنلاین بودن چند کاربر به صورت هم‌زمان به کار می‌رود.

**پارامتر:**

- **users:** یک کاربر یا لیستی از کاربران (GUID یا نام‌کاربری).

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    online = app.get_contacts_last_online(["@User1", "@User2", "u0abc123..."])
    print(online)
```

---

<a id="shad_get_contacts"></a>
## [get_contacts](#shad_get_contacts)

این متد برای دریافت فهرست کامل مخاطبان ذخیره شده به کار می‌رود.

**پارامتر:**

- **show_user_guids:** در صورت True بودن، شناسه (GUID) کاربران به صورت جداگانه در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    contacts = app.get_contacts()
    print(contacts)
```

---

<a id="shad_add_contact"></a>
## [add_contact](#shad_add_contact)

این متد برای افزودن یک مخاطب جدید به دفترچه تلفن به کار می‌رود.

**پارامترها:**

- **phone_number:** شماره تلفن مخاطب.
- **first_name:** نام مخاطب.
- **last_name:** نام خانوادگی مخاطب. (پیش‌فرض: خالی)

**نکته:** شماره تلفن می‌تواند با فرمت‌های مختلفی (مانند `09123456789`، `+989123456789` یا `989123456789`) وارد شود.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.add_contact(
        phone_number="09123456789",
        first_name="علی",
        last_name="حسینی"
    )
    print(result)
```

---

<a id="shad_delete_contact"></a>
## [delete_contact](#shad_delete_contact)

این متد برای حذف یک مخاطب از دفترچه تلفن به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری مخاطب مورد نظر.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.delete_contact("@Online_User")
    print(result)
```

---

<a id="shad_reset_contacts"></a>
## [reset_contacts](#shad_reset_contacts)

این متد برای حذف تمام مخاطبین ذخیره شده از سرور به کار می‌رود.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.reset_contacts()
    print(result)
```

---

<a id="shad_get_contacts_updates"></a>
## [get_contacts_updates](#shad_get_contacts_updates)

این متد برای دریافت به‌روزرسانی‌های مربوط به مخاطبین (مانند تغییر نام، عکس پروفایل و ...) به کار می‌رود.

**پارامتر:**

- **state:** پارامتر فیلتر برای دریافت به‌روزرسانی‌ها. (پیش‌فرض: زمان فعلی منهای ۱۵۰ ثانیه)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    updates = app.get_contacts_updates()
    print(updates)
```

---

<a id="shad_block_user"></a>
## [block_user](#shad_block_user)

این متد برای مسدود کردن یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.block_user("@SpamUser")
    print(result)
```

---

<a id="shad_unblock_user"></a>
## [unblock_user](#shad_unblock_user)

این متد برای رفع مسدودیت یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.unblock_user("@SpamUser")
    print(result)
```

---

<a id="shad_get_blocked_users"></a>
## [get_blocked_users](#shad_get_blocked_users)

این متد برای دریافت فهرست کامل کاربران مسدود شده به کار می‌رود.

**پارامتر:**

- **show_user_guids:** در صورت True بودن، شناسه (GUID) کاربران به صورت جداگانه در خروجی نمایش داده می‌شود. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    blocked = app.get_blocked_users()
    print(blocked)
```

---

<a id="shad_unblock_all_users"></a>
## [unblock_all_users](#shad_unblock_all_users)

این متد برای رفع مسدودیت تمام کاربران مسدود شده به کار می‌رود. امکان مستثنی کردن برخی کاربران نیز وجود دارد.

**پارامتر:**

- **exclude:** یک کاربر یا لیستی از کاربران (GUID یا نام‌کاربری) که نباید از حالت مسدود خارج شوند. (پیش‌فرض: None)

**مثال‌ها:**

رفع مسدودیت همه کاربران:

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.unblock_all_users()
    print(result)
```

رفع مسدودیت همه به جز یک کاربر خاص:

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.unblock_all_users(exclude="@ImportantUser")
    print(result)
```

---

<a id="shad_get_common_groups"></a>
## [get_common_groups](#shad_get_common_groups)

این متد برای دریافت گروه‌های مشترک با یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    groups = app.get_common_groups("@Online_User")
    print(groups)
```

---

<a id="shad_delete_user_chat"></a>
## [delete_user_chat](#shad_delete_user_chat)

این متد برای حذف تاریخچه چت با یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**نکته:** شناسه آخرین پیام حذف‌شده به‌صورت خودکار توسط کتابخانه از آخرین پیام چت استخراج می‌شود و نیازی به پاس دادن دستی آن نیست.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.delete_user_chat("@TestUser")
    print(result)
```

---

<a id="shad_request_voice_call"></a>
## [request_voice_call](#shad_request_voice_call)

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
from maxrubika import Shad

with Shad("mySession") as app:
    call = app.request_voice_call("@Online_User")
    print(call)
```

---

<a id="shad_request_video_call"></a>
## [request_video_call](#shad_request_video_call)

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
from maxrubika import Shad

with Shad("mySession") as app:
    call = app.request_video_call("@Online_User")
    print(call)
```

---

<a id="shad_discard_call"></a>
## [discard_call](#shad_discard_call)

این متد برای پایان دادن به یک تماس در حال انجام به کار می‌رود.

**پارامترها:**

- **call_id:** شناسه تماس.
- **duration:** مدت زمان تماس به ثانیه. (پیش‌فرض: 0)
- **reason:** دلیل پایان تماس. مقادیر رایج: `Missed` و `Disconnect`. (پیش‌فرض: Disconnect)

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.discard_call(
        call_id="call_abc123",
        duration=120,
        reason="Disconnect"
    )
    print(result)
```

---

<a id="shad_get_top_users"></a>
## [get_top_users](#shad_get_top_users)

این متد برای دریافت لیست کاربران برتر (Top Users) به کار می‌رود.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    top = app.get_top_users()
    print(top)
```

---

<a id="shad_remove_from_top_users"></a>
## [remove_from_top_users](#shad_remove_from_top_users)

این متد برای حذف یک کاربر از لیست کاربران برتر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    result = app.remove_from_top_users("@TestUser")
    print(result)
```

---

<a id="shad_get_saved_music_playlist"></a>
## [get_saved_music_playlist](#shad_get_saved_music_playlist)

این متد برای دریافت لیست موسیقی‌های ذخیره شده یک کاربر به کار می‌رود.

**پارامتر:**

- **user:** شناسه (GUID) یا نام‌کاربری کاربر مورد نظر. همچنین می‌توان از مقادیر `me`، `cloud`، `self` یا `myself` برای دریافت لیست خود استفاده کرد.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    playlist = app.get_saved_music_playlist("me")
    print(playlist)
```

---

<a id="shad_get_contacts_stories"></a>
## [get_contacts_stories](#shad_get_contacts_stories)

این متد برای دریافت استوری‌های مخاطبین از صفحه چت به کار می‌رود.

**مثال:**

```python
from maxrubika import Shad

with Shad("mySession") as app:
    stories = app.get_contacts_stories()
    print(stories)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../shad-methods/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>