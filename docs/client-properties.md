# پراپرتی‌ها

همه هندلرها یک شیء `event` دریافت می‌کنند با پراپرتی‌های زیر:

---

<a id="client_basic_properties"></a>
## [اطلاعات پایه](#client_basic_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.action` | نوع رویداد | `New`, `Edit`, `Delete` |
| `event.type` | نوع کلی رویداد | str |
| `event.message_id` | شناسه پیام | str |
| `event.object_guid` | شناسه چت | str |
| `event.timestamp` | زمان رویداد | str |
| `event.user_guid` | شناسه کاربر مرتبط | str |
| `event.updated_parameters` | پارامترهای به‌روزرسانی شده | list |
| `event.original_data` | دیتای خام API | dict |

---

<a id="client_message_properties"></a>
## [اطلاعات پیام](#client_message_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.text` | متن پیام | str |
| `event.is_edited` | ویرایش شده؟ | bool |
| `event.author_guid` | شناسه فرستنده | str |
| `event.message_type` | نوع پیام | `Text`, `FileInline`, `Event`, `Sticker` و... |
| `event.message` | شیء کامل پیام | Data |

---

<a id="client_chat_properties"></a>
## [اطلاعات چت](#client_chat_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.chat_guid` | شناسه چت (معادل object_guid) | str |
| `event.is_group` | چت گروه است؟ | bool |
| `event.is_channel` | چت کانال است؟ | bool |
| `event.is_pv` | چت خصوصی است؟ | bool |
| `event.is_bot` | چت بات است؟ | bool |
| `event.is_service` | چت سرویس است؟ | bool |

---

<a id="client_sender_status"></a>
## [وضعیت فرستنده](#client_sender_status)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.is_me` | پیام از خود کاربر است؟ | bool |

---

<a id="client_reply_forward_properties"></a>
## [ریپلای و فوروارد](#client_reply_forward_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.is_reply` | پیام ریپلای است؟ | bool |
| `event.reply_to_message_id` | شناسه پیام ریپلای شده | str یا None |
| `event.is_forward` | پیام فوروارد است؟ | bool |
| `event.forwarded_from` | اطلاعات فوروارد | dict یا None |
| `event.forward_type_from` | نوع فرستنده فوروارد | `User`, `Channel`, `Bot` |
| `event.is_forwarded_from_user` | فوروارد از کاربر؟ | bool |
| `event.is_forwarded_from_channel` | فوروارد از کانال؟ | bool |
| `event.is_forwarded_from_bot` | فوروارد از بات؟ | bool |
| `event.is_forwarded_no_link` | فوروارد با هویت مخفی؟ | bool |

---

<a id="client_file_media_properties"></a>
## [فایل و مدیا](#client_file_media_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.is_file_inline` | پیام حاوی فایل است؟ | bool |
| `event.file_inline` | شیء فایل پیوست | Data یا None |
| `event.file_type` | نوع فایل | `Image`, `Video`, `Voice`, `Music`, `Gif`, `File` و... |
| `event.file_name` | نام فایل | str |
| `event.file_size` | سایز فایل (بایت) | int |
| `event.file_dc_id` | شناسه دیتاسنتر | str |
| `event.file_access_hash` | هش دسترسی فایل | str |
| `event.file_width` | عرض فایل | int |
| `event.file_height` | ارتفاع فایل | int |
| `event.file_duration` | مدت زمان فایل | int |
| `event.file_mime` | نوع MIME فایل | str |
| `event.music_performer` | نام خواننده (فقط موسیقی) | str |
| `event.thumb_inline` | تصویر بندانگشتی (Base64) | str |

---

<a id="client_media_detection"></a>
## [تشخیص نوع مدیا](#client_media_detection)

| پراپرتی | توضیح |
|:------:|------|
| `event.is_text` | پیام متنی است؟ |
| `event.is_image` | تصویر است؟ |
| `event.is_video` | ویدئو (غیر گرد) است؟ |
| `event.is_video_message` | پیام ویدئویی (گرد) است؟ |
| `event.is_voice` | ویس است؟ |
| `event.is_music` | موسیقی است؟ |
| `event.is_gif` | گیف است؟ |
| `event.is_file` | فایل/سند است؟ |
| `event.is_contact` | مخاطب است؟ |
| `event.is_location` | موقعیت مکانی است؟ |
| `event.is_poll` | نظرسنجی است؟ |
| `event.is_live` | پخش زنده است؟ |
| `event.is_sticker` | استیکر است؟ |
| `event.sticker` | شیء استیکر | Data یا None |

---

<a id="client_event_properties"></a>
## [رویداد سیستمی](#client_event_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.is_event` | رویداد سیستمی است؟ | bool |
| `event.event_data` | داده‌های رویداد | dict یا None |
| `event.event_type` | نوع رویداد سیستمی | `AddedGroupMembers`, `PinnedMessageUpdated` و... |

---

<a id="client_metadata_reaction_properties"></a>
## [متادیتا و ری‌اکشن](#client_metadata_reaction_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.has_metadata` | پیام متادیتا دارد؟ | bool |
| `event.metadata` | متادیتای پیام | dict یا None |
| `event.metadata_types` | انواع متادیتا | list |
| `event.has_reaction` | پیام ری‌اکشن دارد؟ | bool |
| `event.reactions` | ری‌اکشن‌های پیام | dict یا None |

---

<a id="client_user_activity_properties"></a>
## [فعالیت کاربر](#client_user_activity_properties)

| پراپرتی | توضیح | نوع |
|:------:|------|:------:|
| `event.user_activity_guid` | شناسه کاربر در حال فعالیت | str |

---

<a id="client_utility_methods"></a>
## [متدهای کاربردی](#client_utility_methods)

| متد | توضیح |
|:------:|------|
| `await event.reply("متن")` | ریپلای سریع به پیام |
| `await event.delete()` | حذف پیام |
| `await event.copy()` | کپی پیام در همان چت |
| `await event.copy("chat_id")` | کپی پیام به چت دیگر |
| `await event.forward()` | فوروارد پیام در همان چت |
| `await event.forward("chat_id")` | فوروارد پیام به چت دیگر |
| `await event.pin()` | سنجاق کردن پیام |
| `await event.unpin()` | برداشتن سنجاق پیام |
| `await event.seen()` | علامت‌گذاری پیام به عنوان دیده‌شده |
| `await event.add_reaction(id)` | افزودن ری‌اکشن |
| `await event.remove_reaction(id)` | حذف ری‌اکشن |
| `await event.download()` | دانلود فایل پیوست |
| `await event.get_author()` | دریافت اطلاعات فرستنده |
| `await event.get_chat()` | دریافت اطلاعات چت |
| `await event.ban_member()` | مسدود کردن فرستنده |
| `await event.unban_member()` | رفع مسدودیت فرستنده |
| `await event.block_user()` | بلاک کردن فرستنده |
| `await event.unblock_user()` | رفع بلاک فرستنده |
| `await event.member_is_admin()` | بررسی ادمین بودن عضو |
| `await event.send_activity("Typing")` | ارسال فعالیت (تایپ، آپلود، ضبط) |
| `event.guid_type()` | تشخیص نوع چت (Group, Channel, User...) |

---

<div style="display: flex; gap: 12px; flex-wrap: wrap;">

<a href="../client-messenger/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به صفحه قبل</a>

</div>