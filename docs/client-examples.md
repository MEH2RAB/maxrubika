# مثال‌ها

<a id="messenger_examples_create_session"></a>
## [ساخت سشن (Session)](#messenger_examples_create_session)

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    pass
```

---

<a id="messenger_examples_get_chats"></a>
## [گرفتن همه چت‌ها](#messenger_examples_get_chats)

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    chats = app.get_chats()
    print(chats)
```

---

<a id="messenger_examples_show_chat_counts"></a>
## [نمایش تعداد چت‌ها](#messenger_examples_show_chat_counts)

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    chats = app.get_chats(show_chat_guids=True)
    guids = chats.chat_guids

    print("تعداد کل گفتگوهای شما:", chats.total)
    print("تعداد کانال‌ها:", sum(g.startswith("c0") for g in guids))
    print("تعداد گروه‌ها:", sum(g.startswith("g0") for g in guids))
    print("تعداد کاربران:", sum(g.startswith("u0") for g in guids))
    print("تعداد بات‌ها:", sum(g.startswith("b0") for g in guids))
    print("تعداد سرویس‌ها:", sum(g.startswith("s0") for g in guids))
```

---

<a id="messenger_examples_send_hello"></a>
## [پاسخ خودکار به سلام با افکت متحرک قلب](#messenger_examples_send_hello)

```python
import asyncio, time
from maxrubika import Messenger
from maxrubika.client.filters import IsMe, Text

app = Messenger("mySession")

last_reply = {}
sleep = 90

@app.on_new_message(Text("^سلام") |  Text("^درود") & ~IsMe())
async def i(event):
    user_guid = event.author_guid

    now = time.time()
    if user_guid in last_reply:
        if now - last_reply[user_guid] < sleep:
            return
        else:
            del last_reply[user_guid]

    last_reply[user_guid] = now

    send = await event.reply("درود! ❤")

    hearts = ["🩵", "💙", "💖", "🩶", "💚", "💛", "💜", "🖤", "🤍", "🤎"]
    delay = 0.5
    total_time = 30
    steps = int(total_time / delay)

    for i in range(steps):
        heart = hearts[i % len(hearts)]
        try:
            await send.edit(f"درود! {heart}")
        except Exception:
            break
        await asyncio.sleep(delay)

app.run()
```

---

<a id="messenger_examples_self_bot_combined"></a>
## [ترکیب بات و سلف‌بات - دریافت لینک پست](#messenger_examples_self_bot_combined)

```python
import re
from maxrubika import Bot, Messenger
from maxrubika.bot.filters import Text

bot = Bot("Token") # توکن بات خود را اینجا وارد کنید.
app = Messenger("mySession") # سشن اکانت خود را اینجا وارد کنید.

app.start()
@bot.on_message(Text(re.compile(r'https://rubika\.ir/\w+/[A-Z]+', re.IGNORECASE)))
async def get_post(bot, event):
    link = event.text.strip()

    try:
        result = await app.get_channel_post_by_link(link)
        ask_spam_link = result.ask_spam_link

        if ask_spam_link:
            await event.reply(f"**لینک پست مورد نظر آماده شد:\n\n>**{ask_spam_link}")
        else:
            await event.reply("**خطایی رخ داد.**")

    except Exception as e:
        print(e)
        await event.reply(f"**لطفاً لینک معتبر وارد شود.**")

bot.run()
```

---

<a id="messenger_examples_dual_avatar"></a>
## [پروفایل دو تایی (Dual Avatar)](#messenger_examples_dual_avatar)

```python
from maxrubika import Messenger

with Messenger("mySession") as app:  # نام سشن خود را اینجا وارد کنید

    image1 = "IMG_20260711_083318_110.jpg"  # عکس دور
    image2 = "IMG_20260711_000458.jpg"  # عکس نزدیک

    target = "me"  # برای گروه یا کانال، لینک یا شناسه آن را وارد کنید

    result = app.upload_avatar(target, image2, image1)
    print(result)
```

---

<a id="messenger_examples_fake_action"></a>
## [نمایش چت اکشن فیک](#messenger_examples_fake_action)

```python
from maxrubika import Messenger
from maxrubika.client.filters import IsMe

app= Messenger("mySession") # نام سشن اکانت خود را اینجا وارد کنید

activity = "Typing" # نوع فعالیت را اینجا وارد کنید، می‌توانید کلمه Recording برای ضبط پیام صوتی یا Uploading را برای ارسال فایل، وارد کنید

@app.on_new_message(~IsMe())
async def i(event):
    await event.send_activity(activity)

app.run()
```

---

<a id="messenger_examples_check_join"></a>
## [بررسی عضویت کاربر (Check Join)](#messenger_examples_check_join)

```python
from maxrubika import Messenger

with Messenger("mySession") as app:

    target = "Link"  # شناسه، لینک یا آیدی کانال/گروه
    member = "@Online_User"  # شناسه یا نام‌کاربری کاربر

    result = app.check_join(target, member)
    print(result)
```

---

<a id="messenger_examples_group_clock_title"></a>
## [ساعت زنده در عنوان گروه](#messenger_examples_group_clock_title)

```python
import asyncio, pytz
from datetime import datetime, timedelta
from maxrubika import Messenger

SESSION = "mySession" # نام سشن اکانت خود اینجا وارد شود
CHAT_LINK = "" # لینک گروه خود اینجا وارد شود

SHOW_SECONDS = True # اگر می‌خواهید ثانیه نمایش داده نشود، False وارد کنید

IRAN_TZ = pytz.timezone("Asia/Tehran")

def now_iran() -> datetime:
    return datetime.now(IRAN_TZ)

async def main():
    async with Messenger(SESSION) as app:
        chat_guid = await app.get_guid(CHAT_LINK)

        info = await app.get_group_info(chat_guid)
        name = info.group_title

        try:
            await app.edit_group_info(chat_guid, event_messages=False)
            print("✅ پیام‌های شیشه‌ای غیرفعال شد.")
        except Exception as e:
            print(f"⚠️ خطا در غیرفعال کردن پیام شیشه‌ای: {e}")

        print(f"⏳ ساعت زنده روی اسم گروه '{name}' فعال شد...")

        while True:
            current_time = now_iran()
            
            if SHOW_SECONDS:
                time_str = current_time.strftime("%H:%M:%S")
                new_title = f"{name} | {time_str}"
                try:
                    await app.edit_group_title(chat_guid, new_title)
                except Exception as e:
                    print(f"❌ خطا در تغییر نام گروه: {e}")
                await asyncio.sleep(1)
                
            else:
                time_str = current_time.strftime("%H:%M")
                new_title = f"{name} | {time_str}"
                try:
                    await app.edit_group_title(chat_guid, new_title)
                except Exception as e:
                    print(f"❌ خطا در تغییر نام گروه: {e}")

                next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
                await asyncio.sleep((next_minute - current_time).total_seconds())

asyncio.run(main())
```

---

<a id="messenger_examples_channel_clock_title"></a>
## [ساعت زنده در عنوان کانال](#messenger_examples_channel_clock_title)

```python
import asyncio, pytz
from datetime import datetime, timedelta
from maxrubika import Messenger

SESSION = "mySession" # نام سشن اکانت خود اینجا وارد شود
CHAT_LINK = "" # لینک کانال خود اینجا وارد شود

IRAN_TZ = pytz.timezone("Asia/Tehran")

def now_iran() -> datetime:
    return datetime.now(IRAN_TZ)

async def main():
    async with Messenger(SESSION) as app:
        chat_guid = await app.get_guid(CHAT_LINK)

        info = await app.get_channel_info(chat_guid)
        name = info.channel.channel_title

        print(f"⏳ ساعت زنده روی اسم کانال '{name}' فعال شد...")

        while True:
            current_time = now_iran()
            time_str = current_time.strftime("%H:%M")
            new_title = f"{name} | {time_str}"

            try:
                result = await app.edit_channel_title(chat_guid, new_title)
                msg_id = result.message_id
                await app.delete_messages(chat_guid, [msg_id])
                
            except Exception as e:
                print(f"❌ خطا در تغییر نام کانال: {e}")

            next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
            await asyncio.sleep((next_minute - current_time).total_seconds())

asyncio.run(main())
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">
<a href="../client-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>
</div>