# سکوت کردن کاربران

---

```python
from maxrubika import Bot
from maxrubika.bot.filters import ChatType, Text, IsReply, FromUser

token = "Token" # در این خط توکن بات خود را وارد کنید
sender_id = "" # در این خط سندر آیدی اکانت خود را وارد کنید

bot = Bot(token)
messages = {}
muted = []

@bot.middleware()
async def process_all_messages(bot, event, call_next):
    chat_id = str(event.chat_id)
    msg_id = event.msg_id
    author_id = event.author_id

    if chat_id not in messages:
        messages[chat_id] = []

    messages[chat_id].append({
        "msg_id": msg_id,
        "sender_id": author_id
    })

    if author_id in muted:
        try:
            await event.delete()
            return
        except: pass

    await call_next()

@bot.on_new_message(Text("^سکوت$") & ChatType("group") & FromUser(sender_id) & IsReply())
async def mute_user(bot, event):
    chat_id = str(event.chat_id)
    reply_to_id = event.reply_to_message_id

    target_sender = None
    for msg in messages.get(chat_id, []):
        if msg["msg_id"] == reply_to_id:
            target_sender = msg["sender_id"]
            break

    if not target_sender:
        await event.reply("**کاربر مورد نظر پیدا نشد!**")
        return

    if target_sender == sender_id:
        await event.reply("**شما نمی‌توانید خودتان را سکوت کنید!**")
        return

    if target_sender in muted:
        await event.reply(f"**[کاربر مورد نظر]({target_sender}) قبلاً سکوت شده است.**")
        return

    muted.append(target_sender)
    await event.reply(f"**[کاربر مورد نظر]({target_sender}) با موفیقت سکوت شد، از این پس پیام های کاربر از گروه حذف می‌شود.**")

@bot.on_new_message(Text("^لغو سکوت$") & ChatType("group") & FromUser(sender_id) & IsReply())
async def unmute_user(bot, event):
    chat_id = str(event.chat_id)
    reply_to_id = event.reply_to_message_id

    target_sender = None
    for msg in messages.get(chat_id, []):
        if msg["msg_id"] == reply_to_id:
            target_sender = msg["sender_id"]
            break

    if not target_sender:
        await event.reply("**کاربر مورد نظر پیدا نشد!**")
        return

    if target_sender in muted:
        muted.remove(target_sender)
        await event.reply(f"**سکوت [کاربر مورد نظر]({target_sender}) لغو شد.**")
    else:
        await event.reply(f"**[کاربر مورد نظر]({target_sender}) سکوت نبوده است.**")

bot.run()
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-examples/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به مثال‌ها</a>

</div>