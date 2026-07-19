# مثال‌ها

<a id="create-session"></a>
## [ساخت سشن (Session)](#create-session)

```python
from maxrubika import Client

session = "mySession"
app = Client(session)

print(app.get_me())
```

---

<a id="get-chats"></a>
## [گرفتن همه چت‌ها](#get-chats)

```python
from maxrubika import Client

client = Client("mySession")
a = client.get_chats()
print(a)
```

---

<a id="self-bot"></a>
## [ترکیب سلف‌بات و بات (Self + Bot)](#self-bot)

```python
import re
from maxrubika import Bot, Client
from maxrubika.bot.filters import Text

bot = Bot("Token")  # توکن بات خود را اینجا وارد کنید
client = Client("mySession")  # سشن اکانت خود را اینجا وارد کنید

@bot.on_message(Text(re.compile(r'https://rubika\.ir/\w+/[A-Z]+', re.IGNORECASE)))
async def get_post(bot, event):
    link = event.text.strip()

    try:
        result = await client.get_channel_post_by_link(link)
        ask_spam_link = result.ask_spam_link

        if ask_spam_link:
            await event.reply(f"**لینک پست مورد نظر آماده شد:**\n\n{ask_spam_link}")
        else:
            await event.reply("**خطایی رخ داد.**")

    except Exception:
        await event.reply("**لطفاً لینک معتبر وارد شود.**")

bot.run()
```

---

<a id="dual-avatar"></a>
## [پروفایل دو تایی (Dual Avatar)](#dual-avatar)

```python
from maxrubika import Client

app = Client("mySession")  # نام سشن خود را اینجا وارد کنید

image1 = "IMG_20260711_083318_110.jpg"  # عکس دور
image2 = "IMG_20260711_000458.jpg"  # عکس نزدیک

target = "me"  # برای گروه یا کانال، لینک یا شناسه آن را وارد کنید

a = app.upload_avatar(target, image2, image1)
print(a)
```

---

<a id="check-join"></a>
## [بررسی عضویت کاربر (Check Join)](#check-join)

```python
from maxrubika import Client

client = Client("mySession")

target = "Link"  # شناسه، لینک یا آیدی کانال/گروه
member = "@Online_User"  # شناسه یا نام‌کاربری کاربر

a = client.check_join(target, member)
print(a)
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">
<a href="../client-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>
</div>