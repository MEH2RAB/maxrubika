# فیلترها

فیلترها با `&` (AND)، `|` (OR) و `~` (NOT) ترکیب می‌شوند.

```python
# AND - پیام کاربر خاص در گروه
@client.on_new_message(FromUser("u0abc...") & ChatType("group"))

# OR - گروه یا کانال
@client.on_new_message(ChatType("group") | ChatType("channel"))

# NOT - هر چیزی غیر از خودم
@client.on_new_message(~IsMe())
```

---

<a id="client_event_filters"></a>
## [فیلترهای نوع رویداد](#client_event_filters)

| <div style="text-align:center">فیلتر</div> | <div style="text-align:center">توضیح</div> |
|------|------|
| `IsMessage()` | پیام جدید |
| `IsEdited()` | پیام ویرایش شده |
| `IsDeleted()` | پیام پاک شده |

---

<a id="client_chat_user_filters"></a>
## [فیلترهای چت و کاربر](#client_chat_user_filters)

| <div style="text-align:center">فیلتر</div> | <div style="text-align:center">توضیح</div> | <div style="text-align:center">مثال</div> |
|------|------|------|
| `ChatType("user")` | نوع چت | `ChatType("group")` |
| `ChatType(["group", "channel"])` | چند نوع | |
| `FromChat("id")` | چت خاص (GUID، نام‌کاربری یا لینک) | `FromChat("g0abc...")` |
| `FromUser("id")` | کاربر خاص | `FromUser("@Online_User")` |
| `FromBot("id")` | بات خاص | `FromBot("@MyBot")` |
| `FromActivity("id")` | فعالیت از کاربر خاص | `FromActivity("u0abc...")` |
| `IsMe()` | پیام‌های خود کاربر | |

---

<a id="client_media_filters"></a>
## [فیلترهای فایل و مدیا](#client_media_filters)

| <div style="text-align:center">فیلتر</div> | <div style="text-align:center">توضیح</div> |
|------|------|
| `IsText()` | فقط پیام متنی (بدون فایل) |
| `IsImage()` | تصویر |
| `IsVideo()` | ویدئو (غیر گرد) |
| `IsVideoMessage()` | پیام ویدئویی (ویدئوی گرد) |
| `IsVoice()` | پیام صوتی (ویس) |
| `IsMusic()` | فایل موسیقی |
| `IsGif()` | گیف |
| `IsSticker()` | استیکر |
| `IsFile()` | فایل/سند |
| `IsContact()` | مخاطب |
| `IsLocation()` | موقعیت مکانی |
| `IsPoll()` | نظرسنجی |
| `IsLive()` | پخش زنده |

---

<a id="client_event_system_filters"></a>
## [فیلترهای رویداد سیستمی](#client_event_system_filters)

| <div style="text-align:center">فیلتر</div> | <div style="text-align:center">توضیح</div> | <div style="text-align:center">مثال</div> |
|------|------|------|
| `IsEvent()` | هر رویداد سیستمی | |
| `EventType("type")` | نوع خاص رویداد | `EventType("AddedGroupMembers")` |

**انواع رویداد:** `RemoveGroupMembers`, `AddedGroupMembers`, `PinnedMessageUpdated`, `TitleUpdate`, `PhotoUpdate`, `RemovePhoto`, `SetAutoDelete`, `JoinedGroupByLink`, `LeaveGroup`, `JoinedGroupByRequest`, `CreateGroupVoiceChat`, `StopGroupVoiceChat`, `GroupCreated`, `ChannelCreated`

---

<a id="client_reply_forward_filters"></a>
## [فیلترهای ریپلای و فوروارد](#client_reply_forward_filters)

| <div style="text-align:center">فیلتر</div> | <div style="text-align:center">توضیح</div> |
|------|------|
| `IsReply()` | پیام ریپلای شده |
| `IsForwarded()` | هر نوع فوروارد |
| `ForwardedFromUser()` | فوروارد از کاربر |
| `ForwardedFromChannel()` | فوروارد از کانال |
| `ForwardedFromBot()` | فوروارد از بات |
| `ForwardedNoLink()` | فوروارد با هویت مخفی |

---

<a id="client_text_filters"></a>
## [فیلترهای متن](#client_text_filters)

| <div style="text-align:center">فیلتر</div> | <div style="text-align:center">توضیح</div> | <div style="text-align:center">مثال</div> |
|------|------|------|
| `Text("pattern")` | متن شامل الگو باشد | `Text("سلام")` |
| `TextMatch("pattern")` | مانند Text + ذخیره match | `TextMatch(r"اسم (\w+)")` |
| `Command("name")` | دستور با / شروع شود | `Command("start")` |
| `Command()` | هر دستوری | |
| `Command(["start", "help"])` | چند دستور | |

---

<a id="client_metadata_reaction_filters"></a>
## [فیلترهای متادیتا و ری‌اکشن](#client_metadata_reaction_filters)

| <div style="text-align:center">فیلتر</div> | <div style="text-align:center">توضیح</div> | <div style="text-align:center">مثال</div> |
|------|------|------|
| `HasMetadata()` | پیام فرمت‌دار (Bold, Italic) | |
| `MetadataType("Bold")` | نوع خاص | `MetadataType(["Bold", "Italic"])` |
| `HasReaction()` | پیام دارای ری‌اکشن | |

---

<a id="client_filter_examples"></a>
## [مثال‌های ترکیبی](#client_filter_examples)

```python
# فقط تصاویر در گروه
@client.on_new_message(IsImage() & ChatType("group"))
async def group_images(event):
    await event.reply("تصویر در گروه دریافت شد!")

# پیام متنی از کاربر خاص که ریپلای نباشد
@client.on_new_message(FromUser("@Online_User") & IsText() & ~IsReply())
async def text_from_user(event):
    print(f"پیام: {event.text}")

# دستور start یا help
@client.on_new_message(Command(["start", "help"]))
async def commands(event):
    await event.reply("در خدمتم!")

# تشخیص نام با TextMatch
@client.on_new_message(TextMatch(r"اسم من (\w+) هست"))
async def name_catcher(event):
    name = event.pattern_match.group(1)
    await event.reply(f"سلام {name}!")

# رویداد افزودن عضو به گروه
@client.on_message(EventType("AddedGroupMembers"))
async def new_member(event):
    print("کاربر جدید اضافه شد!")

# پیام فوروارد شده از کانال
@client.on_new_message(IsForwarded() & ForwardedFromChannel())
async def forwarded_from_channel(event):
    print("فوروارد از کانال")
```

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">

<a href="client-messenger" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>