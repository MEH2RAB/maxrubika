# ساخت و پیکربندی بات

---

هنگام ساخت نمونه ربات، می‌توانید پارامترهای زیر را به سازنده کلاس `Bot` بدهید:

| پارامتر | نوع | پیش‌فرض | توضیح |
|------|------|:------:|------|
| `token` | str | `None` | توکن احراز هویت بات. اگر خالی یا نامعتبر باشد، از کاربر در ترمینال درخواست می‌شود. |
| `token_string` | str | `None` | نسخهٔ رمزنگاری‌شدهٔ توکن. **اولویت آن از `token` بیشتر است.** |
| `password` | str | `None` | رمز عبور برای رمزگشایی `token_string` (در صورت استفاده). |
| `base_url` | str | `"https://botapi.shad.ir/v3"` | آدرس پایهٔ API. |
| `timeout` | int/float | `30` | مدت زمان انتظار برای هر درخواست (ثانیه). |
| `max_retries` | int | `5` | حداکثر تعداد تلاش مجدد در صورت خطای شبکه. |
| `show_welcome` | bool | `True` | نمایش پیام خوش‌آمدگویی کتابخانه هنگام راه‌اندازی. |
| `run_all_handlers` | bool | `True` | اگر `True` باشد، همهٔ هندلرهایی که شرطشان با رویداد مطابقت دارد اجرا می‌شوند. اگر `False` باشد، تنها اولین هندلر مطابق اجرا می‌شود. |

---

## نکات مهم

1. **اولویت `token_string`:** اگر هم `token` و هم `token_string` را بدهید، `token_string` استفاده می‌شود (و در صورت نیاز با `password` رمزگشایی می‌شود).

2. **`run_all_handlers`:** اگر چند هندلر با یک رویداد مطابقت داشته باشند، با `True` همه اجرا می‌شوند و با `False` فقط اولی.

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-more/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به توضیحات بیشتر</a>

</div>