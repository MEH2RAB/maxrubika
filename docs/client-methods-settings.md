# تنظیمات

---

<a id="messenger_get_privacy_setting"></a>
## [get_privacy_setting](#messenger_get_privacy_setting)

این متد برای دریافت تنظیمات حریم خصوصی فعلی کاربر به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        privacy = app.get_privacy_setting()
        print(privacy)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_notification_setting"></a>
## [get_notification_setting](#messenger_get_notification_setting)

این متد برای دریافت تنظیمات اعلان‌های فعلی حساب کاربری به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        notifications = app.get_notification_setting()
        print(notifications)

    except Exception as e:
        print(e)
```

---

<a id="messenger_set_notification"></a>
## [set_notification](#messenger_set_notification)

این متد برای به‌روزرسانی تنظیمات اعلان‌ها به کار می‌رود.

**پارامترها:**

- **user_notification:** فعال/غیرفعال کردن اعلان کاربران.
- **user_message_preview:** نمایش/عدم نمایش پیش‌نمایش پیام کاربران.
- **group_notification:** فعال/غیرفعال کردن اعلان گروه‌ها.
- **group_message_preview:** نمایش/عدم نمایش پیش‌نمایش پیام گروه‌ها.
- **channel_notification:** فعال/غیرفعال کردن اعلان کانال‌ها.
- **channel_message_preview:** نمایش/عدم نمایش پیش‌نمایش پیام کانال‌ها.
- **in_app_sound:** فعال/غیرفعال کردن صدای درون برنامه.
- **in_app_preview:** فعال/غیرفعال کردن پیش‌نمایش درون برنامه.
- **new_contacts:** فعال/غیرفعال کردن اعلان مخاطبین جدید.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_notification(
            user_notification=True,
            group_notification=False,
            in_app_sound=True
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_set_setting"></a>
## [set_setting](#messenger_set_setting)

این متد برای تنظیم حریم خصوصی و تنظیمات حذف خودکار به کار می‌رود.

**پارامترهای حریم خصوصی (مقادیر قابل قبول: `Everybody`، `MyContacts`، `Nobody`):**

- **show_my_last_online:** چه کسانی آخرین بازدید شما را ببینند.
- **show_my_phone_number:** چه کسانی شماره تلفن شما را ببینند.
- **show_my_profile_photo:** چه کسانی عکس پروفایل شما را ببینند.
- **link_forward_message:** چه کسانی لینک پیام‌های شما را فوروارد کنند.
- **can_join_chat_by:** چه کسانی بتوانند از طریق لینک به چت شما ملحق شوند.
- **show_my_birth_date:** چه کسانی تاریخ تولد شما را ببینند.
- **can_called_by:** چه کسانی بتوانند با شما تماس بگیرند.

**پارامترهای استثنا (exceptions):**

هر کدام می‌توانند یک دیکشنری با کلیدهای `include_users` و `exclude_users` باشند.

**پارامترهای حذف خودکار:**

- **auto_delete_messages:** مدت زمان حذف خودکار پیام‌ها.
- **inactive_account_delete:** حذف حساب پس از چند ماه عدم فعالیت. (مقادیر: 3، 6، 12، 24)

**مثال‌ها:**

۱. تنظیم آخرین بازدید فقط برای مخاطبین:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_setting(show_my_last_online="MyContacts")
        print(result)

    except Exception as e:
        print(e)
```

۲. تنظیم با استثنا:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_setting(
            show_my_last_online="Nobody",
            show_my_last_online_exceptions={
                "include_users": ["u0abc123..."]
            }
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_edit_show_last_online"></a>
## [edit_show_last_online](#messenger_edit_show_last_online)

این متد میانبری برای تنظیم نمایش آخرین بازدید است.

**پارامترها:**

- **setting:** `Everybody`، `MyContacts` یا `Nobody`.
- **exceptions:** دیکشنری استثناها (include_users و exclude_users).

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.edit_show_last_online("MyContacts")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_edit_show_phone_number"></a>
## [edit_show_phone_number](#messenger_edit_show_phone_number)

این متد میانبری برای تنظیم نمایش شماره تلفن است.

**پارامترها:**

- **setting:** `Everybody`، `MyContacts` یا `Nobody`.
- **exceptions:** دیکشنری استثناها.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.edit_show_phone_number("Nobody")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_edit_show_profile_photo"></a>
## [edit_show_profile_photo](#messenger_edit_show_profile_photo)

این متد میانبری برای تنظیم نمایش عکس پروفایل است.

**پارامترها:**

- **setting:** `Everybody`، `MyContacts` یا `Nobody`.
- **exceptions:** دیکشنری استثناها.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.edit_show_profile_photo("MyContacts")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_edit_show_birthday"></a>
## [edit_show_birthday](#messenger_edit_show_birthday)

این متد میانبری برای تنظیم نمایش تاریخ تولد است.

**پارامترها:**

- **setting:** `Everybody`، `MyContacts` یا `Nobody`.
- **exceptions:** دیکشنری استثناها.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.edit_show_birthday("Nobody")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_edit_can_join_chat_by"></a>
## [edit_can_join_chat_by](#messenger_edit_can_join_chat_by)

این متد میانبری برای تنظیم امکان ملحق شدن از طریق لینک است.

**پارامترها:**

- **setting:** `Everybody`، `MyContacts` یا `Nobody`.
- **exceptions:** دیکشنری استثناها.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.edit_can_join_chat_by("MyContacts")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_edit_can_called_by"></a>
## [edit_can_called_by](#messenger_edit_can_called_by)

این متد میانبری برای تنظیم امکان تماس گرفتن با شما است.

**پارامترها:**

- **setting:** `Everybody`، `MyContacts` یا `Nobody`.
- **exceptions:** دیکشنری استثناها.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.edit_can_called_by("Nobody")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_auto_delete_account"></a>
## [auto_delete_account](#messenger_auto_delete_account)

این متد برای تنظیم حذف خودکار حساب پس از مدت مشخصی عدم فعالیت به کار می‌رود.

**پارامتر:**

- **setting:** تعداد ماه‌ها. مقادیر قابل قبول: 3، 6، 12 یا 24.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.auto_delete_account(6)
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_update_my_name"></a>
## [update_my_name](#messenger_update_my_name)

این متد برای به‌روزرسانی نام و نام خانوادگی کاربر به کار می‌رود.

**پارامترها:**

- **first_name:** نام جدید. (حداکثر ۳۰ کاراکتر)
- **last_name:** نام خانوادگی جدید. (حداکثر ۵۰ کاراکتر)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.update_my_name(first_name="علی", last_name="حسینی")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_update_my_username"></a>
## [update_my_username](#messenger_update_my_username)

این متد برای به‌روزرسانی نام‌کاربری کاربر به کار می‌رود.

**پارامتر:**

- **username:** نام‌کاربری جدید. (حداقل ۷ و حداکثر ۳۲ کاراکتر، فقط حروف انگلیسی، اعداد و زیرخط)

**نکته:** نام‌کاربری نمی‌تواند با عدد یا زیرخط شروع شود یا به زیرخط ختم شود و باید حداقل شامل یک حرف باشد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.update_my_username("new_username")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_update_my_bio"></a>
## [update_my_bio](#messenger_update_my_bio)

این متد برای به‌روزرسانی بیوگرافی کاربر به کار می‌رود.

**پارامتر:**

- **bio:** متن بیوگرافی جدید. (حداکثر ۱۵۰ کاراکتر)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.update_my_bio("این بیوگرافی من است.")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_update_my_birthday"></a>
## [update_my_birthday](#messenger_update_my_birthday)

این متد برای به‌روزرسانی تاریخ تولد کاربر به کار می‌رود.

**پارامتر:**

- **birthday:** تاریخ تولد با فرمت YYYY-MM-DD.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.update_my_birthday("2000-05-20")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_update_my_profile"></a>
## [update_my_profile](#messenger_update_my_profile)

این متد برای به‌روزرسانی هم‌زمان چند بخش از پروفایل به کار می‌رود.

**پارامترها:**

- **first_name:** نام جدید.
- **last_name:** نام خانوادگی جدید.
- **bio:** بیوگرافی جدید.
- **birthday:** تاریخ تولد با فرمت YYYY-MM-DD.
- **location:** اطلاعات موقعیت مکانی شامل longitude، latitude و map_view.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.update_my_profile(
            first_name="علی",
            bio="برنامه‌نویس پایتون"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_two_passcode_status"></a>
## [get_two_passcode_status](#messenger_get_two_passcode_status)

این متد برای دریافت وضعیت تأیید دو مرحله‌ای حساب به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        status = app.get_two_passcode_status()
        print(status)

    except Exception as e:
        print(e)
```

---

<a id="messenger_set_two_step_verification"></a>
## [set_two_step_verification](#messenger_set_two_step_verification)

این متد برای تنظیم تأیید دو مرحله‌ای به کار می‌رود.

**پارامترها:**

- **password:** رمز عبور فعلی.
- **hint:** راهنمایی برای یادآوری رمز. (پیش‌فرض: None)
- **recovery_email:** ایمیل بازیابی. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_two_step_verification(
            password="current_password",
            hint="رمز من"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_check_two_step_passcode"></a>
## [check_two_step_passcode](#messenger_check_two_step_passcode)

این متد برای بررسی صحت رمز تأیید دو مرحله‌ای به کار می‌رود.

**پارامتر:**

- **password:** رمز تأیید دو مرحله‌ای.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.check_two_step_passcode("my_password")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_turn_off_two_step"></a>
## [turn_off_two_step](#messenger_turn_off_two_step)

این متد برای غیرفعال کردن تأیید دو مرحله‌ای به کار می‌رود.

**پارامتر:**

- **password:** رمز تأیید دو مرحله‌ای فعلی.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.turn_off_two_step("my_password")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_change_password"></a>
## [change_password](#messenger_change_password)

این متد برای تغییر رمز عبور حساب به کار می‌رود.

**پارامترها:**

- **password:** رمز عبور فعلی.
- **new_password:** رمز عبور جدید.
- **new_hint:** راهنمایی جدید برای رمز.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.change_password(
            password="old_pass",
            new_password="new_pass",
            new_hint="راهنمایی جدید"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_recovery_email"></a>
## [recovery_email](#messenger_recovery_email)

این متد برای بازیابی حساب با استفاده از ایمیل بازیابی به کار می‌رود.

**پارامترها:**

- **password:** رمز عبور فعلی.
- **recovery_email:** ایمیل بازیابی.

**نکته:** این متد یک کد به ایمیل ارسال می‌کند و سپس از کاربر درخواست وارد کردن کد را می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.recovery_email(
            password="my_password",
            recovery_email="example@email.com"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_request_change_phone_number"></a>
## [request_change_phone_number](#messenger_request_change_phone_number)

این متد برای درخواست تغییر شماره تلفن حساب به کار می‌رود.

**پارامتر:**

- **new_phone_number:** شماره تلفن جدید.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.request_change_phone_number("09123456789")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_verify_change_phone_number"></a>
## [verify_change_phone_number](#messenger_verify_change_phone_number)

این متد برای تأیید تغییر شماره تلفن با کد دریافتی به کار می‌رود.

**پارامترها:**

- **code:** کد تأیید ارسال شده.
- **hash:** هش دریافتی از متد `request_change_phone_number`.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.verify_change_phone_number(
            code="12345",
            hash="hash_from_request"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_my_sessions"></a>
## [get_my_sessions](#messenger_get_my_sessions)

این متد برای دریافت اطلاعات نشست‌های فعال حساب کاربری به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        sessions = app.get_my_sessions()
        print(sessions)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_unconfirmed_sessions"></a>
## [get_unconfirmed_sessions](#messenger_get_unconfirmed_sessions)

این متد برای دریافت نشست‌های تأیید نشده (در انتظار تأیید) حساب کاربری به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        pending = app.get_unconfirmed_sessions()
        print(pending)

    except Exception as e:
        print(e)
```

---

<a id="messenger_confirm_unconfirmed_session"></a>
## [confirm_unconfirmed_session](#messenger_confirm_unconfirmed_session)

این متد برای تأیید یک نشست در انتظار به کار می‌رود.

**پارامتر:**

- **unconfirmed_session_key:** کلید نشست تأیید نشده.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.confirm_unconfirmed_session("session_key_123")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_deny_unconfirmed_session"></a>
## [deny_unconfirmed_session](#messenger_deny_unconfirmed_session)

این متد برای رد یک نشست در انتظار به کار می‌رود.

**پارامتر:**

- **unconfirmed_session_key:** کلید نشست تأیید نشده.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.deny_unconfirmed_session("session_key_123")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_terminate_session"></a>
## [terminate_session](#messenger_terminate_session)

این متد برای پایان دادن به یک نشست خاص به کار می‌رود.

**پارامتر:**

- **session_key:** کلید نشست.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.terminate_session("session_key_123")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_terminate_other_sessions"></a>
## [terminate_other_sessions](#messenger_terminate_other_sessions)

این متد برای پایان دادن به تمام نشست‌های دیگر (به جز نشست فعلی) به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.terminate_other_sessions()
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_register_device"></a>
## [register_device](#messenger_register_device)

این متد برای ثبت دستگاه فعلی در سرور روبیکا به کار می‌رود.

**پارامتر:**

- **device_model:** نام مدل دستگاه سفارشی. (پیش‌فرض: None - تشخیص خودکار)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.register_device()
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_logout"></a>
## [logout](#messenger_logout)

این متد برای خروج از نشست فعلی به کار می‌رود.

**توجه:** پس از اجرا، باید حرف `y` را برای تأیید وارد نمایید.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.logout()
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_account"></a>
## [delete_account](#messenger_delete_account)

این متد برای درخواست حذف دائمی حساب روبیکا به کار می‌رود.

**توجه:** پس از اجرا، یک پیامک تأیید حاوی لینک حذف حساب به شماره شما ارسال خواهد شد.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_account()
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_folders"></a>
## [get_folders](#messenger_get_folders)

این متد برای دریافت لیست پوشه‌ها (Folders) به کار می‌رود.

**پارامتر:**

- **last_state:** آخرین وضعیت برای دریافت پوشه‌ها. (پیش‌فرض: زمان فعلی منهای ۱۵۰ ثانیه)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        folders = app.get_folders()
        print(folders)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_suggested_folders"></a>
## [get_suggested_folders](#messenger_get_suggested_folders)

این متد برای دریافت پوشه‌های پیشنهادی کاربر به کار می‌رود.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        suggested = app.get_suggested_folders()
        print(suggested)

    except Exception as e:
        print(e)
```

---

<a id="messenger_add_folder"></a>
## [add_folder](#messenger_add_folder)

این متد برای افزودن یک پوشه جدید برای سازمان‌دهی چت‌ها به کار می‌رود.

**پارامترها:**

- **name:** نام پوشه.
- **include_chats:** چت‌هایی که در پوشه قرار گیرند (GUID، لینک یا نام‌کاربری).
- **exclude_chats:** چت‌هایی که از پوشه مستثنی شوند.
- **include_chat_types:** انواع چت برای شمول (مانند `User`، `Group`، `Channel`، `Bot`).
- **exclude_chat_types:** انواع چت برای استثنا.
- **is_add_to_top:** افزودن پوشه به بالای لیست. (پیش‌فرض: True)
- **suggestion_folder_id:** شناسه پوشه پیشنهادی.
- **folder_id:** شناسه پوشه.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.add_folder(
            name="دوستان",
            include_chats=["@User1", "@User2"]
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_folder"></a>
## [delete_folder](#messenger_delete_folder)

این متد برای حذف یک پوشه به کار می‌رود.

**پارامتر:**

- **folder_id:** شناسه پوشه.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_folder("folder_id_123")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_reorder_folder"></a>
## [reorder_folder](#messenger_reorder_folder)

این متد برای تغییر ترتیب پوشه‌ها به کار می‌رود.

**پارامتر:**

- **folder_ids:** یک شناسه یا لیستی از شناسه‌های پوشه‌ها به ترتیب جدید.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.reorder_folder(["id3", "id1", "id2"])
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_add_saved_music_playlist"></a>
## [add_saved_music_playlist](#messenger_add_saved_music_playlist)

این متد برای افزودن آهنگ به لیست موسیقی ذخیره شده در پروفایل به کار می‌رود.

**پارامترها:**

- **files:** یک مسیر فایل یا لیستی از مسیرهای فایل‌های موسیقی.
- **file_inlines:** لیست دیکشنری‌های file_inline از پیش آپلود شده.
- **time:** مدت زمان سفارشی به ثانیه. (در صورت عدم ارسال، تشخیص خودکار)
- **performer:** نام خواننده سفارشی. (در صورت عدم ارسال، تشخیص خودکار)
- **file_name:** نام فایل سفارشی. (در صورت عدم ارسال، از نام اصلی فایل استفاده می‌شود)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.add_saved_music_playlist(
            files=["song1.mp3", "song2.mp3"]
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_set_saved_music_playlist"></a>
## [set_saved_music_playlist](#messenger_set_saved_music_playlist)

این متد برای جایگزینی کامل لیست موسیقی ذخیره شده در پروفایل به کار می‌رود.

**پارامترها:**

- **files:** یک مسیر فایل یا لیستی از مسیرهای فایل‌های موسیقی.
- **file_inlines:** لیست دیکشنری‌های file_inline از پیش آپلود شده.
- **time:** مدت زمان سفارشی به ثانیه. (در صورت عدم ارسال، تشخیص خودکار)
- **performer:** نام خواننده سفارشی. (در صورت عدم ارسال، تشخیص خودکار)
- **file_name:** نام فایل سفارشی. (در صورت عدم ارسال، از نام اصلی فایل استفاده می‌شود)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_saved_music_playlist(
            files=["song1.mp3", "song2.mp3"]
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_delete_saved_music_playlist"></a>
## [delete_saved_music_playlist](#messenger_delete_saved_music_playlist)

این متد برای حذف آهنگ‌ها از لیست موسیقی ذخیره شده به کار می‌رود.

**پارامتر:**

- **position:** موقعیت آهنگ برای حذف. اگر None باشد، تمام آهنگ‌ها حذف می‌شوند. (پیش‌فرض: None)

**مثال‌ها:**

حذف یک آهنگ خاص:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_saved_music_playlist(position=1)
        print(result)

    except Exception as e:
        print(e)
```

حذف تمام آهنگ‌ها:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.delete_saved_music_playlist()
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_upgrade_to_api6"></a>
## [upgrade_to_api6](#messenger_upgrade_to_api6)

این متد برای ارتقاء از API نسخه ۵ به نسخه ۶ با تنظیم کلید عمومی RSA به کار می‌رود.

**پارامترها:**

- **save_as:** در صورت True بودن، auth و private_key در فایل JSON ذخیره می‌شود. (پیش‌فرض: True)
- **file_name:** نام فایل سفارشی برای ذخیره. (پیش‌فرض: `maxrubika_{auth[:10]}`)

**نکته:** این متد فقط با `api_version = 5` کار می‌کند.

**مثال:**

```python
from maxrubika import Messenger

with Messenger(auth = "ahkjbsawthnh...", api_version=5) as app:
    try:
        result = app.upgrade_to_api6()
        print(result)

    except Exception as e:
        print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>