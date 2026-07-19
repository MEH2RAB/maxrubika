# پلاگین

سیستم پلاگین به شما اجازه می‌دهد کد ربات را به ماژول‌های مستقل، قابل استفاده مجدد و قابل اشتراک‌گذاری تقسیم کنید.

---

<a id="bot_plugin_structure"></a>
## [ساختار پایه](#bot_plugin_structure)

هر پلاگین یک کلاس است که از `Plugin` ارث‌بری می‌کند:

```python
from maxrubika.bot.plugin import Plugin, PluginMeta

class MyPlugin(Plugin):
    meta = PluginMeta(
        name="myplugin",
        version="1.0.0",
        description="توضیحات پلاگین",
        author="نام شما"
    )
    
    async def setup(self):
        # هنگام فعال شدن پلاگین اجرا می‌شود
        pass
    
    async def teardown(self):
        # هنگام غیرفعال شدن پلاگین اجرا می‌شود
        pass
```

---

<a id="bot_plugin_methods"></a>
## [روش‌های ساخت پلاگین](#bot_plugin_methods)

### روش ۱: با دکوراتور `@create_plugin`

```python
from maxrubika.bot.plugin import Plugin, create_plugin

@create_plugin("greeter", version="1.0.0", description="پلاگین خوش‌آمدگویی")
class GreeterPlugin(Plugin):
    async def setup(self):
        @self.bot.on_command("hello")
        async def hello(bot, event):
            await event.reply("سلام! 👋")
```

### روش ۲: با `PluginMeta` (برای تنظیمات پیشرفته)

```python
from maxrubika.bot.plugin import Plugin, PluginMeta

class AdminPlugin(Plugin):
    meta = PluginMeta(
        name="admin",
        version="2.0.0",
        description="مدیریت گروه",
        author="MEHRAB",
        dependencies=("logger", "antispam"),
        default_config={
            "admins": [],
            "welcome_message": "خوش آمدید!"
        }
    )
    
    async def setup(self):
        admins = self.get_config("admins", [])
        msg = self.get_config("welcome_message", "")
        
        @self.bot.on_command("ban")
        async def ban(bot, event):
            if event.author_id in admins:
                await bot.ban_member(event.chat_id, "sender_id")
                await event.reply("کاربر مورد نظر باموفقیت بن شد.")
```

---

<a id="bot_plugin_activation"></a>
## [فعال‌سازی پلاگین‌ها](#bot_plugin_activation)

### ثبت دستی

```python
from maxrubika import Bot

bot = Bot("TOKEN")

# ثبت پلاگین
bot.plugin_manager.register_plugin(GreeterPlugin)
bot.plugin_manager.register_plugin(AdminPlugin)

# فعال‌سازی
@bot.on_start()
async def startup(bot):
    await bot.plugin_manager.enable_all()

bot.run()
```

### کشف خودکار از پوشه `plugins/`

```
my_bot/
├── test.py
└── plugins/
    ├── greeter.py
    ├── admin.py
    └── antispam.py
```

```python
# test.py
from maxrubika import Bot

bot = Bot("TOKEN")

@bot.on_start()
async def startup(bot):
    await bot.plugin_manager.enable_all()

bot.run()
```

پلاگین‌ها خودکار از پوشه `plugins/` کشف و فعال می‌شوند.

---

<a id="bot_plugin_management"></a>
## [مدیریت پلاگین‌ها در زمان اجرا](#bot_plugin_management)

```python
# فعال کردن یک پلاگین
await bot.plugin_manager.enable("greeter")

# غیرفعال کردن
await bot.plugin_manager.disable("greeter")

# فعال کردن همه
await bot.plugin_manager.enable_all()

# غیرفعال کردن همه
await bot.plugin_manager.disable_all()

# بارگذاری مجدد
await bot.plugin_manager.reload("greeter")

# بررسی وضعیت
bot.plugin_manager.is_enabled("greeter")      # True/False
bot.plugin_manager.is_registered("greeter")   # True/False
bot.plugin_manager.enabled_plugins            # ['greeter', 'admin']
bot.plugin_manager.registered_plugins         # ['greeter', 'admin', 'logger']

# گرفتن نمونه پلاگین
plugin = bot.plugin_manager.get_plugin("greeter")
print(plugin.is_ready)  # True/False
```

---

<a id="bot_plugin_config"></a>
## [تنظیمات پلاگین](#bot_plugin_config)

```python
# تنظیم تنظیمات
bot.plugin_manager.set_config("admin", {
    "admins": ["u0abc123..."],
    "welcome_message": "سلام به گروه ما!"
})

# گرفتن تنظیمات
config = bot.plugin_manager.get_config("admin")
print(config["admins"])

# داخل پلاگین
class AdminPlugin(Plugin):
    async def setup(self):
        admins = self.get_config("admins", [])
        msg = self.get_config("welcome_message", "خوش آمدید")
```

---

<a id="bot_plugin_dependencies"></a>
## [وابستگی‌ها](#bot_plugin_dependencies)

پلاگین‌ها می‌توانند به پلاگین‌های دیگر وابسته باشند:

```python
@create_plugin("stats", version="1.0.0", dependencies=("logger", "saver"))
class StatsPlugin(Plugin):
    async def setup(self):
        # logger و saver اول فعال می‌شوند
        saver = self.bot.plugin_manager.get_plugin("saver")
        print(f"پیام‌های ذخیره شده: {len(saver.saved)}")
```

سیستم به طور خودکار:

- پلاگین‌های وابسته را اول فعال می‌کند
- از وابستگی دایره‌ای جلوگیری می‌کند
- اگر وابستگی فعال نشود، پلاگین فعال نمی‌شود

---

<a id="bot_plugin_examples"></a>
## [نمونه‌های کاربردی](#bot_plugin_examples)

### پلاگین ضد اسپم

```python
@create_plugin("antispam", version="1.0.0", description="حذف پیام‌های اسپم")
class AntiSpamPlugin(Plugin):
    SPAM_WORDS = "پیام اسپم"
    
    async def setup(self):
        @self.bot.on_new_message(Text(self.SPAM_WORDS) & ChatType("group"))
        async def spam_filter(bot, event):
            await event.delete()
            await bot.send_message(event.chat_id, "⛔ پیام اسپم حذف شد!")
```

### پلاگین لاگر

```python
@create_plugin("logger", version="1.0.0", description="ثبت تمام پیام‌ها")
class LoggerPlugin(Plugin):
    async def setup(self):
        @self.bot.middleware()
        async def log_middleware(bot, event, call_next):
            print(f"[{event.update_type}] {event.chat_id}: {event.text}")
            await call_next()
```

### پلاگین ذخیره پیام

```python
@create_plugin("saver", version="1.0.0")
class MessageSaverPlugin(Plugin):
    async def setup(self):
        self.saved = []
        
        @self.bot.on_new_message(Text("ذخیره") & IsForwarded())
        async def save_forward(bot, event):
            self.saved.append({
                "text": event.text,
                "from": event.forward_title,
                "time": event.message_time
            })
            await event.reply(f"✅ ذخیره شد! ({len(self.saved)} پیام)")
        
        @self.bot.on_command("list")
        async def list_saved(bot, event):
            text = "📋 پیام‌های ذخیره شده:\n\n"
            for i, msg in enumerate(self.saved[-5:], 1):
                text += f"{i}. {msg['text'][:50]}...\n"
            await event.reply(text)
```

### پلاگین تایمر

```python
import asyncio

@create_plugin("timer", version="1.0.0")
class TimerPlugin(Plugin):
    async def setup(self):
        @self.bot.on_command("timer")
        async def timer(bot, event):
            await event.reply("⏰ ۵ ثانیه صبر کن...")
            await asyncio.sleep(5)
            await bot.send_message(event.chat_id, "⏰ وقت تموم شد!")
```

---

<a id="bot_plugin_lifecycle"></a>
## [چرخه حیات پلاگین](#bot_plugin_lifecycle)

```
register_plugin → enable → setup() → فعال و آماده
                        ↓
                  disable → teardown() → غیرفعال
```

---

<a id="bot_plugin_notes"></a>
## [نکات مهم](#bot_plugin_notes)

۱. پلاگین‌ها در `setup()` هندلرها و میدلورها را ثبت می‌کنند
۲. از `self.bot` برای دسترسی به نمونه ربات استفاده کنید
۳. از `self.get_config()` برای خواندن تنظیمات استفاده کنید
۴. پلاگین‌های وابسته خودکار اول فعال می‌شوند
۵. برای اشتراک‌گذاری، فقط فایل پلاگین را کپی کنید
۶. هر پلاگین می‌تواند داده‌های خود را در `self` ذخیره کند
۷. `is_ready` نشان می‌دهد پلاگین فعال و آماده است

---

<div style="display: flex; justify-content: center; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="bot-properties" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">→ صفحه قبل</a>

<a href="bot-guide" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #333;">صفحه اصلی</a>

<a href="bot-more" class="md-button md-button--primary" style="background: linear-gradient(135deg, #4CAF50, #388E3C); border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold;">صفحه بعد ←</a>

</div>