# پراپرتی‌ها

همه هندلرها یک شیء `event` دریافت می‌کنند با پراپرتی‌های زیر:

---

<a id="bot_base_properties"></a>
## [اطلاعات پایه](#bot_base_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.update_type` | نوع رویداد | `"NewMessage"`, `"UpdatedMessage"`, `"RemovedMessage"`, `"InlineMessage"`, `"StartedBot"`, `"StoppedBot"`, `"EventData"` |
| `event.chat_id` | آیدی چت | str |
| `event.text` | متن پیام | str یا None |
| `event.msg_id` | آیدی پیام | str یا None |
| `event.message_id` | مترادف `msg_id` | str یا None |
| `event.author_id` | آیدی فرستنده | str یا None |
| `event.sender_id` | مترادف `author_id` | str یا None |
| `event.sender_type` | نوع فرستنده | `"User"`, `"Bot"` یا None |
| `event.is_edited` | ویرایش شده؟ | bool |
| `event.is_deleted` | پاک شده؟ | bool |
| `event.timestamp` | زمان آپدیت (سرور) | int |
| `event.message_time` | زمان پیام | str یا None |

---

<a id="bot_file_properties"></a>
## [فایل](#bot_file_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.file_id` | آیدی فایل پیوست | str یا None |
| `event.file_name` | نام اصلی فایل | str یا None |
| `event.file_size` | سایز فایل به بایت | int یا None |
| `event.file_type` | نوع فایل | `"image"`, `"video"`, `"voice"`, `"music"`, `"sticker"`, `"file"` یا None |
| `event.is_image` | عکس است؟ | bool |
| `event.is_video` | ویدیو است؟ | bool |
| `event.is_voice` | ویس است؟ | bool |
| `event.is_music` | موزیک است؟ | bool |

---

<a id="bot_media_properties"></a>
## [استیکر، موقعیت مکانی و نظرسنجی](#bot_media_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.sticker` | دیتای استیکر | dict یا None |
| `event.sticker_id` | آیدی استیکر | str یا None |
| `event.is_sticker` | استیکر است؟ | bool |
| `event.poll` | دیتای نظرسنجی | dict یا None |
| `event.poll_options` | گزینه‌های نظرسنجی | list یا None |
| `event.is_poll` | نظرسنجی است؟ | bool |
| `event.location` | دیتای موقعیت مکانی | dict یا None |
| `event.is_location` | موقعیت مکانی است؟ | bool |

---

<a id="bot_button_properties"></a>
## [دکمه‌های کیبورد](#bot_button_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.button_id` | آیدی دکمه | str یا None |
| `event.aux_data` | دیکشنری aux_data | dict یا None |
| `event.callback_payload` | کل payload کلیک دکمه | dict یا None |
| `event.callback_data` | مترادف `callback_payload` | dict یا None |
| `event.callback_button_id` | آیدی دکمه (فقط InlineMessage) | str یا None |

---

<a id="bot_forward_properties"></a>
## [فوروارد](#bot_forward_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.is_forwarded` | فوروارد شده؟ (هر نوع) | bool |
| `event.forward_type` | نوع فوروارد | `"User"`, `"Channel"`, `"Bot"`, `"NoLink"` یا None |
| `event.forward_sender_id` | آیدی فرستنده اصلی | str یا None |
| `event.forward_chat_id` | آیدی چت اصلی | str یا None |
| `event.forward_message_id` | آیدی پیام اصلی فوروارد شده | str یا None |
| `event.forward_title` | عنوان (هدایت بسته) | str یا None |
| `event.forwarded_from` | اطلاعات فوروارد (با لینک) | dict یا None |
| `event.forwarded_no_link` | اطلاعات فوروارد (هدایت بسته) | dict یا None |
| `event.is_forwarded_from_user` | فوروارد از کاربر؟ | bool |
| `event.is_forwarded_from_channel` | فوروارد از کانال؟ | bool |
| `event.is_forwarded_from_bot` | فوروارد از بات؟ | bool |
| `event.is_forwarded_no_link` | هدایت بسته؟ | bool |

---

<a id="bot_metadata_properties"></a>
## [متادیتا](#bot_metadata_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.metadata` | دیکشنری متادیتا (Bold, Italic و...) | dict یا None |
| `event.metadata_types` | لیست انواع متادیتا | `["Bold", "Italic", "Quote", "Monospace", "Strikethrough", "Underline", ...]` |
| `event.metadata_parts` | آرایه کامل بخش‌های متادیتا | List[dict] |
| `event.metadata_type` | اولین نوع متادیتا | str یا None |

---

<a id="bot_chat_user_properties"></a>
## [چت و کاربر](#bot_chat_user_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.is_user` | پیوی کاربر؟ | bool |
| `event.is_group` | گروه؟ | bool |
| `event.is_channel` | کانال؟ | bool |
| `event.is_text` | متن خالص؟ | bool |
| `event.is_reply` | ریپلای؟ | bool |
| `event.is_command` | با `/` شروع می‌شود؟ | bool |

---

<a id="bot_command_properties"></a>
## [دستورات](#bot_command_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.command` | نام دستور (بدون `/`) | str یا None |
| `event.command_args` | آرگومان‌های بعد از دستور | str یا None |
| `event.is_command` | با `/` شروع می‌شود؟ | bool |

---

<a id="bot_reply_properties"></a>
## [ریپلای](#bot_reply_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.reply_to_message_id` | آیدی پیام ریپلای شده | str یا None |
| `event.reply_to_msg_id` | مترادف `reply_to_message_id` | str یا None |
| `event.is_reply` | ریپلای است؟ | bool |

---

<a id="bot_event_properties"></a>
## [الگو و رویداد](#bot_event_properties)

| پراپرتی | توضیح | نوع |
|------|------|------|
| `event.pattern_match` | آبجکت match از فیلتر regex | Match یا None |
| `event.event_data` | payload رویداد EventData | dict یا None |
| `event.event_type` | نوع رویداد داخل `event_data` | str یا None |
| `event.message` | payload پیام جدید (NewMessage) | dict یا None |
| `event.edited_message` | payload پیام ویرایش‌شده (UpdatedMessage) | dict یا None |
| `event.deleted_message_id` | آیدی پیام پاک‌شده | str یا None |

---

<a id="bot_utility_methods"></a>
## [متدهای کاربردی](#bot_utility_methods)

| متد | توضیح |
|------|------|
| `await event.reply("متن")` | ریپلای سریع |
| `await event.delete()` | حذف پیام |
| `await event.copy()` | کپی پیام در همان چت |
| `await event.copy("chat_id")` | کپی پیام به چت دیگر |
| `await event.forward()` | فوروارد پیام در همان چت |
| `await event.forward("chat_id")` | فوروارد پیام به چت دیگر |
| `await event.ban_member()` | بن کردن کاربر |
| `await event.is_admin()` | آیا ادمین است؟ |
| `await event.is_owner()` | آیا سازنده است؟ |
| `await event.is_joined("chat_id")` | آیا عضو چت است؟ |
| `await event.get_chat_info()` | دریافت اطلاعات چت |
| `event.original_data` | دیتای خام API |

---

<a id="bot_reply_methods"></a>
## [متدهای ریپلای تخصصی](#bot_reply_methods)

| متد | توضیح |
|------|------|
| `await event.reply_image()` | ریپلای عکس |
| `await event.reply_video()` | ریپلای ویدیو |
| `await event.reply_gif()` | ریپلای گیف |
| `await event.reply_music()` | ریپلای موزیک |
| `await event.reply_voice()` | ریپلای ویس |
| `await event.reply_file()` | ریپلای فایل |
| `await event.reply_contact()` | ریپلای مخاطب |
| `await event.reply_location()` | ریپلای موقعیت مکانی |
| `await event.reply_poll()` | ریپلای نظرسنجی |
| `await event.reply_quiz()` | ریپلای کوییز |

---

<div style="display: flex; justify-content: center; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-filters/" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">→ صفحه قبل</a>

<a href="../bot-guide/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">صفحه اصلی</a>

<a href="../bot-plugins/" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">صفحه بعد ←</a>

</div>