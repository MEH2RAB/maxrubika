# مثال‌ها

<a id="shad_examples_create_session"></a>
## [ساخت سشن (Session)](#shad_examples_create_session)

```python
from maxrubika import Shad

with Shad("mySession") as app:
    pass
```

---

<a id="shad_examples_get_chats"></a>
## [گرفتن همه چت‌ها](#shad_examples_get_chats)

```python
from maxrubika import Shad

with Shad("mySession") as app:
    chats = app.get_chats()
    print(chats)
```

---

<a id="shad_examples_show_chat_counts"></a>
## [نمایش تعداد چت‌ها](#shad_examples_show_chat_counts)

```python
from maxrubika import Shad

with Shad("mySession") as app:
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

<a id="shad_examples_send_hello"></a>
## [پاسخ خودکار به سلام با افکت متحرک قلب](#shad_examples_send_hello)

```python
import asyncio, time
from maxrubika import Shad
from maxrubika.client.filters import IsMe, Text

app = Shad("mySession")

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

<a id="shad_examples_dual_avatar"></a>
## [پروفایل دو تایی (Dual Avatar)](#shad_examples_dual_avatar)

```python
from maxrubika import Shad

with Shad("mySession") as app:  # نام سشن خود را اینجا وارد کنید

    image1 = "IMG_20260711_083318_110.jpg"  # عکس دور
    image2 = "IMG_20260711_000458.jpg"  # عکس نزدیک

    target = "me"  # برای گروه یا کانال، لینک یا شناسه آن را وارد کنید

    result = app.upload_avatar(target, image2, image1)
    print(result)
```

---

<a id="shad_examples_fake_action"></a>
## [نمایش چت اکشن فیک](#shad_examples_fake_action)

```python
from maxrubika import Shad
from maxrubika.client.filters import IsMe

app = Shad("mySession") # نام سشن اکانت خود را اینجا وارد کنید

activity = "Typing" # نوع فعالیت را اینجا وارد کنید، می‌توانید کلمه Recording برای ضبط پیام صوتی یا Uploading را برای ارسال فایل، وارد کنید

@app.on_new_message(~IsMe())
async def i(event):
    await event.send_activity(activity)

app.run()
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">
<a href="../shad-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>
</div>