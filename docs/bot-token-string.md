# توکن استرینگ (TokenString) و امنیت آن

---

توکن بات یکی از حساس‌ترین اطلاعات پروژه است. اگر توکن شما به دست شخص دیگری بیفتد، می‌تواند از طرف بات شما به کاربران پیام بفرستد، اطلاعات گروه‌ها را بخواند یا حتی بات را مختل کند.

**TokenString** یک راهکار امنیتی برای ذخیره و انتقال توکن است. این قابلیت توکن خام بات را به یک رشتهٔ رمزنگاری‌شده تبدیل می‌کند و می‌توانید آن را جای توکن اصلی استفاده کنید.

---

## مزایای امنیتی TokenString

1. **رمزنگاری:** توکن اصلی بات هرگز به‌صورت متن ساده ذخیره یا ارسال نمی‌شود.
2. **رمز عبور اختیاری:** می‌توانید TokenString را با یک رمز عبور محافظت کنید. در این صورت، حتی اگر رشتهٔ رمزنگاری‌شده لو برود، بدون رمز عبور قابل استفاده نیست.
3. **دور ماندن از مخازن:** می‌توانید TokenString را در فایل‌های تنظیمات، متغیرهای محیطی یا مخزن کد قرار دهید بدون نگرانی از افشای توکن اصلی.
4. **چرخش توکن:** در صورت نیاز، می‌توانید TokenString جدید بسازید بدون اینکه توکن اصلی بات تغییر کند.

---

## ساخت TokenString از توکن فعلی

با متد `get_token_string()` می‌توانید توکن فعلی بات را به یک TokenString رمزنگاری‌شده تبدیل کنید:

```python
from maxrubika import Bot

with Bot("TOKEN") as bot:
    # بدون رمز عبور
    token_string = bot.get_token_string()

    # با رمز عبور (امن‌تر)
    token_string = bot.get_token_string(password="my_secret_password")

    print(token_string)
```

---

## استفاده از TokenString برای ساخت ربات

```python
from maxrubika import Bot

with Bot(token_string="ENCRYPTED_STRING", password="my_secret_password") as bot:
    print(bot.get_me())
```

---

## پارامترهای `get_token_string`

| پارامتر | نوع | پیش‌فرض | توضیح |
|------|------|:------:|------|
| `password` | str | `None` | رمز عبور اختیاری برای رمزنگاری. اگر بدهید، TokenString فقط با همین رمز قابل باز شدن است. |

---

## نکات مهم

1. اگر TokenString را با رمز عبور بسازید، **حتماً رمز را جای امنی نگه دارید.** بدون آن، TokenString قابل بازیابی نیست.
2. TokenString در واقع توکن اصلی نیست، بلکه یک نسخهٔ رمزنگاری‌شده است. توکن اصلی همچنان در سمت سرور روبیکا معتبر است.

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-more/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به توضیحات بیشتر</a>

</div>