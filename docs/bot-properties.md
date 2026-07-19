# پراپرتی‌ها

همه هندلرها یک شیء `event` از نوع `IncomingEnvelope` دریافت می‌کنند با پراپرتی‌های زیر:

---

<a id="bot_base_properties"></a>
## [اطلاعات پایه](#bot_base_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.update_type` | نوع رویداد | `"NewMessage"`, `"UpdatedMessage"`, `"RemovedMessage"`, `"InlineMessage"`, `"StartedBot"`, `"StoppedBot"` |
| `event.chat_id` | آیدی چت | str |
| `event.bot` | نمونه ربات | Any |
| `event.timestamp` | زمان آپدیت | int |
| `event.text` | متن پیام (برای message, edit و callback کار می‌کند) | str یا None |
| `event.author_id` | آیدی فرستنده در روبیکا | str یا None |
| `event.sender_type` | نوع فرستنده | `"User"`, `"Bot"` یا None |
| `event.msg_id` | آیدی پیام (برای حذف شده هم کار می‌کند) | str یا None |
| `event.is_edited` | ویرایش شده؟ | bool |
| `event.message_time` | زمان پیام (از سرور) | str یا None |
| `event.reply_to_message_id` | آیدی پیامی که به آن ریپلای زده شده | str یا None |

---

<a id="bot_file_properties"></a>
## [فایل](#bot_file_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.file_id` | آیدی فایل پیوست | str یا None |
| `event.file_name` | نام اصلی فایل | str یا None |
| `event.file_size` | سایز فایل به بایت | int یا None |
| `event.file_type` | نوع فایل | `"image"`, `"video"`, `"voice"`, `"music"`, `"sticker"`, `"file"` یا None |

---

<a id="bot_forward_properties"></a>
## [فوروارد](#bot_forward_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.is_forwarded` | فوروارد شده؟ (هر نوع) | bool |
| `event.forwarded_from` | اطلاعات فوروارد (با لینک) | dict یا None |
| `event.forwarded_no_link` | اطلاعات فوروارد (پروفایل مخفی) | dict یا None |
| `event.forward_type` | نوع فوروارد | `"User"`, `"Channel"`, `"Bot"`, `"NoLink"` یا None |
| `event.forward_sender_id` | آیدی فرستنده اصلی (از forwarded_from) | str یا None |
| `event.forward_chat_id` | آیدی چت اصلی (از forwarded_from) | str یا None |
| `event.forward_message_id` | آیدی پیام اصلی فوروارد شده | str یا None |
| `event.forward_title` | عنوان (از forwarded_no_link) | str یا None |

---

<a id="bot_button_properties"></a>
## [دکمه](#bot_button_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.button_id` | آیدی دکمه (از aux_data برای کیپاد و اینلاین) | str یا None |
| `event.aux_data` | دیکشنری داده‌های کمکی (شامل button_id) | dict یا None |
| `event.callback_data` | محموله کامل کالبک برای کلیک دکمه اینلاین | dict یا None |
| `event.callback_button_id` | آیدی دکمه از کالبک (وقتی update_type=InlineMessage) | str یا None |

---

<a id="bot_metadata_properties"></a>
## [متادیتا](#bot_metadata_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.metadata` | دیکشنری متادیتا (فرمت‌های Bold, Italic و...) | dict یا None |
| `event.metadata_types` | لیست انواع متادیتای استفاده شده | `["Bold", "Italic", "Quote", "Monospace", "Strikethrough", "Underline", ...]` |
| `event.metadata_parts` | آرایه کامل بخش‌های متادیتا | List[dict] |

---

<a id="bot_utility_methods"></a>
## [متدهای کاربردی](#bot_utility_methods)

| متد | توضیح | پارامترها |
|------|------|------|
| `await event.reply("متن")` | ارسال ریپلای به پیام | content: str, **extras |
| `await event.delete()` | حذف پیام | message_id: str (اختیاری) |
| `await event.copy()` | کپی پیام در همان چت | to_chat_id: str (اختیاری) |
| `await event.forward()` | فوروارد پیام در همان چت | to_chat_id: str (اختیاری) |
| `await event.ban_member()` | بن کردن فرستنده | sender_id: str (اختیاری) |
| `event.pattern_match` | آبجکت match ریجکس (اگر توسط فیلتر ذخیره شده باشد) | - |
| `event.original_data` | دیتای خام API | - |

---

<a id="bot_internal_properties"></a>
## [پراپرتی‌های داخلی](#bot_internal_properties)

| پراپرتی | توضیح |
|------|------|
| `event.message` | دیتای پیام جدید |
| `event.edited_message` | دیتای پیام ویرایش شده |
| `event.deleted_message_id` | آیدی پیام حذف شده |
| `event.callback_payload` | محموله کالبک (برای InlineMessage) |

---

<div style="display: flex; justify-content: center; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="/bot-filters" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">→ صفحه قبل</a>

<a href="/bot-guide" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">صفحه اصلی</a>

<a href="/bot-plugins" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">صفحه بعد ←</a>

</div>