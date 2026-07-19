# مدیریت چت و لینک دعوت

---

<a id="client_join_chat"></a>
## [join_chat](#client_join_chat)

این متد برای عضویت در یک چت (گروه یا کانال) است. به صورت خودکار نوع چت را تشخیص داده و متد مناسب را فراخوانی می‌کند.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.join_chat("https://rubika.ir/joing/ABC123")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_leave_chat"></a>
## [leave_chat](#client_leave_chat)

این متد برای خروج از یک چت (گروه یا کانال) است.

**پارامتر:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.leave_chat("g0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_check_join"></a>
## [check_join](#client_check_join)

این متد برای بررسی عضویت یک کاربر یا بات در یک گروه یا کانال است. مقدار بازگشتی `True` یا `False` است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **member:** GUID یا نام‌کاربری کاربر یا بات مورد نظر.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    is_member = client.check_join("g0abc123...", member="@Online_User")
    print(is_member)

except Exception as e:
    print(e)
```

---

<a id="client_create_join_link"></a>
## [create_join_link](#client_create_join_link)

این متد برای ایجاد لینک دعوت برای یک گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **expire_time:** مدت زمان اعتبار لینک به ثانیه. (پیش‌فرض: None - بدون انقضا)
- **request_needed:** نیاز به تأیید درخواست عضویت. (پیش‌فرض: False)
- **title:** عنوان سفارشی برای لینک دعوت. (پیش‌فرض: None)
- **usage_limit:** حداکثر تعداد استفاده از لینک. (پیش‌فرض: 0 - نامحدود)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    link = client.create_join_link(
        "g0abc123...",
        request_needed=True,
        title="لینک ویژه",
        usage_limit=10
    )
    print(link)

except Exception as e:
    print(e)
```

---

<a id="client_get_join_links"></a>
## [get_join_links](#client_get_join_links)

این متد برای دریافت لیست لینک‌های دعوت یک گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **creator:** GUID یا نام‌کاربری سازنده لینک برای فیلتر. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    links = client.get_join_links("g0abc123...")
    print(links)

except Exception as e:
    print(e)
```

---

<a id="client_get_join_requests"></a>
## [get_join_requests](#client_get_join_requests)

این متد برای دریافت لیست درخواست‌های عضویت در یک گروه یا کانال است. به صورت خودکار تمام صفحات را پیمایش می‌کند.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **show_user_guids:** نمایش GUID کاربران در خروجی. (پیش‌فرض: False)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    requests = client.get_join_requests("g0abc123...")
    print(requests)

except Exception as e:
    print(e)
```

---

<a id="client_accept_join_request"></a>
## [accept_join_request](#client_accept_join_request)

این متد برای پذیرفتن یک درخواست عضویت در گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **user:** GUID یا نام‌کاربری کاربر درخواست‌دهنده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.accept_join_request("g0abc123...", user="@NewUser")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_reject_join_request"></a>
## [reject_join_request](#client_reject_join_request)

این متد برای رد کردن یک درخواست عضویت در گروه یا کانال است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **user:** GUID یا نام‌کاربری کاربر درخواست‌دهنده.

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.reject_join_request("g0abc123...", user="@SpamUser")
    print(result)

except Exception as e:
    print(e)
```

---

<a id="client_accept_all_join_requests"></a>
## [accept_all_join_requests](#client_accept_all_join_requests)

این متد برای پذیرفتن تمام درخواست‌های عضویت در یک گروه یا کانال به صورت یکجا است.

**پارامترها:**

- **chat:** GUID، لینک یا نام‌کاربری گروه یا کانال.
- **exclude:** GUID یا نام‌کاربری کاربرانی که نباید پذیرفته شوند. (پیش‌فرض: None)

**مثال:**

```python
from maxrubika import Client
client = Client("mySession")

try:
    result = client.accept_all_join_requests("g0abc123...")
    print(result)

except Exception as e:
    print(e)
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="/client-methods-chat" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>