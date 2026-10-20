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

<a id="messenger_string_session_guide"></a>
## [راهنمای استرینگ سشن (StringSession) و امنیت آن](#messenger_string_session_guide)

فایل سشن معمولی (Session) اطلاعات احراز هویت شما را در یک فایل روی دیسک ذخیره می‌کند. اما در برخی محیط‌ها (مثل سرورهای ابری، محیط‌های Docker یا اجرای ربات در جاهایی که دسترسی به فایل‌سیستم محدود است) نمی‌توانید به راحتی فایل سشن را نگه دارید.

**StringSession** یک راهکار جایگزین برای ذخیره و انتقال سشن است. به جای ذخیره در فایل، سشن به صورت یک **رشته رمزنگاری‌شده** در می‌آید و می‌توانید آن را در متغیرهای محیطی، فایل‌های تنظیمات یا هر جای دیگری نگه دارید.

### مزایای StringSession:

1. **عدم وابستگی به فایل‌سیستم:** می‌توانید سشن را در متغیرهای محیطی (Environment Variables) ذخیره کنید. مناسب برای Heroku، Docker، Railway و... .
2. **رمزنگاری با رمز عبور:** می‌توانید StringSession را با یک رمز عبور محافظت کنید. حتی اگر رشته لو برود، بدون رمز عبور قابل استفاده نیست.
3. **انتقال آسان:** می‌توانید StringSession را بین سیستم‌ها یا سرورهای مختلف کپی کنید.
4. **امنیت بیشتر:** اطلاعات حساس به‌صورت رمزنگاری‌شده ذخیره می‌شوند.
5. **اولویت بر فایل سشن:** اگر هم `session` و هم `string_session` را بدهید، `string_session` استفاده می‌شود.

### ساخت StringSession از سشن فعلی:

با استفاده از متد `get_string_session()` می‌توانید سشن فعلی خود را به یک رشته رمزنگاری‌شده تبدیل کنید:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    # بدون رمز عبور
    print(app.get_string_session())

    # با رمز عبور (امن‌تر)
    print(app.get_string_session(password="my_secret_password")
```

### استفاده از StringSession برای ساخت کلاینت:

```python
from maxrubika import Messenger

# بدون رمز عبور
with Messenger(string_session="ENCRYPTED_STRING") as app:
    print(app.get_me())

# با رمز عبور
with Messenger(string_session="ENCRYPTED_STRING", password="my_secret_password") as app:
    print(app.get_me())
```

### پارامتر مربوط به متد get_string_session:

| پارامتر | نوع | پیش‌فرض | توضیح |
|:------:|------|:------:|------|
| `password` | str | `None` | رمز عبور برای رمزگشایی `string_session` (در صورت استفاده). |

### نکات مهم:

1. **اولویت `string_session`:** اگر هم `session` و هم `string_session` را بدهید، `string_session` استفاده می‌شود.
2. **رمز عبور را نگه دارید:** اگر StringSession را با رمز عبور بسازید، **حتماً رمز را جای امنی نگه دارید.** بدون آن، StringSession قابل بازیابی نیست.
3. **مخصوص API v6:** استفاده از `string_session` فقط در `api_version=6` پشتیبانی می‌شود.
4. **سازگاری:** StringSession ساخته‌شده با کتابخانه MAXRubika فقط در همین کتابخانه قابل استفاده است.
5. **مدیریت خطا:** اگر StringSession نامعتبر باشد یا رمز عبور اشتباه باشد، خطای `SessionError` برگردانده می‌شود.

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

**توجه:**

- حداکثر تعداد متادیتا در هر پیام ۳۰ مورد است و می‌توانید از ترکیب‌های مختلف به‌صورت همزمان استفاده کنید.

- برای اعمال متادیتا بر روی پیام، می‌بایست علامت‌ها را اول و آخر **جمله** قرار دهید، اگر در اول و آخر متن قرار دهید، متادیتا اعمال نمی‌شود. (به جز علامت های بلاک کد)

---

<a id="messenger_creation_guide"></a>
## [راهنمای ایجاد کلاینت (Messenger)](#messenger_creation_guide)

برای ایجاد یک نمونه از کلاینت MAXRubika، می‌توانید از پارامترهای زیر استفاده کنید:

| پارامتر | توضیح | نوع | پیش‌فرض |
|:------:|------|:------:|:------:|
| `session` | نام یا مسیر فایل نشست (فقط api_version=6) | str | None |
| `string_session` | نشست به صورت رشته (اولویت بر `session`) | str | None |
| `password` | رمز عبور برای رمزگشایی `string_session` | str | None |
| `auth` | کلید احراز هویت | str | None |
| `private_key` | کلید خصوصی RSA (فقط api_version=6) | str یا bytes | None |
| `timeout` | مدت زمان انتظار برای درخواست (ثانیه) | int/float | 30 |
| `proxy` | آدرس پروکسی | str | None |
| `logger` | نمونه Logger | logging.Logger | None |
| `platform` | پلتفرم کلاینت | `web`, `pwa`, `android`, `rubx`, `rubikids`, `rubino` | pwa |
| `api_version` | نسخه API | 5 یا 6 | 6 |
| `max_retries` | حداکثر تعداد تلاش مجدد | int | 5 |
| `stop_on_first_match` | توقف پس از اولین تطابق هندلر | bool | False |
| `continue_on_error` | ادامه تلاش سایر پلتفرم‌ها در صورت خطای auth | bool | True |
| `show_welcome` | نمایش پیام خوش‌آمدگویی | bool | True |

### روش‌های احراز هویت

**روش ۱: استفاده از نشست (Session) - مخصوص API v6**
```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    # کد شما
    pass
```

**روش ۲: استفاده از String Session - مخصوص API v6**
```python
from maxrubika import Messenger

with Messenger(string_session="ENCRYPTED_STRING", password="my_pass") as app:
    # کد شما
    pass
```

**روش ۳: استفاده از Auth و Private Key - مخصوص API v6**
```python
from maxrubika import Messenger

with Messenger(
    auth="abcdefghijklmnopqrstuvwxyz12",
    private_key="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
) as app:
    # کد شما
    pass
```

**روش ۴: استفاده از Auth - مخصوص API v5**
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
1. در API v6 باید `session` یا `string_session` یا هر دو `auth` و `private_key` ارائه شود.
2. در API v5 فقط `auth` نیاز است و `private_key` پشتیبانی نمی‌شود.
3. مقدار `auth` باید دقیقاً ۳۲ حرف کوچک انگلیسی باشد.
4. `continue_on_error` در صورت True بودن، در صورت خطا دادن، پلتفرم‌های دیگر را امتحان می‌کند.
5. `Messenger` در واقع نسخهٔ جدیدتر و جایگزین `Client` است. استفاده از `Client` منقضی شده است.

---

<a id="messenger_connect_disconnect"></a>
## [نحوه اتصال و قطع اتصال](#messenger_connect_disconnect)

برای برقراری و قطع اتصال در کتابخانه MAXRubika، دو روش اصلی وجود دارد که بسته به نوع استفاده (Sync یا Async) و نیاز پروژه، می‌توانید یکی را انتخاب کنید.

### روش اول: استفاده از Context Manager

در این روش نیازی به صدا زدن متد اضافه‌ای برای قطع اتصال نیست؛ کافی است از `with` (در حالت Sync) یا `async with` (در حالت Async) استفاده کنید. اتصال به‌صورت خودکار برقرار می‌شود و در پایان بلوک، به‌درستی بسته خواهد شد.

#### حالت Sync:

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    me = app.get_me()
    print(me)
```

همچنین می‌توانید ابتدا شیء را بسازید و سپس از `with` استفاده کنید:

```python
from maxrubika import Messenger

app = Messenger("mySession")

with app:
    me = app.get_me()
    print(me)
```

#### حالت Async:

```python
import asyncio
from maxrubika import Messenger

async def main():
    async with Messenger("mySession") as app:
        me = await app.get_me()
        print(me)

asyncio.run(main())
```

یا ساخت جداگانه‌ی شیء و سپس استفاده از `async with`:

```python
import asyncio
from maxrubika import Messenger

async def main():
    app = Messenger("mySession")

    async with app:
        me = await app.get_me()
        print(me)

asyncio.run(main())
```

### روش دوم: صدا زدن متد start و disconnect یا close

در این روش، خودتان به‌صورت دستی اتصال را برقرار می‌کنید (با متد `start`) و در انتهای عملیات، با صدا زدن متد مناسب (`disconnect` در Sync و `close` در Async)، اتصال را می‌بندید.

#### حالت Sync:

```python
from maxrubika import Messenger

app = Messenger("mySession")

app.start()  # برقراری اتصال

me = app.get_me()
print(me)

app.disconnect()  # قطع اتصال در پایان عملیات
```

#### حالت Async:

```python
import asyncio
from maxrubika import Messenger

async def main():
    app = Messenger("mySession")
    
    await app.start()  # برقراری اتصال
    
    me = await app.get_me()
    print(me)
    
    await app.close()  # قطع اتصال در پایان عملیات

asyncio.run(main())
```

### نکته مهم:

استفاده از این روش‌ها فقط زمانی لازم است که بخواهید یک عملیات موقت با کتابخانه انجام دهید (مثلاً دریافت اطلاعات یک‌باره‌ی یک شیء).

اگر از دکوراتورها استفاده می‌کنید و وب‌سوکت را فعال کرده‌اید، نیازی به صدا زدن `disconnect` یا `close` یا استفاده از Context Manager نیست؛ زیرا کتابخانه خودش مدیریت اتصال را در طول اجرا به عهده دارد.

#### مثال: استفاده از دکوراتور (بدون نیاز به قطع دستی)

```python
from maxrubika import Messenger
from maxrubika.client.filters import Command

app = Messenger("mySession")

@app.on_new_message(Command("start"))
async def start(event):
    await event.reply("سلام، پیام شما دریافت شد.")

app.run()
```

در این حالت، کتابخانه به‌طور خودکار اتصال را در طول اجرای ربات مدیریت می‌کند و نیازی به فراخوانی متدهای `disconnect` یا `close` نخواهد بود.

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