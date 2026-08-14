# مثال‌ها

<a id="create-session"></a>
## [ساخت سشن (Session)](#create-session)

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    print(app.get_me())
```

---

<a id="get-chats"></a>
## [گرفتن همه چت‌ها](#get-chats)

```python
from maxrubika import Messenger

with Messenger("mySession") as app:
    chats = app.get_chats()
    print(chats)
```

---

<a id="self-bot"></a>
## [ترکیب سلف‌بات و بات (Self + Bot)](#self-bot)

```python
import re
from maxrubika import Bot, Messenger
from maxrubika.bot.filters import Text

bot = Bot("Token")  # توکن بات خود را اینجا وارد کنید

with Messenger("mySession") as app:  # سشن اکانت خود را اینجا وارد کنید

    @bot.on_message(Text(re.compile(r'https://rubika\.ir/\w+/[A-Z]+', re.IGNORECASE)))
    async def get_post(bot, event):
        link = event.text.strip()

        try:
            result = await app.get_channel_post_by_link(link)
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
from maxrubika import Messenger

with Messenger("mySession") as app:  # نام سشن خود را اینجا وارد کنید

    image1 = "IMG_20260711_083318_110.jpg"  # عکس دور
    image2 = "IMG_20260711_000458.jpg"  # عکس نزدیک

    target = "me"  # برای گروه یا کانال، لینک یا شناسه آن را وارد کنید

    result = app.upload_avatar(target, image2, image1)
    print(result)
```

---

<a id="check-join"></a>
## [بررسی عضویت کاربر (Check Join)](#check-join)

```python
from maxrubika import Messenger

with Messenger("mySession") as app:

    target = "Link"  # شناسه، لینک یا آیدی کانال/گروه
    member = "@Online_User"  # شناسه یا نام‌کاربری کاربر

    result = app.check_join(target, member)
    print(result)
```

---

<a id="check-join-channel-bot"></a>
## [ترکیب بات و سلف‌بات - بررسی عضویت کانال](#check-join-channel-bot)

```python
from maxrubika import Bot, Messenger
from maxrubika.bot.filters import ChatType

bot = Bot("Token")

with Messenger("mySession") as app:
    channel = "@TheMAXRubika"

    guid = app.get_guid(channel)
    info = app.get_channel_info(guid)
    title = info.channel.channel_title

    @bot.on_command("start", ChatType("user"))
    async def handler(bot, event):
        sender = event.author_id
        chat_info = await bot.get_chat_info(event.chat_id)
        username = getattr(chat_info.data.chat, 'username', None)

        if username:
            is_member = await app.check_join(guid, username)
            if is_member:
                await event.reply(f"✅ **شما در کانال {title} عضو هستید.**")
                return
            else:
                await event.reply(f"❌ **ابتدا در کانال زیر عضو شوید و سپس مجدد دستور /start را وارد کنید:**\n{channel}")
                return

        members = await app.get_channel_members(guid)
        sender_prefix = sender[:7]

        for member in members.in_chat_members:
            if member.member_guid[:7] == sender_prefix:
                await event.reply(f"✅ **شما در کانال {title} عضو هستید.**")
                return

        await event.reply(f"❌ **ابتدا در کانال زیر عضو شوید و سپس مجدد دستور /start را وارد کنید:**\n{channel}\n\n**اگر از قبل عضو بودید، ابتدا کانال را ترک کنید و دوباره عضو کانال شوید.**")

    bot.run(0)
```

---

<a id="check-join-group-bot"></a>
## [ترکیب بات و سلف‌بات - بررسی عضویت گروه](#check-join-group-bot)

```python
from maxrubika import Bot, Messenger
from maxrubika.bot.filters import ChatType

bot = Bot("Token")

with Messenger("mySession") as app:
    group = "https://rubika.ir/joing/..."

    guid = app.get_guid(group)
    info = app.get_group_info(guid)
    title = info.group.group_title

    @bot.on_command("start", ChatType("user"))
    async def handler(bot, event):
        sender = event.author_id
        chat_info = await bot.get_chat_info(event.chat_id)
        username = getattr(chat_info.data.chat, 'username', None)

        if username:
            is_member = await app.check_join(guid, username)
            if is_member:
                await event.reply(f"✅ **شما در گروه {title} عضو هستید.**")
                return
            else:
                await event.reply(f"❌ **ابتدا در گروه زیر عضو شوید و سپس مجدد دستور /start را وارد کنید:**\n{group}")
                return

        members = await app.get_group_members(guid)
        sender_prefix = sender[:7]

        for member in members.in_chat_members:
            if member.member_guid[:7] == sender_prefix:
                await event.reply(f"✅ **شما در گروه {title} عضو هستید.**")
                return

        await event.reply(f"❌ **ابتدا در گروه زیر عضو شوید و سپس مجدد دستور /start را وارد کنید:**\n{group}\n\n**اگر از قبل عضو بودید، ابتدا گروه را ترک کنید و دوباره عضو گروه شوید.**")

    bot.run(0)
```

---

<a id="group-clock-title"></a>
## [ساعت زنده در عنوان گروه](#group-clock-title)

```python
import time
from datetime import datetime
from maxrubika import Messenger

with Messenger("mySession") as app:
    GROUP = "link"
    TITLE = "اسم ثابت"

    GUID = app.get_guid(GROUP)

    show_seconds = input("آیا می‌خواهید ثانیه هم نمایش داده شود؟ (y/n): ").lower() == 'y'

    def update_time():
        time.sleep(0.5)
        while True:
            app.edit_group_info(GUID, event_messages=False)
            now = datetime.now()
            
            if show_seconds:
                time_str = now.strftime("%H:%M:%S")
                wait = 1
            else:
                target = now.replace(second=0, microsecond=0)
                time_str = target.strftime("%H:%M")
                wait = 60 - (now - target).total_seconds()
            
            app.edit_group_title(GUID, f"{TITLE} | {time_str}")
            time.sleep(wait)

    update_time()
```

---

<a id="channel-clock-title"></a>
## [ساعت زنده در عنوان کانال](#channel-clock-title)

```python
import time
from datetime import datetime
from maxrubika import Messenger

with Messenger("mySession") as app:
    CHANNEL = "@CodeYaran"
    TITLE = "نام ثابت"

    GUID = app.get_guid(CHANNEL)

    def update_time():
        time.sleep(0.5)
        while True:
            now = datetime.now()
            target = now.replace(second=0, microsecond=0)
            wait = 60 - (now - target).total_seconds()

            time_str = target.strftime("%H:%M")
            result = app.edit_channel_title(GUID, f"{TITLE} | {time_str}")
            app.delete_messages(GUID, result.message_id)

            time.sleep(wait)

    update_time()
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">
<a href="../client-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>
</div>