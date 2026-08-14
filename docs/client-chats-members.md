# اعضا و ادمین‌ها

---

<a id="messenger_add_members"></a>
## [add_members](#messenger_add_members)

این متد برای افزودن یک یا چند عضو به گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **members:** یک GUID/نام‌کاربری یا لیستی از GUID/نام‌کاربری اعضا.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.add_members(
            "g0abc123...",
            members=["@User1", "@User2", "u0xyz789..."]
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_ban_member"></a>
## [ban_member](#messenger_ban_member)

این متد برای مسدود کردن یک عضو از گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **member:** GUID یا نام‌کاربری عضو مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.ban_member("g0abc123...", member="@SpamUser")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_ban_members"></a>
## [ban_members](#messenger_ban_members)

این متد برای مسدود کردن چند عضو به صورت یکجا است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **members:** لیستی از GUID یا نام‌کاربری اعضا.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.ban_members("g0abc123...", members=["@User1", "@User2"])
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_unban_member"></a>
## [unban_member](#messenger_unban_member)

این متد برای رفع مسدودیت یک عضو از گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **member:** GUID یا نام‌کاربری عضو مورد نظر.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unban_member("g0abc123...", member="@SpamUser")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_unban_members"></a>
## [unban_members](#messenger_unban_members)

این متد برای رفع مسدودیت چند عضو به صورت یکجا است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **members:** لیستی از GUID یا نام‌کاربری اعضا.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unban_members("g0abc123...", members=["@User1", "@User2"])
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_unban_all_members"></a>
## [unban_all_members](#messenger_unban_all_members)

این متد برای رفع مسدودیت تمام اعضای مسدود شده یک گروه یا کانال به صورت یکجا است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **exclude:** GUID یا نام‌کاربری اعضایی که نباید رفع مسدود شوند. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unban_all_members("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_banned_members"></a>
## [get_banned_members](#messenger_get_banned_members)

این متد برای دریافت لیست اعضای مسدود شده یک گروه یا کانال است. به صورت خودکار تمام صفحات را پیمایش می‌کند.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **show_member_guids:** نمایش GUID اعضا در خروجی. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        banned = app.get_banned_members("g0abc123...")
        print(banned)

    except Exception as e:
        print(e)
```

---

<a id="messenger_clear_black_list"></a>
## [clear_black_list](#messenger_clear_black_list)

این متد برای پاک‌سازی لیست سیاه (رفع مسدودیت تمام اعضا) در یک گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **exclude:** GUID یا نام‌کاربری اعضایی که نباید رفع مسدود شوند. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.clear_black_list("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_set_admin"></a>
## [set_admin](#messenger_set_admin)

این متد برای تنظیم یک عضو به عنوان ادمین در گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **member:** GUID یا نام‌کاربری عضو.
- **access:** لیست دسترسی‌های مجاز یا یک دسترسی تکی.
    - **گروه:** `SetAdmin`, `BanMember`, `ChangeInfo`, `PinMessages`, `SetJoinLink`, `SetMemberAccess`, `DeleteGlobalAllMessages`
    - **کانال:** `ChangeInfo`, `DeleteGlobalAllMessages`, `PinMessages`, `SetAdmin`, `ViewAdmins`, `SetJoinLink`, `AddMember`, `ViewMembers`, `SendMessages`, `EditAllMessages`
- **custom_title:** عنوان سفارشی برای ادمین (فقط گروه). (پیش‌فرض: خالی)

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_admin(
            "g0abc123...",
            member="@NewAdmin",
            access=["BanMember", "PinMessages", "ChangeInfo"],
            custom_title="مدیر ارشد"
        )
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_unset_admin"></a>
## [unset_admin](#messenger_unset_admin)

این متد برای حذف ادمینی یک عضو در گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **member:** GUID یا نام‌کاربری عضو.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.unset_admin("g0abc123...", member="@OldAdmin")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_member_is_admin"></a>
## [member_is_admin](#messenger_member_is_admin)

این متد برای بررسی ادمین بودن یک عضو در گروه یا کانال است. مقدار بازگشتی `True` یا `False` است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **member:** GUID یا نام‌کاربری عضو.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        is_admin = app.member_is_admin("g0abc123...", member="@TestUser")
        print(is_admin)

    except Exception as e:
        print(e)
```

---

<a id="messenger_change_owner"></a>
## [change_owner](#messenger_change_owner)

این متد برای درخواست انتقال مالکیت یک چت (گروه یا کانال) به کاربر دیگر است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **new_owner:** GUID یا نام‌کاربری مالک جدید.

**نکته:** فقط مالک فعلی می‌تواند این درخواست را ارسال کند. مالک جدید باید درخواست را بپذیرد. این عملیات غیرقابل بازگشت است.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.change_owner("g0abc123...", new_owner="@NewOwner")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_accept_ownership_request"></a>
## [accept_ownership_request](#messenger_accept_ownership_request)

این متد برای پذیرفتن درخواست انتقال مالکیت یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.accept_ownership_request("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_reject_ownership_request"></a>
## [reject_ownership_request](#messenger_reject_ownership_request)

این متد برای رد کردن درخواست انتقال مالکیت یک چت است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.reject_ownership_request("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_cancel_change_owner"></a>
## [cancel_change_owner](#messenger_cancel_change_owner)

این متد برای لغو درخواست انتقال مالکیت توسط مالک فعلی است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.cancel_change_owner("g0abc123...")
        print(result)

    except Exception as e:
        print(e)
```

---

<a id="messenger_get_pending_owner"></a>
## [get_pending_owner](#messenger_get_pending_owner)

این متد برای دریافت اطلاعات مالک در انتظار (کسی که درخواست انتقال مالکیت برایش ارسال شده) است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        pending = app.get_pending_owner("g0abc123...")
        print(pending)

    except Exception as e:
        print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../client-methods-chat/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>