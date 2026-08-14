# توضیحات بیشتر

---

<a id="messenger_guid_guide"></a>
## [راهنمای شناسه‌های گفتگو (GUID)](#messenger_guid_guide)

شناسه‌های گفتگو در پلتفرم روبیکا از قاعده‌ی مشخصی پیروی می‌کنند که آگاهی از آن برای عملکرد صحیح کتابخانه ضروری است:

| نوع گفتگو | پیشوند | طول | مثال |
|:------:|------|:------:|:------|
| کاربر | u0 | ۳۲ کاراکتر | u0Hzgbk0ac24729c1d1a5d55c26ac3ef |
| بات | b0 | ۳۲ کاراکتر | b0Hzgbk0ac24729c1d1a5d55c29ac5ag |
| گروه | g0 | ۳۲ کاراکتر | g0G3R190567fa33c5f5ee7d399a104e8 |
| کانال | c0 | ۳۲ کاراکتر | c0Hzgbk0ac24729c1d1a5d55c26ac3ef |
| سرویس | s0 | ۳۲ کاراکتر | s0abcdefghijklmnopqrstuvwxyz12 |

### نکته:
شناسه گفتگو (GUID) با Chat ID که مختص سرور بات است متفاوت می‌باشد:
- **GUID:** شناسه عمومی و یکتا برای تمام بخش‌های روبیکا.
- **Chat ID:** مختص سرور بات است و برای ارتباط با API بات استفاده می‌شود.

---

<a id="messenger_session_guide"></a>
## [راهنمای فایل سشن (Session)](#messenger_session_guide)

### فایل سشن چیست؟

فایل نشست (Session) یک فایل است که کتابخانه پس از اولین ورود موفق (شماره تلفن و کد تأیید) ایجاد می‌کند. این فایل شامل اطلاعات احراز هویت شماست و در دفعات بعدی، دیگر نیازی به وارد کردن مجدد شماره و کد نخواهید داشت.

### مزایای استفاده از فایل سشن:
- عدم نیاز به ورود مجدد - پس از اولین بار، نیازی به وارد کردن شماره و کد نیست.
- سرعت بالا - اتصال سریع‌تر به سرور.
- امنیت - اطلاعات به صورت رمزنگاری شده ذخیره می‌شوند.
- سازگاری با سایر کتابخانه‌ها - فایل‌های نشست کتابخانه‌های دیگر (مانند rubpy و pyrubi) نیز قابل استفاده هستند.

---

<a id="messenger_metadata_guide"></a>
## [راهنمای متادیتا در متن پیام](#messenger_metadata_guide)

برای غنی‌سازی متن پیام‌ها و ایجاد قالب‌بندی پیشرفته، می‌توانید از متادیتاهای زیر استفاده کنید. هر متادیتا با علامت‌های مشخصی در ابتدا و انتهای عبارت اعمال می‌شود:

| نوع قالب‌بندی | علامت‌ها | مثال |
|:------:|------|------|
| برجسته (Bold) | `**` | `**سلام دوست عزیز!**` |
| کج (Italic) | `__` | `__این یک جمله تست است.__` |
| اسپویل (Spoiler) | `||` | `||متن اسپویل شده||` |
| نقل قول (Quote) | `>` (فقط ابتدا) | `> سلام!` |
| زیرخط (Underline) | `--` | `--تست--` |
| خط‌خورده (Strikethrough) | `~~` | `~~عالی و قوی~~` |
| مونو (Monospace) | `` ` `` | `` `بی‌نظیر` `` |
| بلاک کد (Code Block) | `` ``` `` | `` ``` کد ``` `` |
| هایپرلینک | `[متن](لینک)` | `[کلیک کنید](https://example.com)` |
| منشن (Mention) | `[متن](sender_id)` | `[مدیر](u0...)` |

### نمونه‌های ترکیبی پیشرفته

**مثال ۱ - ترکیب چند متادیتا:**
```
> __سلام__ [کاربر عزیز](u0) --به کتابخانه‌ی-- **MAXRubika** ||خوش آمدید||!
```

**مثال ۲ - متادیتای تودرتو:**
```
> ||__**این یک جمله از کتابخانه --MAXRubika-- است.**__||
```

**توجه:** حداکثر تعداد متادیتا در هر پیام ۳۰ مورد است و می‌توانید از ترکیب‌های مختلف به‌صورت همزمان استفاده کنید.

---

<a id="messenger_creation_guide"></a>
## [راهنمای ایجاد کلاینت (Messenger)](#messenger_creation_guide)

برای ایجاد یک نمونه از کلاینت MAXRubika، می‌توانید از پارامترهای زیر استفاده کنید:

| پارامتر | توضیح | نوع | پیش‌فرض |
|:------:|------|:------:|:------:|
| `session` | نام یا مسیر فایل نشست | str | None |
| `auth` | کلید احراز هویت | str | None |
| `private_key` | کلید خصوصی RSA | str یا bytes | None |
| `timeout` | مدت زمان انتظار برای درخواست (ثانیه) | int/float | 30 |
| `proxy` | آدرس پروکسی | str | None |
| `logger` | نمونه Logger | logging.Logger | None |
| `platform` | پلتفرم کلاینت | `web`, `pwa`, `android`, `rubx`, `rubikids`, `rubino` | web |
| `api_version` | نسخه API | 5 یا 6 | 6 |
| `max_retries` | حداکثر تعداد تلاش مجدد | int | 5 |
| `stop_on_first_match` | توقف پس از اولین تطابق هندلر | bool | False |
| `continue_on_error` | ادامه تلاش سایر پلتفرم‌ها در صورت خطای auth | bool | True |

### روش‌های احراز هویت

**روش ۱: استفاده از نشست (Session) - مخصوص API v6**
```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    # کد شما
    pass
```

**روش ۲: استفاده از Auth و Private Key - مخصوص API v6**
```python
from maxrubika import Messenger

with Messenger(
    auth="abcdefghijklmnopqrstuvwxyz12",
    private_key="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
) as app:
    # کد شما
    pass
```

**روش ۳: استفاده از Auth - مخصوص API v5**
```python
from maxrubika import Messenger

with Messenger(
    auth="abcdefghijklmnopqrstuvwxyz12",
    api_version=5
) as app:
    # کد شما
    pass
```

### نکات:
1. در API v6 باید `session` یا هر دو `auth` و `private_key` ارائه شود.
2. در API v5 فقط `auth` نیاز است و `private_key` پشتیبانی نمی‌شود.
3. مقدار `auth` باید دقیقاً ۳۲ حرف کوچک انگلیسی باشد.
4. `continue_on_error` در صورت True بودن، در صورت خطای auth پلتفرم‌های دیگر را امتحان می‌کند.

---

<a id="messenger_input_methods_guide"></a>
## [راهنمای ورودی‌های متدها (Input Methods)](#messenger_input_methods_guide)

### انعطاف‌پذیری در شناسایی مخاطبان و گروه‌ها

تمامی متدهای کتابخانه **MAXRubika** که با گروه‌ها، کانال‌ها، گفتگوهای خصوصی یا هر نوع چت دیگری سروکار دارند، از **سه روش مختلف** برای شناسایی هدف پشتیبانی می‌کنند:

| روش ورودی | فرمت | مثال |
|:------:|------|------|
| **GUID** | شناسه یکتا با پیشوند `g0`, `c0`, `u0`, `b0` | `g0G3R190567fa33c5f5ee7d399a104e8` |
| **یوزرنیم** | نام کاربری با یا بدون `@` | `@MyChannel` یا `MyChannel` |
| **لینک دعوت** | لینک عضویت در گروه/کانال | `https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD` |

### ویژگی‌های کلیدی:
- **پشتیبانی از @:** در هنگام استفاده از یوزرنیم، وجود یا عدم وجود علامت `@` در ابتدا **تفاوتی ندارد** و کتابخانه به‌صورت خودکار آن را تشخیص می‌دهد.
- **تشخیص هوشمند:** کتابخانه به‌صورت خودکار نوع ورودی را تشخیص داده و پردازش مناسب را انجام می‌دهد.
- **سازگاری کامل:** تمامی متدهایی که شامل پارامترهای `chat`، `group`، `channel` هستند، از این قابلیت پشتیبانی می‌کنند.

### ⚠️ نکته مهم درباره ورودی‌های لینک و یوزرنیم

اگر برای ورودی چت از **لینک** یا **یوزرنیم** استفاده می‌کنید، بهتر است این روش را فقط در متدهایی به‌کار ببرید که **تعداد دفعات فراخوانی آن‌ها کم است**.

اما اگر قرار است یک متد را **بارها یا داخل حلقه** فراخوانی کنید، توصیه می‌شود ابتدا با استفاده از `get_guid` شناسه را **یک‌بار** دریافت کرده و سپس همان مقدار را به متدهای بعدی ارسال کنید.

**دلیل:** وقتی لینک یا یوزرنیم ارسال می‌کنید، کتابخانه ابتدا یک درخواست برای تبدیل آن به `guid` ارسال می‌کند و سپس درخواست اصلی متد را اجرا می‌کند. در نتیجه هر بار فراخوانی عملاً **دو درخواست** به API ارسال می‌شود.

**عواقب تکرار این روند:**
- افزایش غیرضروری تعداد درخواست‌ها به API
- کاهش عملکرد (Performance) برنامه
- افزایش احتمال رسیدن به محدودیت نرخ درخواست (Rate Limit)

**مثال غیربهینه:**
```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    for _ in range(5):
        app.get_chat_info("@YaserDev")
```

**مثال بهینه:**
```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    guid = app.get_guid("@YaserDev")
    for _ in range(5):
        app.get_chat_info(guid)
```

### مثال‌های عملی

**مثال ۱ - افزودن اعضا به گروه با روش‌های مختلف:**
```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.add_members(
            chat="g0abc123...",  # یا لینک دعوت
            members=["@User1", "User2", "u0xyz789..."]  # ترکیب یوزرنیم و GUID
        )
        print(result)
    except Exception as e:
        print(f"خطا: {e}")
```

**مثال ۲ - تنظیم ادمین با استفاده از لینک دعوت و یوزرنیم:**
```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        result = app.set_admin(
            chat="https://rubika.ir/joing/JGDJDBDJ0SRHELBQEBMZQFTPTKWSHDLCD",  # لینک دعوت
            member="@NewAdmin",  # یوزرنیم با @
            access=["BanMember", "PinMessages", "ChangeInfo"],
            custom_title="مدیر ارشد"
        )
        print(result)
    except Exception as e:
        print(f"خطا: {e}")
```

**مثال ۳ - ارسال پیام به کانال با GUID و یوزرنیم:**
```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    try:
        app.send_message(
            chat="c0Hzgbk0ac24729c1d1a5d85c26ac3ef",
            text="**پیام تستی**"
        )
        
        app.send_message(
            chat="MyChannel",
            text="__پیام دوم__"
        )
    except Exception as e:
        print(f"خطا: {e}")
```

### نکات مهم:
1. در تمامی متدها، پارامتر مربوط به شناسایی چت (`chat`, `group`, `channel`) از هر سه روش ورودی پشتیبانی می‌کند.
2. در پارامترهای مربوط به اعضا (`members`, `member`, `user`) نیز می‌توانید از GUID یا یوزرنیم استفاده کنید.
3. در صورت نامعتبر بودن ورودی، کتابخانه خطای مناسب را نمایش می‌دهد.

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">
<a href="../client-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>
</div>