# فیلترها

فیلترها با `&` (AND)، `|` (OR) و `~` (NOT) ترکیب می‌شوند.

```python
# ترکیبِ چند فیلتر
@bot.on_message((Text("سلام") | Command("start")) & ChatType("group") & ~IsForwarded())
async def handler(bot, event):
    await event.reply("سلام!")

# OR - گروه یا کانال
@bot.on_new_message(ChatType("group") | ChatType("channel"))

# NOT - هر چیزی غیر از دستور
@bot.on_new_message(~Command())
```

---

<a id="bot_event_filters"></a>
## [فیلترهای نوع رویداد](#bot_event_filters)

| فیلتر | توضیح |
|------|------|
| `IsMessage()` | پیام جدید |
| `IsEdited()` | پیام ویرایش شده |
| `IsDeleted()` | پیام پاک شده |
| `IsCallback()` | کلیک دکمه اینلاین |
| `IsStartedBot()` | شروع بات توسط کاربر |
| `IsStoppedBot()` | توقف بات توسط کاربر |
| `IsEventData()` | رویدادهای EventData (مثل اضافه / حذف شدن بات) |
| `EventType("BotJoined")` | نوع خاص رویداد داخل EventData |

**مثال:**

```python
@bot.on_new_message(IsMessage())
async def new_msg(bot, event):
    await event.reply("این یک پیام جدید است!")

@bot.on_callback(IsCallback())
async def callback_handler(bot, event):
    await event.reply("روی دکمه کلیک شد!")

@bot.on_message(EventType("BotJoined"))
async def bot_joined(bot, event):
    await event.reply("بات به چت اضافه شد!")
```

---

<a id="bot_text_filters"></a>
## [فیلترهای متن](#bot_text_filters)

| فیلتر | توضیح | مثال |
|------|------|------|
| `IsText()` | فقط پیام متنی (بدون فایل) | - |
| `Text("pattern")` | متن شامل الگو باشد (regex) | `Text("سلام")` |
| `TextMatch("pattern")` | مانند Text + ذخیره match | `TextMatch(r"اسم (\w+)")` |
| `Command("name")` | متن با / شروع شود | `Command("start")` |
| `Command()` | هر دستوری | - |
| `Command(["start", "شروع"])` | چند نام | - |
| `Command("help", prefixes=["/", "!"])` | با prefix دلخواه | - |

**مثال:**

```python
@bot.on_new_message(IsText())
async def text_only(bot, event):
    await event.reply(f"متن: {event.text}")

@bot.on_new_message(TextMatch(r"اسم من (\w+) هست"))
async def name_catcher(bot, event):
    name = event.pattern_match.group(1)
    await event.reply(f"سلام {name}!")
```

---

<a id="bot_chat_user_filters"></a>
## [فیلترهای چت و کاربر](#bot_chat_user_filters)

| فیلتر | توضیح | مثال |
|------|------|------|
| `ChatType("user")` | فقط پیوی | - |
| `ChatType("group")` | فقط گروه | - |
| `ChatType("channel")` | فقط کانال | - |
| `ChatType(["group", "channel"])` | گروه یا کانال | - |
| `FromChat("g0abc...")` | چت خاص | - |
| `FromUser("u0abc...")` | کاربر خاص | - |
| `FromUser(["u0A", "u0B"])` | چند کاربر | - |
| `IsUser()` | پیوی کاربر | - |
| `IsGroup()` | گروه | - |
| `IsChannel()` | کانال | - |

**مثال:**

```python
@bot.on_new_message(ChatType("user"))
async def private_only(bot, event):
    await event.reply("این پیام در پیوی ارسال شده!")

@bot.on_new_message(FromChat("g0abc123def456ghi789jklmno123456"))
async def specific_group(bot, event):
    await event.reply("سلام به گروه خاص!")
```

---

<a id="bot_media_filters"></a>
## [فیلترهای فایل و مدیا](#bot_media_filters)

| فیلتر | توضیح |
|------|------|
| `IsFile()` | هر نوع فایل (به جز استیکر) |
| `IsImage()` | عکس |
| `IsVideo()` | ویدیو |
| `IsVoice()` | پیام صوتی |
| `IsMusic()` | موسیقی |
| `IsSticker()` | استیکر |
| `IsPoll()` | نظرسنجی |
| `IsLocation()` | موقعیت مکانی |

**مثال:**

```python
@bot.on_new_message(IsImage())
async def image_handler(bot, event):
    await event.reply(f"عکس {event.file_name} دریافت شد!")

@bot.on_new_message(IsPoll())
async def poll_handler(bot, event):
    await event.reply("یک نظرسنجی دریافت شد!")
```

---

<a id="bot_reply_forward_filters"></a>
## [فیلترهای ریپلای و فوروارد](#bot_reply_forward_filters)

| فیلتر | توضیح |
|------|------|
| `IsReply()` | پیام ریپلای شده |
| `IsForwarded()` | هر نوع فوروارد |
| `ForwardedFromUser()` | فوروارد از کاربر |
| `ForwardedFromChannel()` | فوروارد از کانال |
| `ForwardedFromBot()` | فوروارد از بات |
| `ForwardedNoLink()` | فوروارد با هدایت بسته (پروفایل مخفی) |

**مثال:**

```python
@bot.on_new_message(IsReply())
async def reply_handler(bot, event):
    await event.reply("این پیام به پیام دیگری ریپلای زده!")

@bot.on_new_message(ForwardedFromBot())
async def forward_from_bot(bot, event):
    await event.reply("این پیام از یک بات فوروارد شده!")
```

---

<a id="bot_metadata_filters"></a>
## [فیلترهای متادیتا](#bot_metadata_filters)

| فیلتر | توضیح | مثال |
|------|------|------|
| `HasMetadata()` | پیام فرمت‌دار (Bold, Italic) | - |
| `MetadataType("Bold")` | نوع خاص | - |
| `MetadataType(["Bold", "Italic"])` | چند نوع | - |

**مثال:**

```python
@bot.on_new_message(HasMetadata())
async def metadata_handler(bot, event):
    await event.reply("این پیام فرمت‌دار است!")

@bot.on_new_message(MetadataType("Bold"))
async def bold_handler(bot, event):
    await event.reply("این پیام دارای متن پررنگ است!")
```

---

<a id="bot_access_filters"></a>
## [فیلترهای عضویت و دسترسی](#bot_access_filters)

| فیلتر | توضیح |
|------|------|
| `IsJoined("c0...")` | کاربر عضو چت خاصی باشد |
| `IsJoined(["c0A", "c0B"])` | عضو چند چت باشد |
| `~IsJoined("c0...")` | عضو نباشد |
| `IsAdmin()` | ادمین یا مالک چت |
| `IsOwner()` | فقط مالک چت |

**مثال:**

```python
@bot.on_message(IsJoined("c0abc123def456ghi789jklmno123456") & Command("start"))
async def joined_user(bot, event):
    await event.reply("شما عضو کانال هستید، خوش آمدید!")

@bot.on_new_message(IsAdmin())
async def admin_handler(bot, event):
    await event.reply("شما ادمین این چت هستید!")

@bot.on_new_message(IsOwner())
async def owner_handler(bot, event):
    await event.reply("شما مالک این چت هستید!")
```

---

<div style="display: flex; justify-content: center; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-decorators/" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">→ صفحه قبل</a>

<a href="../bot-guide/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">صفحه اصلی</a>

<a href="../bot-properties/" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">صفحه بعد ←</a>

</div>