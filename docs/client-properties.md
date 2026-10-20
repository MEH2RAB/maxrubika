# پراپرتی‌ها

همه هندلرها یک شیء `event` دریافت می‌کنند با پراپرتی‌های زیر:

---

<a id="client_basic_properties"></a>
## [اطلاعات پایه](#client_basic_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.action` | نوع اکشن رویداد | `New`, `Edit`, `Delete` |
| `event.type` | نوع رویداد | str |
| `event.text` | متن پیام یا کپشن | str |
| `event.message` | کل دیتای پیام | Data |
| `event.message_id` | آیدی پیام | str |
| `event.message_type` | نوع پیام | `Text`, `FileInline`, `Event`, `Sticker` و... |
| `event.timestamp` | زمان رویداد (تایم‌استمپ) | str |
| `event.original_data` | دیتای خام API | dict |
| `event.author_guid` | آیدی فرستنده | str |
| `event.author_type` | نوع فرستنده | str |
| `event.author_title` | نام نمایشی فرستنده | str |
| `event.is_mine` | پیام خودت؟ | bool |
| `event.is_me` | پیام خودت؟ (بر اساس GUID) | bool |
| `event.is_edited` | ویرایش شده؟ | bool |
| `event.is_reply` | ریپلای؟ | bool |
| `event.reply_to_message_id` | آیدی پیام ریپلای‌شده | str یا None |
| `event.updated_parameters` | لیست پارامترهای آپدیت‌شده | list |
| `event.pattern_match` | match آبجکت از فیلتر TextMatch | Match یا None |

---

<a id="client_chat_properties"></a>
## [اطلاعات چت](#client_chat_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.chat_guid` | آیدی چت (object_guid) | str |
| `event.chat_type` | نوع چت | `User`, `Group`, `Channel`, ... |
| `event.is_group` | گروه؟ | bool |
| `event.is_channel` | کانال؟ | bool |
| `event.is_pv` | پیوی؟ | bool |
| `event.is_bot` | بات؟ | bool |
| `event.is_service` | سرویس؟ | bool |
| `event.guid_type(chat_guid)` | نوع هر GUID (User, Group, Channel, Bot, Service) | str |

---

<a id="client_file_media_properties"></a>
## [فایل و مدیا](#client_file_media_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.file_inline` | دیتای فایل (Data) | Data یا None |
| `event.file_inline_raw` | دیتای فایل (dict خام) | dict یا None |
| `event.file_type` | نوع فایل | `Image`, `Video`, `Voice`, `Music`, `Gif`, `File` و... |
| `event.file_id` | آیدی فایل | str |
| `event.file_name` | نام فایل | str |
| `event.file_size` | سایز (بایت) | int |
| `event.file_dc_id` | آیدی دیتاسنتر | str |
| `event.file_access_hash` | هش دسترسی | str |
| `event.file_width` | عرض (عکس/ویدیو) | int |
| `event.file_height` | ارتفاع (عکس/ویدیو) | int |
| `event.file_duration` | مدت (صوت/ویدیو) | int |
| `event.file_mime` | MIME type | str |
| `event.thumb_inline` | تصویر بندانگشتی | str |
| `event.music_performer` | نام خواننده | str |
| `event.is_round` | ویدیو دایره‌ای؟ | bool |

---

<a id="client_media_detection"></a>
## [تشخیص نوع محتوا](#client_media_detection)

| پراپرتی | توضیح |
|:------:|------|
| `event.is_text` | متن ساده؟ |
| `event.is_file_inline` | فایل اینلاین؟ (FileInline / FileInlineCaption) |
| `event.is_event` | رویداد سیستمی؟ |
| `event.is_image` | عکس؟ |
| `event.is_video` | ویدیو؟ |
| `event.is_video_message` | ویدیو دایره‌ای؟ |
| `event.is_voice` | ویس؟ |
| `event.is_music` | موزیک؟ |
| `event.is_gif` | گیف؟ |
| `event.is_file` | فایل (سند)؟ |
| `event.is_contact` | مخاطب؟ |
| `event.is_location` | موقعیت مکانی؟ |
| `event.is_poll` | نظرسنجی؟ |
| `event.is_live` | لایو؟ |
| `event.is_sticker` | استیکر؟ |
| `event.sticker` | دیتای استیکر (Data) |
| `event.sticker_raw` | دیتای استیکر (dict خام) |

---

<a id="client_reaction_properties"></a>
## [واکنش‌ها](#client_reaction_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.has_reaction` | واکنش دارد؟ | bool |
| `event.reactions` | دیتای واکنش‌ها | dict یا None |

---

<a id="client_forward_properties"></a>
## [فوروارد](#client_forward_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.is_forward` | فوروارد شده؟ | bool |
| `event.forwarded_from` | اطلاعات فوروارد | dict یا None |
| `event.forwarded_no_link` | فوروارد با هدایت بسته | dict یا None |
| `event.forward_type_from` | نوع مبدأ | `User`, `Channel`, `Bot` |
| `event.is_forwarded_from_user` | از کاربر؟ | bool |
| `event.is_forwarded_from_channel` | از کانال؟ | bool |
| `event.is_forwarded_from_bot` | از بات؟ | bool |
| `event.is_forwarded_no_link` | هدایت بسته؟ | bool |

---

<a id="client_bot_properties"></a>
## [اطلاعات بات](#client_bot_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.via_bot` | GUID باتی که پیام از طریقش فرستاده شده | str یا None |
| `event.is_via_bot` | از طریق بات ارسال شده؟ | bool |

---

<a id="client_metadata_event_properties"></a>
## [متادیتا و رویداد](#client_metadata_event_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.has_metadata` | فرمت‌دار؟ | bool |
| `event.metadata` | دیتای متادیتا | dict یا None |
| `event.metadata_types` | لیست نوع‌های متادیتا | list |
| `event.event_data` | دیتای رویداد سیستمی | dict یا None |
| `event.event_type` | نوع رویداد سیستمی | `AddedGroupMembers`, `PinnedMessageUpdated` و... |
| `event.user_activity_guid` | شناسه کاربر در رویداد اکتیویتی | str |

---

<a id="client_utility_methods"></a>
## [متدهای کمکی (Helper Methods)](#client_utility_methods)

| متد | توضیح |
|:------:|------|
| `await event.reply("متن")` | ریپلای سریع |
| `await event.edit("متن جدید")` | ادیت پیام |
| `await event.delete()` | حذف پیام |
| `await event.copy()` | کپی در همان چت |
| `await event.copy("chat_guid")` | کپی به چت دیگر |
| `await event.forward()` | فوروارد در همان چت |
| `await event.forward("chat_guid")` | فوروارد به چت دیگر |
| `await event.pin()` | پین کردن پیام |
| `await event.unpin()` | آنپین کردن پیام |
| `await event.seen()` | علامت‌گذاری به‌عنوان دیده‌شده |
| `await event.add_reaction(id)` | افزودن واکنش |
| `await event.remove_reaction(id)` | حذف واکنش |
| `await event.download()` | دانلود فایل پیام |
| `await event.send_activity("Typing")` | ارسال اکتیویتی (Typing/Uploading/Recording) |

---

<a id="client_reply_methods"></a>
## [متدهای ریپلای تخصصی](#client_reply_methods)

| متد | توضیح |
|:------:|------|
| `await event.reply_image()` | ریپلای عکس |
| `await event.reply_video()` | ریپلای ویدیو |
| `await event.reply_video_message()` | ریپلای ویدیو دایره‌ای |
| `await event.reply_gif()` | ریپلای گیف |
| `await event.reply_music()` | ریپلای موزیک |
| `await event.reply_voice()` | ریپلای ویس |
| `await event.reply_file()` | ریپلای فایل |
| `await event.reply_contact()` | ریپلای مخاطب |
| `await event.reply_location()` | ریپلای موقعیت مکانی |
| `await event.reply_poll()` | ریپلای نظرسنجی |
| `await event.reply_quiz()` | ریپلای کوییز |

---

<a id="client_management_methods"></a>
## [متدهای مدیریتی](#client_management_methods)

| متد | توضیح |
|:------:|------|
| `await event.get_author()` | اطلاعات فرستنده |
| `await event.get_chat()` | اطلاعات چت |
| `await event.ban_member()` | بن کردن عضو |
| `await event.unban_member()` | آنبن کردن عضو |
| `await event.member_is_admin()` | آیا ادمین است؟ |
| `await event.block_user()` | بلاک کاربر |
| `await event.unblock_user()` | آنبلاک کاربر |
| `await event.mute_chat()` | بی‌صدا کردن چت |
| `await event.unmute_chat()` | لغو بی‌صدا |
| `await event.archive_chat()` | آرشیو چت |
| `await event.unarchive_chat()` | لغو آرشیو |
| `await event.delete_user_chat()` | حذف چت کاربر |

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">

<a href="../client-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>